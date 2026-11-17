"""Tests for the week 22 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import best_pay, ways_to_climb

# 2,000 shifts in 400 blocks of [600, 100, 100, 600, 0]. Each block pays at most 1200 (its two 600 shifts).
# The 0 between blocks keeps the 600 shifts of next-door blocks apart, so the best is 400 x 1200.
LONG_DAY = [600, 100, 100, 600, 0] * 400


@pytest.mark.parametrize(
    ("steps", "broken", "expected"),
    [
        pytest.param(4, [], 5, id="readme-1"),
        pytest.param(5, [3], 2, id="readme-2-one-broken-step"),
        pytest.param(3, [1, 2], 0, id="readme-3-two-broken-steps-in-a-row"),
        pytest.param(0, [], 1, id="readme-4-no-steps"),
        pytest.param(1, [], 1, id="one-step"),
        pytest.param(6, [6], 0, id="top-step-broken"),
        pytest.param(2, [1], 1, id="first-step-broken"),
        pytest.param(30, [], 1_346_269, id="larger-30-steps"),
        pytest.param(30, [7, 15, 23], 28_561, id="larger-30-steps-3-broken"),
    ],
)
def test_ways_to_climb(steps, broken, expected):
    before = list(broken)
    assert ways_to_climb(steps, broken) == expected
    assert broken == before, "Do not change the list `broken`."


@pytest.mark.parametrize(
    ("shifts", "expected"),
    [
        pytest.param([300, 500, 450, 200], 750, id="readme-1"),
        pytest.param([500, 600, 500], 1000, id="readme-2-best-shift-first-is-wrong"),
        pytest.param([600, 100, 100, 600], 1200, id="readme-3-skip-two-in-a-row"),
        pytest.param([450], 450, id="readme-4-one-shift"),
        pytest.param([], 0, id="readme-5-no-shifts"),
        pytest.param([0, 0, 0], 0, id="no-pay-at-all"),
        pytest.param([200, 900, 300, 50, 400], 1300, id="five-shifts"),
        pytest.param([700, 800], 800, id="two-shifts"),
        pytest.param(LONG_DAY, 480_000, id="larger-2000-shifts"),
    ],
)
def test_best_pay(shifts, expected):
    before = list(shifts)
    assert best_pay(shifts) == expected
    assert shifts == before, "Do not change the list `shifts`."
