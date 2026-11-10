"""Starter checks: ready-made tests for four functions that you write.

Each check is skipped until its task. When you finish that task, delete the
@pytest.mark.skip line above the check and run `uv run pytest -q`.
They only check results. The tests that your tasks ask for are still yours
to write, in the other test files.
"""

import datetime

import pytest

from paisalens.recurring import is_monthly
from paisalens.report import bar, month_of, rupees


@pytest.mark.skip(reason="TODO(task 9)")
def test_rupees_uses_whole_paise():
    assert rupees(125050) == "₹1,250.50"
    assert rupees(5) == "₹0.05"


@pytest.mark.skip(reason="TODO(task 18)")
def test_month_of_takes_a_date():
    assert month_of(datetime.date(2026, 1, 5)) == "2026-01"
    assert month_of(datetime.date(2026, 10, 31)) == "2026-10"


@pytest.mark.skip(reason="TODO(task 20)")
def test_is_monthly_needs_every_gap_near_a_month():
    assert is_monthly([30, 31, 29])
    assert not is_monthly([30, 12, 31])


@pytest.mark.skip(reason="TODO(task 24)")
def test_bar_gives_the_largest_value_the_full_width():
    assert len(bar(500, 500)) == 30
    assert len(bar(250, 500)) == 15
    assert len(bar(1, 3, width=6)) == 2
    assert bar(0, 0) == ""
