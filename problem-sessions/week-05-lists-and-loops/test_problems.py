"""Tests for the week 5 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import balls_to_reach, biggest_rise

# 1,800 balls. Every 6 balls add 16 runs, so 250 groups of 6 balls add 4,000 runs.
LONG_CHASE = [0, 1, 2, 3, 4, 6] * 300

# 1,800 days. The balance falls from 1500 to 501, drops to 0, then rises to 799.
FALL_THEN_RISE = list(range(1500, 500, -1)) + list(range(0, 800))


@pytest.mark.parametrize(
    ("runs", "target", "expected"),
    [
        pytest.param([1, 4, 0, 6, 2], 10, 4, id="readme-1-passes-the-target"),
        pytest.param([4, 6], 10, 2, id="readme-2-exactly-the-target"),
        pytest.param([0, 1, 2, 0], 7, -1, id="readme-3-never-reaches"),
        pytest.param([], 5, -1, id="readme-4-empty-list"),
        pytest.param([6], 5, 1, id="one-ball-reaches"),
        pytest.param([3], 5, -1, id="one-ball-falls-short"),
        pytest.param([2, 2, 2, 2, 2], 6, 3, id="same-runs-every-ball"),
        pytest.param([1, 1, 1], 3, 3, id="reaches-on-the-last-ball"),
        pytest.param([0, 0, 0, 4], 1, 4, id="dot-balls-first"),
        pytest.param(LONG_CHASE, 4000, 1500, id="larger-1800-balls"),
    ],
)
def test_balls_to_reach(runs, target, expected):
    assert balls_to_reach(runs, target) == expected


@pytest.mark.parametrize(
    ("balances", "expected"),
    [
        pytest.param([50000, 42000, 61000, 39000, 55000], 19000, id="readme-1"),
        pytest.param([80000, 30000, 45000, 20000], 15000, id="readme-2-highest-comes-first"),
        pytest.param([90000, 70000, 70000, 10000], 0, id="readme-3-never-rises"),
        pytest.param([], 0, id="readme-4-empty-list"),
        pytest.param([500], 0, id="one-day"),
        pytest.param([100, 250], 150, id="two-days"),
        pytest.param([700, 700, 700, 700, 700], 0, id="same-balance-every-day"),
        pytest.param([500, 800, 100], 300, id="lowest-day-is-last"),
        pytest.param([300, 900, 100, 650], 600, id="two-rises-first-is-bigger"),
        pytest.param(FALL_THEN_RISE, 799, id="larger-1800-days"),
    ],
)
def test_biggest_rise(balances, expected):
    assert biggest_rise(balances) == expected
