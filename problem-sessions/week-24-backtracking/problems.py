"""Week 24 problem session: backtracking: try, check, undo.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def addon_sets(prices: list[int], voucher: int) -> list[list[int]]:
    """Return every set of add-ons whose prices add up to exactly `voucher`.

    Each price in `prices` is different, and each add-on goes in a set at
    most once. No set may appear twice. The order of the sets, and of the
    prices inside each set, does not matter.

    Return [] when no set matches, and when `prices` is empty.
    Do not change `prices`.
    """
    raise NotImplementedError


def count_seatings(students: list[str], apart: list[tuple[str, str]]) -> int:
    """Return how many ways the students can sit in one row.

    Each pair in `apart` must not sit in neighbouring seats, in either
    order. The first and the last seat are not neighbours.

    Return 1 when `students` is empty. Do not change the lists.
    """
    raise NotImplementedError
