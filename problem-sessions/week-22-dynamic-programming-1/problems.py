"""Week 22 problem session: dynamic programming in one dimension.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def ways_to_climb(steps: int, broken: list[int]) -> int:
    """Return how many ways the porter can climb to the top step.

    He starts on the ground (step 0) and climbs one or two steps at a time.
    He must never stand on a step listed in `broken`. The top step is
    `steps`.

    Return 0 when the top step is broken. Return 1 when `steps` is 0.
    Do not change `broken`.
    """
    raise NotImplementedError


def best_pay(shifts: list[int]) -> int:
    """Return the most pay the rider can earn without two neighbouring shifts.

    `shifts` holds the pay for each shift today, in order, in rupees. Two
    shifts are neighbours when they sit next to each other in the list.

    Return 0 when `shifts` is empty. Do not change `shifts`.
    """
    raise NotImplementedError
