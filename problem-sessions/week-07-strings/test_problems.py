"""Tests for the week 7 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

from itertools import combinations

import pytest

from problems import is_palindrome, look_alike_groups

# 9,000 characters. Without spaces and capitals it is "abab...ab" then "baba...ba".
LONG_LABEL = "Ab " * 1500 + "bA " * 1500

# 1,000 codes: 500 different three-letter codes, then each one written backwards.
THREE_LETTER_CODES = ["".join(trio) for trio in combinations("abcdefghijklmnopqrstuvwxyz", 3)][:500]
MANY_CODES = THREE_LETTER_CODES + [code[::-1] for code in THREE_LETTER_CODES]
MANY_GROUPS = [[code, code[::-1]] for code in THREE_LETTER_CODES]


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        pytest.param("Malayalam", True, id="readme-1-capital-letter"),
        pytest.param("Top spot", True, id="readme-2-space"),
        pytest.param("Shortly", False, id="readme-3-not-a-palindrome"),
        pytest.param("", True, id="readme-4-empty-string"),
        pytest.param("a", True, id="one-character"),
        pytest.param("Ab", False, id="two-different-letters"),
        pytest.param("12-21", True, id="digits-and-a-hyphen"),
        pytest.param("Aa-aA", True, id="same-letter-repeated"),
        pytest.param("--- !!", True, id="no-letters-or-digits"),
        pytest.param(LONG_LABEL, True, id="larger-9000-characters"),
    ],
)
def test_is_palindrome(label, expected):
    assert is_palindrome(label) == expected


@pytest.mark.parametrize(
    ("codes", "expected"),
    [
        pytest.param(
            ["ab3k", "pq7r", "k3ba", "r7qp", "zz1"],
            [["ab3k", "k3ba"], ["pq7r", "r7qp"]],
            id="readme-1",
        ),
        pytest.param(
            ["Tea9", "eat9", "ate9", "tan"], [["Tea9", "eat9", "ate9"]], id="readme-2-capitals"
        ),
        pytest.param(["aab", "abb"], [], id="readme-3-counts-differ"),
        pytest.param([], [], id="readme-4-empty-list"),
        pytest.param(["x1y2"], [], id="one-code"),
        pytest.param(["mx9", "mx9", "9xm"], [["mx9", "mx9", "9xm"]], id="same-code-twice"),
        pytest.param(
            ["b1", "a2", "2a", "1b"], [["b1", "1b"], ["a2", "2a"]], id="groups-follow-first-code"
        ),
        pytest.param(["ab", "aba", "ba"], [["ab", "ba"]], id="different-lengths"),
        pytest.param(["ABC", "cba", "Bca"], [["ABC", "cba", "Bca"]], id="mixed-capitals"),
        pytest.param(MANY_CODES, MANY_GROUPS, id="larger-1000-codes"),
    ],
)
def test_look_alike_groups(codes, expected):
    assert look_alike_groups(codes) == expected
