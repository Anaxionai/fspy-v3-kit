"""Week 27 problem session: mock interview 2.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def days_until_cheaper(fares: list[int]) -> list[int]:
    """Return, for each day, how many days you must wait for a lower fare.

    `fares` holds the lowest fare for each day, in rupees. Only a lower fare
    counts, not an equal one. Use 0 for a day when no later day is cheaper.
    The answer has one number for each day.

    Return [] when `fares` is empty. Do not change `fares`.
    """
    raise NotImplementedError


def cluster_sizes(grid: list[str]) -> list[int]:
    """Return the size of every cluster of orders, from largest to smallest.

    Each string in `grid` is one row of blocks: "H" is a block with an order
    and "." is a block without one. Blocks with orders that share a side
    (up, down, left or right) are in the same cluster. Blocks that touch
    only at a corner are not.

    Return [] when the grid is empty or has no orders.
    """
    raise NotImplementedError
