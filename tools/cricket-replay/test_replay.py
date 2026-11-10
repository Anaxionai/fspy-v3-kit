"""Tests for replay.py, using synthetic_match.json (a made-up match, not Cricsheet data).

Run them from this folder with either command:

    uv run --with pytest pytest -q
    python -m pytest -q

The tests never use the internet.
"""

import json
import subprocess
import sys
import threading
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pytest

import replay

HERE = Path(__file__).parent
SYNTHETIC = json.loads((HERE / "synthetic_match.json").read_text(encoding="utf-8"))


@pytest.fixture
def match():
    return replay.load_match(SYNTHETIC, "synthetic", 2.0)


class FakeClock:
    """A clock the test moves by hand, so no test has to wait."""

    def __init__(self) -> None:
        self.now = 100.0

    def __call__(self) -> float:
        return self.now


def test_match_is_read(match):
    assert len(match.deliveries) == 23
    assert [i["team"] for i in match.innings] == ["Pune Peacocks", "Chennai Comets"]
    assert match.meta["teams"] == ["Pune Peacocks", "Chennai Comets"]
    assert match.meta["venue"] == "Kit Test Ground, Pune"
    assert match.meta["date"] == "2026-11-01"
    assert "Cricsheet" in match.meta["source"] and "Attribution" in match.meta["licence"]


def test_fresh_start_has_zero_balls(match):
    state = replay.live_state(match, 0)
    assert state["status"] == "not started"
    assert state["innings"] == [{"number": 1, "team": "Pune Peacocks", "balls": []}]


def test_balls_are_raw_and_grouped_by_innings(match):
    state = replay.live_state(match, 16)  # 14 balls of innings 1 and 2 of innings 2
    assert state["status"] == "live"
    assert set(state) == {"match_id", "status", "innings"}, "no totals at the top level"
    first, second = state["innings"]
    assert set(first) == {"number", "team", "balls"}, "no totals in an innings"
    assert len(first["balls"]) == 14 and len(second["balls"]) == 2
    ball = first["balls"][1]
    assert ball == {"over": 0, "ball": 2, "batter": "P Opener One", "non_striker": "P Opener Two",
                    "bowler": "C Bowler One", "runs": {"batter": 4, "extras": 0, "total": 4}}


def test_extras_wickets_and_ball_numbers(match):
    balls = replay.live_state(match, 14)["innings"][0]["balls"]
    wide, after_wide = balls[2], balls[3]
    assert wide["extras"] == {"wides": 1} and (wide["over"], wide["ball"]) == (0, 3)
    assert (after_wide["over"], after_wide["ball"]) == (0, 3), "a wide does not move the ball number on"
    assert "extras" not in after_wide and "wicket" not in after_wide
    assert balls[5]["wicket"] == {"player_out": "P Opener Two", "kind": "caught", "fielders": ["C Opener Two"]}
    assert balls[10]["wicket"] == {"player_out": "P Opener One", "kind": "bowled"}
    assert balls[9]["runs"]["non_boundary"] is True
    assert balls[8]["extras"] == {"noballs": 1}


def test_finished_match(match):
    state = replay.live_state(match, 23)
    assert state["status"] == "finished"
    assert state["innings"][1]["balls"][4]["wicket"] == {"player_out": "C Opener One", "kind": "run out",
                                                     "fielders": ["P Batter Three"]}
    assert replay.live_state(match, 99) == state  # never more than the whole match


def test_ball_numbers_without_actual_delivery():
    """Older Cricsheet files have no "actual_delivery", so the script counts legal balls."""
    deliveries = [{}, {"extras": {"wides": 1}}, {}, {"extras": {"noballs": 1}}, {}, {}, {}, {}]
    assert replay.ball_numbers(deliveries) == [1, 2, 2, 3, 3, 4, 5, 6]


def test_super_over_flag_is_passed_on():
    data = json.loads(json.dumps(SYNTHETIC))
    data["innings"][1]["super_over"] = True
    match = replay.load_match(data, "x")
    assert match.innings[1] == {"number": 2, "team": "Chennai Comets", "super_over": True}


def test_start_point(match):
    assert replay.start_index(match, 1, 0) == 0
    assert replay.start_index(match, 1, 1) == 7, "over 1 starts after the 7 deliveries of over 0"
    assert replay.start_index(match, 2, 0) == 14
    assert replay.start_index(match, 2, 1) == 21
    assert replay.start_index(match, 1, 5) == 14, "an over past the end starts at the next innings"
    with pytest.raises(replay.ReplayError):
        replay.start_index(match, 3, 0)


