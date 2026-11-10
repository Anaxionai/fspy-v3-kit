"""Tests for make_statement.py.

Run them from this folder with either command:

    uv run --with pytest pytest -q
    python -m pytest -q
"""

import csv
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pytest

import make_statement

HERE = Path(__file__).parent
SCRIPT = HERE / "make_statement.py"


def run_script(tmp_path: Path, *args: str) -> Path:
    """Run the script the way a student does, and return the CSV it wrote."""
    out = tmp_path / "statement.csv"
    subprocess.run([sys.executable, str(SCRIPT), *args, "--out", str(out)], check=True,
                   capture_output=True, text=True)
    return out


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_amount(text: str) -> Decimal | None:
    """The amount as a Decimal, or None if the text is not a plain number."""
    if not re.fullmatch(r"\d+\.\d{2}", text):
        return None
    return Decimal(text)


def is_real_date(text: str) -> bool:
    try:
        datetime.strptime(text, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def find_broken(rows: list[dict[str, str]]) -> dict[str, list[int]]:
    """Find broken rows the way a student's code should: by reading the data."""
    refs = Counter(row["upi_ref"] for row in rows if row["upi_ref"])
    found: dict[str, list[int]] = {"bad_date": [], "empty_amount": [], "text_amount": [], "duplicate_ref": []}
    seen_refs: set[str] = set()
    for i, row in enumerate(rows):
        if not is_real_date(row["date"]):
            found["bad_date"].append(i)
        if row["debit"] == "" and row["credit"] == "":
            found["empty_amount"].append(i)
        for column in ("debit", "credit"):
            if row[column] and as_amount(row[column]) is None:
                found["text_amount"].append(i)
        ref = row["upi_ref"]
        if ref and refs[ref] > 1 and ref in seen_refs:
            found["duplicate_ref"].append(i)  # the second time we see the reference
        seen_refs.add(ref)
    return found


def test_same_student_gives_the_same_file(tmp_path):
    first = run_script(tmp_path, "--student", "FSPY-0042").read_bytes()
    second = run_script(tmp_path, "--student", "FSPY-0042").read_bytes()
    assert first == second


def test_student_id_ignores_case_and_spaces():
    assert make_statement.generate("fspy-0042") == make_statement.generate("  FSPY-0042 ")


def test_different_students_get_different_files():
    assert make_statement.generate("FSPY-0001")[0] != make_statement.generate("FSPY-0002")[0]


def test_columns(tmp_path):
    path = run_script(tmp_path, "--student", "FSPY-0042", "--months", "2")
    header = path.read_text(encoding="utf-8").splitlines()[0]
    assert header == "date,narration,upi_ref,debit,credit,balance"


def test_sample_file_matches_the_generator(tmp_path):
    """sample-statement.csv in the kit must be what the generator makes today."""
    fresh = run_script(tmp_path, "--student", "SAMPLE", "--months", "2").read_text(encoding="utf-8")
    committed = (HERE / "sample-statement.csv").read_text(encoding="utf-8")
    assert committed.replace("\r\n", "\n") == fresh
    assert 55 <= len(fresh.splitlines()) - 1 <= 70  # about 60 rows


@pytest.mark.parametrize("student", ["SAMPLE", "FSPY-0042", "FSPY-0777", "student-with-a-long-id-123"])
def test_broken_rows_are_present(student):
    rows, broken = make_statement.generate(student, 6)
    dict_rows = [dict(zip(make_statement.HEADER, row)) for row in rows]
    found = find_broken(dict_rows)
    for kind in ("bad_date", "empty_amount", "text_amount", "duplicate_ref"):
        assert found[kind] == [broken[kind]], kind
    assert 3 <= len(broken) <= 5


@pytest.mark.parametrize("student", ["SAMPLE", "FSPY-0042", "FSPY-0777", "FSPY-1234"])
def test_running_balance_is_consistent_except_on_broken_rows(student):
    rows, broken = make_statement.generate(student, 6)
    broken_rows = set(broken.values())
    balances = [as_amount(row[5]) for row in rows]
    assert all(balance is not None for balance in balances), "every balance is a plain number"
    for i in range(1, len(rows)):
        if i in broken_rows:
            continue
        debit = as_amount(rows[i][3] or "0.00")
        credit = as_amount(rows[i][4] or "0.00")
        assert balances[i - 1] - debit + credit == balances[i], f"row {i}: {rows[i]}"


def test_amounts_are_rupees_with_two_decimals():
    rows, broken = make_statement.generate("FSPY-0042", 6)
    for i, row in enumerate(rows):
        for value in (row[3], row[4]):
            if value and i != broken["text_amount"]:
                assert as_amount(value) is not None, row
        assert not (row[3] and row[4]), "a row is a debit or a credit, never both"


def test_months_option_sets_the_period():
    rows, _ = make_statement.generate("FSPY-0042", 3, end_month="2026-10")
    months = set()
    for row in rows:
        if is_real_date(row[0]):
            day = datetime.strptime(row[0], "%d/%m/%Y")
            months.add((day.year, day.month))
    assert months == {(2026, 8), (2026, 9), (2026, 10)}


def test_messy_data_is_there():
    rows, _ = make_statement.generate("FSPY-0042", 6)
    narrations = [row[1] for row in rows]
    text = "\n".join(narrations).upper()
    # At least two narration layouts.
    assert any(n.startswith("UPI/DR/") for n in narrations)
    assert any(n.startswith("UPI-") for n in narrations)
    # Salary, ATM cash, refunds or reversals.
    assert sum("SALARY" in n for n in narrations) == 6
    assert any(n.startswith(("ATW-", "NWD-", "ATM CASH")) for n in narrations)
    assert any("REFUND" in n.upper() or n.startswith("REV-") for n in narrations)
    # Swiggy written in at least two ways.
    swiggy_names = {name for name in ("SWIGGY LIMITED", "BUNDL TECHNOLOGIES", "SWIGGY FOOD") if name in text}
    assert len(swiggy_names) >= 2


def test_subscriptions_come_every_month_with_small_drift():
    rows, _ = make_statement.generate("FSPY-0042", 6)
    patterns = {"netflix": "NETFLIX", "spotify": "SPOTIFY", "airtel": "AIRTEL|BHARTI",
                "gym": "CULT|CUREFIT|IRON ?ZONE"}
    for name, pattern in patterns.items():
        days = [datetime.strptime(row[0], "%d/%m/%Y") for row in rows
                if re.search(pattern, row[1].upper()) and is_real_date(row[0])]
        assert len({(d.year, d.month) for d in days}) == 6, name
        assert max(d.day for d in days) - min(d.day for d in days) <= 4, name


def test_bad_arguments_are_refused(tmp_path):
    result = subprocess.run([sys.executable, str(SCRIPT), "--student", "X", "--months", "0"],
                            capture_output=True, text=True, cwd=tmp_path)
    assert result.returncode != 0
    assert "--months" in result.stderr


def test_never_use_real_data_reminder(tmp_path):
    result = subprocess.run([sys.executable, str(SCRIPT), "--student", "X", "--out", str(tmp_path / "s.csv")],
                            capture_output=True, text=True, check=True)
    assert "Never use your real bank statement" in result.stdout


def test_amount_helper_rejects_text():
    assert as_amount("450.00") == Decimal("450.00")
    assert as_amount("Rs.450/-") is None
    with pytest.raises(InvalidOperation):
        Decimal("Rs.450/-")
