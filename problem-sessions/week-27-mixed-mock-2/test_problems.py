"""Tests for the week 27 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import cluster_sizes, days_until_cheaper

# 2,001 days. The fare rises from 1000 to 2999 rupees, then drops to 500 on the last day.
RISE_THEN_DROP = list(range(1000, 3000)) + [500]

# 2,000 days at the same fare. No day is cheaper than another.
SAME_FARE = [1800] * 2000

# 20 x 20 blocks, all with orders.
ALL_ORDERS = ["H" * 20] * 20


def three_kinds_of_cluster() -> list[str]:
    """20 x 20 blocks with three kinds of cluster. Column 10 is always empty.

    Columns 0 to 9: full even rows, joined at alternate ends, make one snake of 100 + 9 = 109 blocks.
    Columns 11 to 18, rows 0 to 7: a square of 64 blocks.
    Columns 11 to 19, rows 9 to 19: a chessboard pattern of 50 single blocks that touch only at corners.
    """
    rows = []
    for r in range(20):
        left = ["."] * 10
        if r % 2 == 0 and r <= 18:
            left = ["H"] * 10
        elif r % 2 == 1 and r <= 17:
            left[9 if (r // 2) % 2 == 0 else 0] = "H"
        right = ["."] * 9
        if r <= 7:
            right = ["H"] * 8 + ["."]
        elif r >= 9:
            right = ["H" if (r + c) % 2 == 0 else "." for c in range(11, 20)]
        rows.append("".join(left) + "." + "".join(right))
    return rows


@pytest.mark.parametrize(
    ("fares", "expected"),
    [
        pytest.param([2400, 2100, 2300, 1900, 2000], [1, 2, 1, 0, 0], id="readme-1"),
        pytest.param([1500, 1500, 1400], [2, 1, 0], id="readme-2-equal-is-not-cheaper"),
        pytest.param([1000, 1200, 1300], [0, 0, 0], id="readme-3-never-cheaper"),
        pytest.param([], [], id="readme-4-no-days"),
        pytest.param([999], [0], id="one-day"),
        pytest.param([2500, 2400, 2300, 2200, 2100], [1, 1, 1, 1, 0], id="falling-every-day"),
        pytest.param([3100, 2800, 3500, 3600, 2700, 2900], [1, 3, 2, 1, 0, 0], id="waits-of-different-lengths"),
        pytest.param(RISE_THEN_DROP, [2000 - day for day in range(2000)] + [0], id="larger-2001-days"),
        pytest.param(SAME_FARE, [0] * 2000, id="larger-2000-equal-days"),
    ],
)
def test_days_until_cheaper(fares, expected):
    before = list(fares)
    assert days_until_cheaper(fares) == expected
    assert fares == before, "Do not change the list `fares`."


@pytest.mark.parametrize(
    ("grid", "expected"),
    [
        pytest.param(["HH..", "H..H", "..HH"], [3, 3], id="readme-1"),
        pytest.param(["H.H", ".H.", "H.H"], [1, 1, 1, 1, 1], id="readme-2-corners-do-not-join"),
        pytest.param(["...", "..."], [], id="readme-3-no-orders"),
        pytest.param([], [], id="readme-4-empty-grid"),
        pytest.param(["H"], [1], id="one-block"),
        pytest.param(["HH.HHH"], [3, 2], id="one-row"),
        pytest.param(["HHHHH", "H...H", "H.H.H", "H...H", "HHHHH"], [16, 1], id="ring-around-one-block"),
        pytest.param(ALL_ORDERS, [400], id="larger-all-400-blocks"),
        pytest.param(three_kinds_of_cluster(), [109, 64] + [1] * 50, id="larger-20-by-20-three-kinds"),
    ],
)
def test_cluster_sizes(grid, expected):
    assert cluster_sizes(grid) == expected
