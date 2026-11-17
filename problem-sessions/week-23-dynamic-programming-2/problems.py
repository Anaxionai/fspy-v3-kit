"""Week 23 problem session: dynamic programming with two-dimensional tables.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def count_routes(grid: list[str]) -> int:
    """Return how many routes go from the top-left to the bottom-right junction.

    Each string in `grid` is one row: "." is an open junction and "#" is a
    closed one. The rider moves only right or down and never enters a
    closed junction.

    Return 0 when `grid` is empty, or when the first or the last junction is
    closed.
    """
    raise NotImplementedError


def edit_distance(typed: str, name: str) -> int:
    """Return the fewest edits that turn `typed` into `name`.

    One edit adds a letter, removes a letter or changes one letter into
    another. A space counts as a letter.

    Return len(name) when `typed` is empty, and len(typed) when `name` is
    empty.
    """
    raise NotImplementedError
