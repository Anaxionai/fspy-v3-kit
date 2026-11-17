"""Tests for the week 11 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import first_train_at_or_after, smallest_busiest_load

# 2,880 departures: two trains leave in every minute of the day.
# The first train at minute 1000 is at position 2000.
TWO_PER_MINUTE = [position // 2 for position in range(2880)]

# 2,000 coaches of 72 passengers and 1,000 TTEs: two coaches each.
LONG_TRAIN = [72] * 2000


@pytest.mark.parametrize(
    ("departures", "arrival", "expected"),
    [
        pytest.param([300, 420, 545, 900, 1310], 500, 2, id="readme-1"),
        pytest.param([300, 420, 420, 900], 420, 1, id="readme-2-first-of-equal-times"),
        pytest.param([300, 420, 545], 1000, -1, id="readme-3-every-train-has-left"),
        pytest.param([], 600, -1, id="readme-4-empty-list"),
        pytest.param([600], 700, -1, id="one-train-already-left"),
        pytest.param([600], 600, 0, id="one-train-leaves-on-arrival"),
        pytest.param([300, 420], 0, 0, id="arrives-before-every-train"),
        pytest.param([500, 500, 500, 500], 500, 0, id="all-trains-at-the-same-minute"),
        pytest.param([100, 500, 500, 500], 200, 1, id="equal-times-after-arrival"),
        pytest.param(TWO_PER_MINUTE, 1000, 2000, id="larger-2880-trains"),
    ],
)
def test_first_train_at_or_after(departures, arrival, expected):
    assert first_train_at_or_after(departures, arrival) == expected


@pytest.mark.parametrize(
    ("passengers", "checkers", "expected"),
    [
        pytest.param([72, 80, 64, 90, 18, 40], 3, 148, id="readme-1"),
        pytest.param([50, 50, 50, 50], 2, 100, id="readme-2-even-split"),
        pytest.param([30, 120, 45], 5, 120, id="readme-3-biggest-coach-alone"),
        pytest.param([], 3, 0, id="readme-4-empty-list"),
        pytest.param([64], 1, 64, id="one-coach"),
        pytest.param([10, 20, 30], 1, 60, id="one-tte-checks-everything"),
        pytest.param([10, 20], 7, 20, id="more-ttes-than-coaches"),
        pytest.param([40, 40, 40, 40, 40, 40], 4, 80, id="equal-coaches"),
        pytest.param([0, 0, 0], 2, 0, id="empty-coaches"),
        pytest.param(LONG_TRAIN, 1000, 144, id="larger-2000-coaches"),
    ],
)
def test_smallest_busiest_load(passengers, checkers, expected):
    assert smallest_busiest_load(passengers, checkers) == expected
