"""Week 11 problem session: binary search.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def first_train_at_or_after(departures: list[int], arrival: int) -> int:
    """Return the position of the first train that leaves at or after `arrival`.

    `departures` holds minutes after midnight, sorted from earliest to
    latest. Two or more trains can leave at the same minute.

    Return -1 when every train leaves before `arrival`, and for an empty
    list. Write the halving yourself: do not use `bisect`. Do not change
    `departures`.
    """
    raise NotImplementedError


def smallest_busiest_load(passengers: list[int], checkers: int) -> int:
    """Return the smallest possible number of passengers for the busiest TTE.

    `passengers` holds the passengers in each coach, in the train's order.
    Each of the `checkers` TTEs checks one run of neighbouring coaches. No
    coach is split, and a TTE may check no coaches.

    Return 0 for an empty list. Do not change `passengers`.
    """
    raise NotImplementedError
