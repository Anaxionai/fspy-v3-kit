"""Tests for the week 6 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import first_repeat, matching_pair

# 2,001 requests: 2,000 different PNRs, then the 1,000th PNR arrives again.
MANY_PNRS = [f"RS{n:08d}" for n in range(2000)] + ["RS00000999"]

# 2,000 spends: 10, 20, 30 and so on up to 20000 paise.
# Only 19990 + 20000 makes 39990, and they are the last two spends.
MANY_SPENDS = [10 * k for k in range(1, 2001)]


@pytest.mark.parametrize(
    ("pnrs", "expected"),
    [
        pytest.param(
            ["RS4K7Q2M9A", "RS8B1N5T3C", "RS4K7Q2M9A"], "RS4K7Q2M9A", id="readme-1"
        ),
        pytest.param(
            ["RS4K7Q2M9A", "RS8B1N5T3C", "RS8B1N5T3C", "RS4K7Q2M9A"],
            "RS8B1N5T3C",
            id="readme-2-earliest-repeat-wins",
        ),
        pytest.param(
            ["RS4K7Q2M9A", "RS8B1N5T3C", "RS2D6W0Y8E"], "", id="readme-3-no-repeat"
        ),
        pytest.param([], "", id="readme-4-empty-list"),
        pytest.param(["RS4K7Q2M9A"], "", id="one-request"),
        pytest.param(["RS9F3H7J1G", "RS9F3H7J1G"], "RS9F3H7J1G", id="two-same-requests"),
        pytest.param(
            ["RS9F3H7J1G", "RS2D6W0Y8E", "RS9F3H7J1G", "RS9F3H7J1G"],
            "RS9F3H7J1G",
            id="three-copies",
        ),
        pytest.param(
            ["RS1A1A1A1A", "RS2B2B2B2B", "RS3C3C3C3C", "RS2B2B2B2B", "RS1A1A1A1A"],
            "RS2B2B2B2B",
            id="inner-repeat-comes-first",
        ),
        pytest.param(MANY_PNRS, "RS00000999", id="larger-2001-requests"),
    ],
)
def test_first_repeat(pnrs, expected):
    assert first_repeat(pnrs) == expected


@pytest.mark.parametrize(
    ("spends", "payment", "expected"),
    [
        pytest.param([45000, 120000, 65000, 30000], 95000, (2, 3), id="readme-1"),
        pytest.param([20000, 50000, 20000], 40000, (0, 2), id="readme-2-same-amount-twice"),
        pytest.param([50000, 10000], 100000, (-1, -1), id="readme-3-no-spend-counts-twice"),
        pytest.param([], 50000, (-1, -1), id="readme-4-empty-list"),
        pytest.param([50000], 50000, (-1, -1), id="one-spend"),
        pytest.param([30000, 70000], 100000, (0, 1), id="two-spends"),
        pytest.param([15000, 25000, 35000], 100000, (-1, -1), id="no-pair"),
        pytest.param(
            [9000, 9000, 9000, 4000, 7500], 11500, (3, 4), id="repeated-amounts-not-in-answer"
        ),
        pytest.param(
            [1000, 2000, 4000, 8000, 16000, 32000], 33000, (0, 5), id="pair-at-both-ends"
        ),
        pytest.param(MANY_SPENDS, 39990, (1998, 1999), id="larger-2000-spends"),
    ],
)
def test_matching_pair(spends, payment, expected):
    assert matching_pair(spends, payment) == expected
