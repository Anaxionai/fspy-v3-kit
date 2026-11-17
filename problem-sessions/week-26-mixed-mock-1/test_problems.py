"""Tests for the week 26 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import count_stretches, slowest_speed

# 2,000 days that switch between +100 and -100, starting with +100.
UP_DOWN = [100, -100] * 1000

# 2,000 days with changes from -100 to 100 paise.
MIXED_DAYS = [(k * 37) % 201 - 100 for k in range(2000)]

# 2,000 videos from 1 to 997 minutes long.
LONG_QUEUE = [(k * 53) % 997 + 1 for k in range(2000)]


@pytest.mark.parametrize(
    ("changes", "target", "expected"),
    [
        pytest.param([300, -300, 300, -300], 0, 4, id="readme-1"),
        pytest.param([500, 200, -200, 700], 700, 3, id="readme-2"),
        pytest.param([100, 100], 300, 0, id="readme-3-no-stretch"),
        pytest.param([], 0, 0, id="readme-4-no-days"),
        pytest.param([250], 250, 1, id="one-day-matches"),
        pytest.param([250], 0, 0, id="one-day-does-not-match"),
        pytest.param([0, 0, 0], 0, 6, id="every-stretch-of-zeros"),
        pytest.param([-100, -200, 300, -300], -300, 3, id="negative-target"),
        pytest.param(UP_DOWN, 0, 1_000_000, id="larger-2000-days-up-and-down"),
        pytest.param(MIXED_DAYS, 150, 5240, id="larger-2000-mixed-days"),
    ],
)
def test_count_stretches(changes, target, expected):
    before = list(changes)
    assert count_stretches(changes, target) == expected
    assert changes == before, "Do not change the list `changes`."


@pytest.mark.parametrize(
    ("videos", "hours", "expected"),
    [
        pytest.param([12, 45, 30, 8], 7, 15, id="readme-1"),
        pytest.param([12, 45, 30, 8], 4, 45, id="readme-2-one-hour-each"),
        pytest.param([12, 45, 30, 8], 100, 1, id="readme-3-plenty-of-time"),
        pytest.param([60], 4, 15, id="readme-4-one-video"),
        pytest.param([], 5, 0, id="readme-5-empty-queue"),
        pytest.param([1], 1, 1, id="one-minute-one-hour"),
        pytest.param([1_000_000], 3, 333_334, id="one-very-long-video"),
        pytest.param([90, 90, 90], 6, 45, id="equal-videos"),
        pytest.param([5, 5], 1_000_000, 1, id="huge-number-of-hours"),
        pytest.param(LONG_QUEUE, 3000, 498, id="larger-2000-videos"),
    ],
)
def test_slowest_speed(videos, hours, expected):
    before = list(videos)
    assert slowest_speed(videos, hours) == expected
    assert videos == before, "Do not change the list `videos`."
