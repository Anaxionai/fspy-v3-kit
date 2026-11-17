"""Week 8 problem session: sort with a key, then two pointers.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def departure_order(trains: list[tuple[str, str, int]]) -> list[str]:
    """Return the train numbers in order of departure time, earliest first.

    Each train is a tuple (number, departs, fare). `departs` is a time such
    as "06:20", and `fare` is in paise. When two trains leave at the same
    time, put the lower fare first. When the time and the fare are the same,
    keep the order of `trains`.

    Return [] for an empty list. Do not change `trains`.
    """
    raise NotImplementedError


def best_pair_total(prices: list[int], budget: int) -> int:
    """Return the largest total of two different gifts that fits the budget.

    `prices` holds gift prices in paise. The total must be less than or
    equal to `budget`. Two gifts can have the same price.

    Return -1 when every pair costs more than `budget`, or when the list has
    fewer than two items. Do not change `prices`.
    """
    raise NotImplementedError
