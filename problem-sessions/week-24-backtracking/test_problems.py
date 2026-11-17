"""Tests for the week 24 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import addon_sets, count_seatings

# 16 add-ons priced 10, 20, 30 ... 160 rupees. Together they cost 1360.
SIXTEEN_PRICES = [10 * k for k in range(1, 17)]

EIGHT_STUDENTS = ["Aarav", "Bhavna", "Chetan", "Deepa", "Farhan", "Gauri", "Harsh", "Ishita"]
SIX_PAIRS = [
    ("Aarav", "Bhavna"),
    ("Chetan", "Deepa"),
    ("Farhan", "Gauri"),
    ("Harsh", "Ishita"),
    ("Aarav", "Chetan"),
    ("Deepa", "Farhan"),
]


def sorted_sets(sets: list[list[int]]) -> list[list[int]]:
    """Sort the prices inside each set, then sort the sets, so that the order does not matter."""
    return sorted(sorted(prices) for prices in sets)


@pytest.mark.parametrize(
    ("prices", "voucher", "expected"),
    [
        pytest.param([20, 30, 50, 70], 100, [[20, 30, 50], [30, 70]], id="readme-1"),
        pytest.param([40, 60, 25], 100, [[40, 60]], id="readme-2-one-set"),
        pytest.param([10, 20, 30, 40], 50, [[10, 40], [20, 30]], id="readme-3-two-sets"),
        pytest.param([15, 25], 30, [], id="readme-4-no-add-on-twice"),
        pytest.param([], 50, [], id="readme-5-no-add-ons"),
        pytest.param([35], 35, [[35]], id="one-add-on-matches"),
        pytest.param([35], 40, [], id="one-add-on-does-not-match"),
        pytest.param([120, 80, 45, 55, 100], 200, [[45, 55, 100], [80, 120]], id="unsorted-prices"),
        pytest.param(SIXTEEN_PRICES, 1360, [SIXTEEN_PRICES], id="larger-every-add-on"),
    ],
)
def test_addon_sets(prices, voucher, expected):
    before = list(prices)
    assert sorted_sets(addon_sets(prices, voucher)) == expected
    assert prices == before, "Do not change the list `prices`."


def test_addon_sets_larger_1314_sets():
    # 1,314 of the 65,536 possible sets of the 16 add-ons cost exactly 680.
    result = sorted_sets(addon_sets(SIXTEEN_PRICES, 680))
    for chosen in result:
        assert sum(chosen) == 680, f"{chosen} does not add up to 680."
        assert len(set(chosen)) == len(chosen), f"{chosen} uses an add-on twice."
        assert set(chosen) <= set(SIXTEEN_PRICES), f"{chosen} uses a price that is not on the list."
    assert len({tuple(chosen) for chosen in result}) == len(result), "A set appears twice."
    assert len(result) == 1314


@pytest.mark.parametrize(
    ("students", "apart", "expected"),
    [
        pytest.param(["Asha", "Ravi", "Meera"], [("Asha", "Ravi")], 2, id="readme-1"),
        pytest.param(["Asha", "Ravi", "Meera"], [], 6, id="readme-2-no-pairs"),
        pytest.param(
            ["Asha", "Ravi", "Meera"],
            [("Asha", "Ravi"), ("Ravi", "Meera")],
            0,
            id="readme-3-no-seating-works",
        ),
        pytest.param(["Kabir", "Diya", "Arjun", "Isha"], [("Kabir", "Diya")], 12, id="readme-4"),
        pytest.param([], [], 1, id="readme-5-nobody"),
        pytest.param(["Zoya"], [], 1, id="one-student"),
        pytest.param(["Kabir", "Diya"], [("Diya", "Kabir")], 0, id="two-students-kept-apart"),
        pytest.param(
            ["Kabir", "Diya", "Arjun", "Isha"],
            [("Kabir", "Diya"), ("Arjun", "Isha")],
            8,
            id="two-pairs",
        ),
        pytest.param(EIGHT_STUDENTS, [], 40_320, id="larger-8-students-no-pairs"),
        pytest.param(EIGHT_STUDENTS, SIX_PAIRS, 7_052, id="larger-8-students-6-pairs"),
    ],
)
def test_count_seatings(students, apart, expected):
    assert count_seatings(students, apart) == expected
