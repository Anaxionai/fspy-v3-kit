"""Tests for make_seed.py.

Run them from this folder with either command:

    uv run --with pytest pytest -q
    python -m pytest -q
"""

import csv
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pytest

import make_seed

HERE = Path(__file__).parent
FILES = ("stations.csv", "trains.csv", "coaches.csv", "schedules.csv")


def read(folder: Path, name: str) -> list[dict[str, str]]:
    with (folder / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


@pytest.fixture(scope="module")
def seed(tmp_path_factory) -> Path:
    """A fresh copy of the normal set, made by running the script like a student."""
    out = tmp_path_factory.mktemp("seed")
    subprocess.run([sys.executable, str(HERE / "make_seed.py"), "--out-dir", str(out)],
                   check=True, capture_output=True, text=True)
    return out


def minutes(day_offset: str, hh_mm: str) -> int:
    hours, mins = hh_mm.split(":")
    return int(day_offset) * 1440 + int(hours) * 60 + int(mins)


def test_committed_files_match_the_generator(seed):
    """The CSV files in the kit must be exactly what the generator makes today."""
    for name in FILES:
        committed = (HERE / name).read_text(encoding="utf-8").replace("\r\n", "\n")
        assert committed == (seed / name).read_text(encoding="utf-8"), name


def test_same_command_gives_the_same_files(seed, tmp_path):
    subprocess.run([sys.executable, str(HERE / "make_seed.py"), "--out-dir", str(tmp_path)], check=True,
                   capture_output=True)
    for name in FILES:
        assert (tmp_path / name).read_bytes() == (seed / name).read_bytes(), name


def test_headers(seed):
    expected = {
        "stations.csv": "code,name,city,state,zone,latitude,longitude",
        "trains.csv": "number,name,type,from_station,to_station,runs_on",
        "coaches.csv": "train_number,coach_code,class,seats",
        "schedules.csv": "train_number,stop_seq,station_code,arrival,departure,day_offset,km",
    }
    for name, header in expected.items():
        assert (seed / name).read_text(encoding="utf-8").splitlines()[0] == header


def test_stations(seed):
    stations = read(seed, "stations.csv")
    codes = [s["code"] for s in stations]
    assert 55 <= len(stations) <= 70
    assert len(codes) == len(set(codes)), "station codes are unique"
    for code in ("NDLS", "BCT", "MAS", "HWH", "SBC", "PUNE", "ADI"):
        assert code in codes
    for s in stations:
        assert 6 <= float(s["latitude"]) <= 36 and 68 <= float(s["longitude"]) <= 98, s  # inside India
        assert s["zone"] in {"NR", "NER", "NFR", "ER", "SER", "ECR", "ECoR", "NCR", "NWR", "WCR", "WR", "CR",
                              "SECR", "SR", "SWR", "SCR", "SCoR", "KR"}


def test_trains(seed):
    trains = read(seed, "trains.csv")
    numbers = [int(t["number"]) for t in trains]
    assert len(trains) == 120
    assert len(numbers) == len(set(numbers)), "train numbers are unique"
    assert all(10_000 <= n <= 99_999 for n in numbers), "train numbers have five digits"
    for t in trains:
        if int(t["number"]) % 2 == 1:  # the return train has the next number and the reverse route
            back = next(b for b in trains if int(b["number"]) == int(t["number"]) + 1)
            assert (back["from_station"], back["to_station"]) == (t["to_station"], t["from_station"])
        days = t["runs_on"].split()
        assert days and len(days) == len(set(days)) and set(days) <= set(make_seed.WEEK)
        assert t["type"] in make_seed.TYPES


def test_coaches(seed):
    trains = {t["number"] for t in read(seed, "trains.csv")}
    coaches = read(seed, "coaches.csv")
    seen = set()
    per_train = defaultdict(int)
    for c in coaches:
        assert c["train_number"] in trains
        assert c["class"] in ("1A", "2A", "3A", "SL", "CC")
        assert int(c["seats"]) == make_seed.SEATS_PER_COACH[c["class"]]
        assert re.fullmatch(r"[HABSC]\d{1,2}", c["coach_code"])
        assert (c["train_number"], c["coach_code"]) not in seen, "coach codes are unique within a train"
        seen.add((c["train_number"], c["coach_code"]))
        per_train[c["train_number"]] += 1
    assert set(per_train) == trains, "every train has coaches"


def test_schedules(seed):
    trains = {t["number"]: t for t in read(seed, "trains.csv")}
    codes = {s["code"] for s in read(seed, "stations.csv")}
    stops = defaultdict(list)
    for row in read(seed, "schedules.csv"):
        stops[row["train_number"]].append(row)
    assert set(stops) == set(trains)
    for number, rows in stops.items():
        assert [int(r["stop_seq"]) for r in rows] == list(range(1, len(rows) + 1))
        assert len(rows) >= 2
        first, last = rows[0], rows[-1]
        assert first["arrival"] == "" and first["departure"] and first["day_offset"] == "0" and first["km"] == "0"
        assert last["departure"] == "" and last["arrival"]
        assert (first["station_code"], last["station_code"]) == (trains[number]["from_station"],
                                                                trains[number]["to_station"])
        times = []
        for r in rows:
            assert r["station_code"] in codes
            for value in (r["arrival"], r["departure"]):
                if value:
                    assert re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", value)
                    times.append(minutes(r["day_offset"], value))
        assert times == sorted(times), f"train {number} goes back in time"
        kms = [int(r["km"]) for r in rows]
        assert kms == sorted(kms) and len(set(kms)) == len(kms), f"train {number}: km must grow"


def test_every_station_has_a_train(seed):
    used = {r["station_code"] for r in read(seed, "schedules.csv")}
    assert used == {s["code"] for s in read(seed, "stations.csv")}


def test_daily_trains_from_new_delhi_to_mumbai_central(seed):
    """P3 searches NDLS to BCT, and P4's Playwright test books on one of these trains."""
    trains = {t["number"]: t for t in read(seed, "trains.csv")}
    order = defaultdict(dict)
    for r in read(seed, "schedules.csv"):
        order[r["train_number"]][r["station_code"]] = int(r["stop_seq"])
    daily = [n for n, seq in order.items()
             if "NDLS" in seq and "BCT" in seq and seq["NDLS"] < seq["BCT"]
             and len(trains[n]["runs_on"].split()) == 7]
    assert len(daily) >= 2


def test_scale_set_starts_with_the_normal_set(seed, tmp_path):
    result = subprocess.run([sys.executable, str(HERE / "make_seed.py"), "--trains", "1000",
                             "--out-dir", str(tmp_path)], check=True, capture_output=True, text=True)
    assert str(tmp_path) in result.stdout, "the script prints where it wrote the files"
    big = (tmp_path / "trains.csv").read_text(encoding="utf-8").splitlines()
    normal = (seed / "trains.csv").read_text(encoding="utf-8").splitlines()
    assert len(big) == 1001
    assert big[:len(normal)] == normal
    numbers = [line.split(",")[0] for line in big[1:]]
    assert len(numbers) == len(set(numbers))


def test_scale_option_makes_ten_thousand_trains(tmp_path):
    result = subprocess.run([sys.executable, str(HERE / "make_seed.py"), "--scale", "--out-dir", str(tmp_path)],
                            check=True, capture_output=True, text=True)
    assert "10,000 trains" in result.stdout
    for name in FILES:
        assert str(tmp_path / name) in result.stdout
    assert len((tmp_path / "trains.csv").read_text(encoding="utf-8").splitlines()) == 10_001
    total_bytes = sum((tmp_path / name).stat().st_size for name in FILES)
    assert total_bytes < 10_000_000, "the scale set stays small enough to load in minutes"
