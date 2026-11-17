"""Tests for the week 21 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import most_bookings, most_videos

# 3,000 uploads: 1,000 each of 10, 20 and 30 minutes, mixed together.
# 25,000 minutes fit all 1,000 ten-minute uploads (10,000 minutes) and 750 twenty-minute uploads (15,000 minutes).
MIXED_UPLOADS = [10, 30, 20] * 1000

# 2,932 requests. Each request lasts at least 1 hour and the week has 168 hours, so 168 is the most possible.
# The 168 one-hour requests reach that. The other requests last 2, 3, 5, 8, 13 or 168 hours.
ONE_HOUR = [(hour, hour + 1) for hour in range(168)]
LONGER = [(hour, hour + length) for length in (2, 3, 5, 8, 13) for hour in range(168 - length)]
WHOLE_WEEK = [(0, 168)] + (LONGER + ONE_HOUR[::-1]) * 3


@pytest.mark.parametrize(
    ("lengths", "free_minutes", "expected"),
    [
        pytest.param([12, 5, 30, 8], 25, 3, id="readme-1-exact-fit"),
        pytest.param([40, 10, 10, 25], 50, 3, id="readme-2-longest-first-is-worse"),
        pytest.param([60, 45], 30, 0, id="readme-3-nothing-fits"),
        pytest.param([], 100, 0, id="readme-4-empty-queue"),
        pytest.param([15], 15, 1, id="one-upload-fits"),
        pytest.param([15], 14, 0, id="one-upload-too-long"),
        pytest.param([7, 7, 7, 7], 0, 0, id="no-free-minutes"),
        pytest.param([5, 50, 5, 50, 5], 200, 5, id="everything-fits"),
        pytest.param(MIXED_UPLOADS, 25_000, 1750, id="larger-3000-uploads"),
    ],
)
def test_most_videos(lengths, free_minutes, expected):
    before = list(lengths)
    assert most_videos(lengths, free_minutes) == expected
    assert lengths == before, "Do not change the list `lengths`."


@pytest.mark.parametrize(
    ("requests", "expected"),
    [
        pytest.param([(0, 10), (2, 4), (4, 8), (9, 12)], 3, id="readme-1-touching-is-fine"),
        pytest.param([(0, 6), (5, 8), (7, 14)], 2, id="readme-2-shortest-first-is-wrong"),
        pytest.param([(0, 50), (1, 3), (3, 5)], 2, id="readme-3-earliest-start-is-wrong"),
        pytest.param([(20, 30), (5, 25), (28, 40), (30, 36)], 2, id="readme-4"),
        pytest.param([], 0, id="readme-5-empty-list"),
        pytest.param([(10, 20)], 1, id="one-request"),
        pytest.param([(10, 20), (10, 20), (10, 20)], 1, id="same-request-three-times"),
        pytest.param([(0, 168), (0, 1), (167, 168)], 2, id="whole-week-request"),
        pytest.param(WHOLE_WEEK, 168, id="larger-2932-requests"),
    ],
)
def test_most_bookings(requests, expected):
    before = list(requests)
    assert most_bookings(requests) == expected
    assert requests == before, "Do not change the list `requests`."
