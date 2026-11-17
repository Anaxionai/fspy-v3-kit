"""Week 19 problem session: depth-first search on graphs, groups and run order.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def count_groups(friends: list[str], shared: list[tuple[str, str]]) -> int:
    """Return how many groups of friends the shared bills make.

    Each pair in `shared` joins two friends, whichever name comes first. Two
    friends are in the same group when a chain of shared bills joins them. A
    friend who shared no bill is a group of one.

    Return 0 when `friends` is empty. Do not change the lists.
    """
    raise NotImplementedError


def run_order(needs: dict[str, list[str]]) -> list[str]:
    """Return an order that runs every job once, after all the jobs it needs.

    `needs` maps each pipeline job to the jobs that must finish before it
    starts. Any order that keeps every rule is correct.

    Raise ValueError when the jobs contain a cycle. A job that needs itself
    is a cycle too. Return [] when `needs` is empty. Do not change `needs`.
    """
    raise NotImplementedError
