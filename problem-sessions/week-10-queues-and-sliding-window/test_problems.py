"""Tests for the week 10 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import clicks_in_last_minute, longest_within_limit

# 2,000 clicks, one every second. After the first minute, every count is 60.
ONE_PER_SECOND = list(range(2000))
ONE_PER_SECOND_COUNTS = [min(position + 1, 60) for position in range(2000)]

# 2,000 days of 100 paise each. A limit of 50000 paise fits 500 days.
EVEN_SPENDS = [100] * 2000


@pytest.mark.parametrize(
    ("times", "expected"),
    [
        pytest.param([0, 10, 59, 60, 125], [1, 2, 3, 3, 1], id="readme-1"),
        pytest.param([30, 30, 30], [1, 2, 3], id="readme-2-same-second"),
        pytest.param([0, 100, 200], [1, 1, 1], id="readme-3-far-apart"),
        pytest.param([], [], id="readme-4-empty-list"),
        pytest.param([42], [1], id="one-click"),
        pytest.param([0, 59], [1, 2], id="59-seconds-apart-both-count"),
        pytest.param([0, 60], [1, 1], id="60-seconds-apart-first-has-left"),
        pytest.param([5, 5, 70, 70], [1, 2, 1, 2], id="pairs-in-the-same-second"),
        pytest.param([999_999_999, 1_000_000_000], [1, 2], id="largest-times"),
        pytest.param(ONE_PER_SECOND, ONE_PER_SECOND_COUNTS, id="larger-2000-clicks"),
    ],
)
def test_clicks_in_last_minute(times, expected):
    assert clicks_in_last_minute(times) == expected


@pytest.mark.parametrize(
    ("spends", "limit", "expected"),
    [
        pytest.param(
            [20000, 5000, 15000, 40000, 10000, 10000, 5000], 30000, 3, id="readme-1"
        ),
        pytest.param([1000, 1000, 1000], 5000, 3, id="readme-2-all-days-fit"),
        pytest.param([60000, 75000], 50000, 0, id="readme-3-no-day-fits"),
        pytest.param([], 10000, 0, id="readme-4-empty-list"),
        pytest.param([4000], 5000, 1, id="one-day-fits"),
        pytest.param([6000], 5000, 0, id="one-day-too-dear"),
        pytest.param([0, 0, 500, 0], 0, 2, id="zero-limit-and-zero-days"),
        pytest.param([3000, 3000, 3000, 3000, 3000], 9000, 3, id="same-spend-every-day"),
        pytest.param([1000, 2000, 3000, 50000, 1000], 6000, 3, id="best-run-at-the-start"),
        pytest.param(EVEN_SPENDS, 50000, 500, id="larger-2000-days"),
    ],
)
def test_longest_within_limit(spends, limit, expected):
    assert longest_within_limit(spends, limit) == expected
