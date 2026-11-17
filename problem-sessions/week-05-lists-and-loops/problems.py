"""Week 5 problem session: one pass over a list.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def balls_to_reach(runs: list[int], target: int) -> int:
    """Return how many balls the team needs to reach `target`.

    `runs` holds the runs from each ball, in order. Each item is from 0 to 6.
    The team reaches the target when its total is equal to or greater than
    `target`.

    Return -1 when the team never reaches the target. An empty list returns -1.
    Do not change `runs`.
    """
    raise NotImplementedError


def biggest_rise(balances: list[int]) -> int:
    """Return the biggest rise in balance from one day to any later day.

    `balances` holds the balance at the end of each day, in paise. A rise
    counts only when the higher balance comes after the lower balance.

    Return 0 when the balance never rises. Return 0 when the list has fewer
    than two items. Do not change `balances`.
    """
    raise NotImplementedError
