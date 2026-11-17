"""Tests for the week 23 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import count_routes, edit_distance

# 12 x 12 junctions with 10 closed.
HINJEWADI_12 = [
    "............",
    "...#........",
    "........#...",
    ".....#......",
    "............",
    "..#.......#.",
    "............",
    "......#.....",
    "...........#",
    ".#..........",
    "....#.......",
    "............",
]

# 180 letters each. Every "r" in TYPED_LONG is an "x" in NAME_LONG: 30 changes.
# "x" never appears in TYPED_LONG, so each of the 30 needs at least one edit.
TYPED_LONG = "nagpur" * 30
NAME_LONG = "nagpux" * 30


@pytest.mark.parametrize(
    ("grid", "expected"),
    [
        pytest.param(["...", "...", "..."], 6, id="readme-1-all-open"),
        pytest.param(["...", ".#.", "..."], 2, id="readme-2-closed-middle"),
        pytest.param(["..#.", "....", "#...", "...."], 12, id="readme-3"),
        pytest.param(["#..", "...", "..."], 0, id="readme-4-start-closed"),
        pytest.param([], 0, id="readme-5-empty-grid"),
        pytest.param(["."], 1, id="one-junction"),
        pytest.param(["...", "...", "..#"], 0, id="end-closed"),
        pytest.param(["..#..."], 0, id="one-row-with-a-closed-junction"),
        pytest.param(["..#", ".#.", "#.."], 0, id="wall-across-the-grid"),
        pytest.param(HINJEWADI_12, 180_465, id="larger-12-by-12"),
    ],
)
def test_count_routes(grid, expected):
    assert count_routes(grid) == expected


@pytest.mark.parametrize(
    ("typed", "name", "expected"),
    [
        pytest.param("bhopl", "bhopal", 1, id="readme-1-add"),
        pytest.param("nagpure", "nagpur", 1, id="readme-2-remove"),
        pytest.param("kanpur", "jaipur", 2, id="readme-3-change-two"),
        pytest.param("madgaon", "margao", 2, id="readme-4-change-and-remove"),
        pytest.param("pune", "pune", 0, id="readme-5-same-name"),
        pytest.param("", "agra", 4, id="readme-6-nothing-typed"),
        pytest.param("vasco", "", 5, id="empty-name"),
        pytest.param("a", "b", 1, id="one-letter-each"),
        pytest.param(
            "chhatrapati shivaji maharaj terminus",
            "chatrapati shivaji terminus",
            9,
            id="with-spaces",
        ),
        pytest.param(TYPED_LONG, NAME_LONG, 30, id="larger-180-letters"),
    ],
)
def test_edit_distance(typed, name, expected):
    assert edit_distance(typed, name) == expected