def test_clock_adds_one_ball_per_interval(match):
    clock = FakeClock()
    feed = replay.Replay(match, seconds_per_ball=2.0, start_count=0, clock=clock)
    assert feed.shown() == 0
    clock.now += 1.9
    assert feed.shown() == 0
    clock.now += 0.1
    assert feed.shown() == 1
    clock.now += 2 * 30
    assert feed.shown() == 23
    later = replay.Replay(match, seconds_per_ball=0.5, start_count=7, clock=clock)
    clock.now += 1.0
    assert later.shown() == 9


@pytest.fixture
def server(match):
    feed = replay.Replay(match, seconds_per_ball=0.05)
    httpd = replay.serve(feed, "127.0.0.1", 0, quiet=True)  # port 0: any free port
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    httpd.server_close()


def fetch(url: str, method: str = "GET", headers: dict | None = None):
    request = urllib.request.Request(url, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.headers, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.headers, error.read()


def test_http_live_and_meta(server):
    status, headers, body = fetch(server + "/live", headers={"Origin": "http://localhost:5173"})
    assert status == 200
    assert headers["Access-Control-Allow-Origin"] == "*"
    assert headers["Content-Type"].startswith("application/json")
    assert headers["Cache-Control"] == "no-store"
    assert json.loads(body)["match_id"] == "synthetic"
    status, headers, body = fetch(server + "/meta", headers={"Origin": "https://asha.github.io"})
    assert status == 200 and headers["Access-Control-Allow-Origin"] == "*"
    assert json.loads(body)["teams"] == ["Pune Peacocks", "Chennai Comets"]


def test_http_preflight_and_private_network(server):
    status, headers, _ = fetch(server + "/live", "OPTIONS", {
        "Origin": "https://asha.github.io",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Private-Network": "true",
    })
    assert status == 204
    assert headers["Access-Control-Allow-Origin"] == "*"
    assert headers["Access-Control-Allow-Private-Network"] == "true"
    status, headers, _ = fetch(server + "/live", "OPTIONS", {"Origin": "http://localhost:5173"})
    assert status == 204 and "Access-Control-Allow-Private-Network" not in headers


def test_http_unknown_page(server):
    status, headers, body = fetch(server + "/score")
    assert status == 404 and headers["Access-Control-Allow-Origin"] == "*"
    assert json.loads(body)["endpoints"] == ["/live", "/meta"]


def test_http_balls_arrive_over_time(server):
    first = json.loads(fetch(server + "/live")[2])
    assert first["status"] in ("not started", "live")
    import time
    time.sleep(0.3)
    later = json.loads(fetch(server + "/live")[2])
    assert sum(len(i["balls"]) for i in later["innings"]) > sum(len(i["balls"]) for i in first["innings"])


@pytest.fixture
def archive(tmp_path) -> Path:
    """A small zip shaped like Cricsheet's IPL archive, holding the synthetic match as 999001."""
    path = tmp_path / "ipl_json.zip"
    readme = ("The matches contained in this zip archive are listed below.\n\n"
              "2026-11-01 - club - IPL - male - 999001 - Pune Peacocks vs Chennai Comets\n"
              "2025-04-02 - club - IPL - male - 999000 - Kolkata Kites vs Mumbai Mangoes\n")
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("README.txt", readme)
        zf.writestr("999001.json", json.dumps(SYNTHETIC))
    return path


def test_archive_list_and_read(archive):
    assert replay.list_matches(archive) == [("999001", "2026-11-01", "Pune Peacocks vs Chennai Comets"),
                                            ("999000", "2025-04-02", "Kolkata Kites vs Mumbai Mangoes")]
    assert [m[0] for m in replay.list_matches(archive, season="2025")] == ["999000"]
    assert [m[0] for m in replay.list_matches(archive, team="peacocks")] == ["999001"]
    assert replay.read_from_archive(archive, "999001")["info"]["venue"] == "Kit Test Ground, Pune"
    with pytest.raises(replay.ReplayError, match="not in the IPL archive"):
        replay.read_from_archive(archive, "123")
    with pytest.raises(replay.ReplayError, match="is a number"):
        replay.read_from_archive(archive, "../etc/passwd")


def test_cached_archive_is_not_downloaded_again(archive, monkeypatch):
    def no_internet(*args, **kwargs):
        raise AssertionError("the test tried to use the internet")
    monkeypatch.setattr(replay.urllib.request, "urlopen", no_internet)
    assert replay.download_archive(archive.parent) == archive


def test_command_line_list(archive):
    result = subprocess.run([sys.executable, str(HERE / "replay.py"), "--list", "--cache-dir", str(archive.parent)],
                            capture_output=True, text=True, check=True)
    assert "999001  2026-11-01  Pune Peacocks vs Chennai Comets" in result.stdout


def test_command_line_reports_a_wrong_id(archive):
    result = subprocess.run([sys.executable, str(HERE / "replay.py"), "--match", "42", "--cache-dir",
                             str(archive.parent)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "not in the IPL archive" in result.stderr
