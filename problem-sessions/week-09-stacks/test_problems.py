"""Tests for the week 9 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import brackets_match, overs_until_bigger

# 9,000 characters: 4,500 brackets open, then all of them close in the right order.
DEEP_RULE = "([{" * 1500 + "}])" * 1500

# 2,000 overs: 1,999 overs of 5 runs, then one over of 6 runs.
FLAT_THEN_BIGGER = [5] * 1999 + [6]
FLAT_THEN_BIGGER_ANSWER = [1999 - position for position in range(1999)] + [0]


@pytest.mark.parametrize(
    ("rule", "expected"),
    [
        pytest.param("(food or [travel and {rail}])", True, id="readme-1"),
        pytest.param("(food or [travel)]", False, id="readme-2-wrong-order"),
        pytest.param("((dinner)", False, id="readme-3-never-closes"),
        pytest.param("", True, id="readme-4-empty-string"),
        pytest.param("(", False, id="one-opening-bracket"),
        pytest.param("]", False, id="one-closing-bracket"),
        pytest.param("{{[[(())]]}}", True, id="same-kinds-nested"),
        pytest.param(")(", False, id="closes-before-it-opens"),
        pytest.param("no brackets here", True, id="no-brackets"),
        pytest.param(DEEP_RULE, True, id="larger-9000-characters"),
    ],
)
def test_brackets_match(rule, expected):
    assert brackets_match(rule) == expected


@pytest.mark.parametrize(
    ("runs", "expected"),
    [
        pytest.param([6, 4, 9, 3, 2, 12], [2, 1, 3, 2, 1, 0], id="readme-1"),
        pytest.param([8, 8, 10], [2, 1, 0], id="readme-2-equal-is-not-bigger"),
        pytest.param([15, 11, 7], [0, 0, 0], id="readme-3-never-bigger"),
        pytest.param([], [], id="readme-4-empty-list"),
        pytest.param([7], [0], id="one-over"),
        pytest.param([5, 5, 5, 5], [0, 0, 0, 0], id="all-overs-equal"),
        pytest.param([1, 2, 3, 4], [1, 1, 1, 0], id="every-over-bigger"),
        pytest.param([10, 2, 3, 1, 11], [4, 1, 2, 1, 0], id="valley"),
        pytest.param([9, 1, 1, 1, 10], [4, 3, 2, 1, 0], id="repeated-small-overs"),
        pytest.param(FLAT_THEN_BIGGER, FLAT_THEN_BIGGER_ANSWER, id="larger-2000-overs"),
    ],
)
def test_overs_until_bigger(runs, expected):
    assert overs_until_bigger(runs) == expected
