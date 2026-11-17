"""Tests for the week 12 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import flatten, voucher_choices

# One amount inside 50 levels of folders.
DEEP_FOLDER: list = [42]
for _ in range(49):
    DEEP_FOLDER = [DEEP_FOLDER]

# 1,000 small folders in one big folder: [[0, [1]], [2, [3]], ...] holds 0 to 1999.
WIDE_FOLDER = [[k, [k + 1]] for k in range(0, 2000, 2)]

# 16 vouchers: 1, 2, 4 and so on up to 32768. Only one choice makes 21845.
POWERS_OF_TWO = [2**k for k in range(16)]

# 12 vouchers of 100. Any 3 of them make 300: there are 220 ways to pick 3 of 12.
TWELVE_EQUAL = [100] * 12


@pytest.mark.parametrize(
    ("folder", "expected"),
    [
        pytest.param([12000, [4500, 8000], 30000], [12000, 4500, 8000, 30000], id="readme-1"),
        pytest.param(
            [[1000, [2000, [3000]]], 4000], [1000, 2000, 3000, 4000], id="readme-2-three-levels"
        ),
        pytest.param([[], [[]], 500], [500], id="readme-3-empty-folders"),
        pytest.param([], [], id="readme-4-empty-folder"),
        pytest.param([700], [700], id="one-amount"),
        pytest.param([5, [5, [5]], 5], [5, 5, 5, 5], id="same-amount-repeated"),
        pytest.param([[[[]]]], [], id="only-folders"),
        pytest.param(DEEP_FOLDER, [42], id="50-levels-deep"),
        pytest.param(WIDE_FOLDER, list(range(2000)), id="larger-2000-amounts"),
    ],
)
def test_flatten(folder, expected):
    assert flatten(folder) == expected


def test_flatten_keeps_the_folders():
    folder = [1, [2, [3]]]
    flatten(folder)
    assert folder == [1, [2, [3]]]


@pytest.mark.parametrize(
    ("vouchers", "bill", "expected"),
    [
        pytest.param(
            [500, 1000, 1500, 2000], 2500, [[500, 2000], [1000, 1500]], id="readme-1"
        ),
        pytest.param(
            [1000, 1000, 2000], 2000, [[1000, 1000], [2000]], id="readme-2-same-value-twice"
        ),
        pytest.param([700, 900], 1000, [], id="readme-3-no-choice"),
        pytest.param([], 500, [], id="readme-4-empty-list"),
        pytest.param([2500], 2500, [[2500]], id="one-voucher-fits"),
        pytest.param([2500], 1000, [], id="one-voucher-does-not-fit"),
        pytest.param([1000, 1000, 3000], 1000, [[1000], [1000]], id="equal-vouchers-are-different"),
        pytest.param(
            [100, 200, 300, 400], 500, [[100, 400], [200, 300]], id="two-choices-of-two"
        ),
        pytest.param(
            POWERS_OF_TWO,
            21845,
            [[1, 4, 16, 64, 256, 1024, 4096, 16384]],
            id="larger-16-vouchers",
        ),
        pytest.param(TWELVE_EQUAL, 300, [[100, 100, 100]] * 220, id="larger-220-choices"),
    ],
)
def test_voucher_choices(vouchers, bill, expected):
    assert sorted(voucher_choices(vouchers, bill)) == sorted(expected)
