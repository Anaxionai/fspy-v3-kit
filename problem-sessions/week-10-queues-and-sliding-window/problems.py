"""Week 10 problem session: queues and a window that slides.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def clicks_in_last_minute(times: list[int]) -> list[int]:
    """For each click, return how many clicks fall in the 60 seconds ending at it.

    `times` holds the second of each click and never goes down. For a click
    at second t, count that click and the earlier clicks in the list with a
    time from t - 59 to t.

    Return a list of the same length as `times`. Return [] for an empty list.
    Do not change `times`.
    """
    raise NotImplementedError


def longest_within_limit(spends: list[int], limit: int) -> int:
    """Return the number of days in the longest run that stays within `limit`.

    `spends` holds the spending on each day, in paise. A run is one or more
    days next to each other, and its total must be less than or equal to
    `limit`.

    Return 0 when no single day fits, and for an empty list.
    Do not change `spends`.
    """
    raise NotImplementedError
