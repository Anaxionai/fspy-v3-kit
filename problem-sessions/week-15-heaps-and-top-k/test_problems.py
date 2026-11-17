"""Tests for the week 15 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import give_seats, top_links

# 2,003 requests in a coach of 2,000 seats: fill every seat, cancel seat 1500,
# then two more bookings.
FILL_THEN_CANCEL = [0] * 2000 + [1500, 0, 0]
FILL_THEN_CANCEL_SEATS = list(range(1, 2001)) + [1500, -1]

# 5,050 clicks on 100 codes, mixed together. Code c000 has 1 click, c001 has
# 2 clicks, and so on up to c099 with 100 clicks.
MANY_CLICKS = [f"c{i:03d}" for start in range(100) for i in range(start, 100)]
TOP_TEN = [f"c{i:03d}" for i in range(99, 89, -1)]


@pytest.mark.parametrize(
    ("seat_count", "requests", "expected"),
    [
        pytest.param(3, [0, 0, 0], [1, 2, 3], id="readme-1"),
        pytest.param(3, [0, 0, 1, 0, 0], [1, 2, 1, 3], id="readme-2-cancelled-seat-again"),
        pytest.param(1, [0, 0], [1, -1], id="readme-3-coach-full"),
        pytest.param(5, [], [], id="readme-4-no-requests"),
        pytest.param(1, [0, 1, 0], [1, 1], id="one-seat"),
        pytest.param(
            4, [0, 0, 0, 0, 3, 1, 0, 0, 0], [1, 2, 3, 4, 1, 3, -1], id="two-cancelled-seats"
        ),
        pytest.param(2, [0, 0, 2, 0, 2, 0], [1, 2, 2, 2], id="same-seat-again-and-again"),
        pytest.param(2, [0, 0, 0, 0], [1, 2, -1, -1], id="many-bookings-when-full"),
        pytest.param(5, [0, 0, 0, 0, 0, 4, 2, 0, 0], [1, 2, 3, 4, 5, 2, 4], id="lower-seat-first"),
        pytest.param(2000, FILL_THEN_CANCEL, FILL_THEN_CANCEL_SEATS, id="larger-2003-requests"),
    ],
)
def test_give_seats(seat_count, requests, expected):
    assert give_seats(seat_count, requests) == expected


@pytest.mark.parametrize(
    ("clicks", "k", "expected"),
    [
        pytest.param(["dl7", "mb2", "dl7", "ch9", "mb2", "dl7"], 2, ["dl7", "mb2"], id="readme-1"),
        pytest.param(
            ["pq1", "ab3", "pq1", "ab3", "zz9"], 2, ["ab3", "pq1"], id="readme-2-tie-alphabetical"
        ),
        pytest.param(["kl5", "kl5"], 3, ["kl5"], id="readme-3-fewer-codes-than-k"),
        pytest.param([], 10, [], id="readme-4-empty-list"),
        pytest.param(["x1"], 10, ["x1"], id="one-click"),
        pytest.param(["b2", "a1", "b2", "a1"], 1, ["a1"], id="tie-for-the-only-place"),
        pytest.param(["go"] * 5, 1, ["go"], id="one-code-many-clicks"),
        pytest.param(["c", "b", "b", "a", "a", "a"], 3, ["a", "b", "c"], id="three-different-counts"),
        pytest.param(["m", "k", "z", "a"], 4, ["a", "k", "m", "z"], id="all-tied"),
        pytest.param(MANY_CLICKS, 10, TOP_TEN, id="larger-5050-clicks"),
    ],
)
def test_top_links(clicks, k, expected):
    assert top_links(clicks, k) == expected
