"""Week 26 problem session: mock interview 1.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def count_stretches(changes: list[int], target: int) -> int:
    """Return how many stretches of days add up to exactly `target`.

    `changes` holds the net change in the account for each day, in paise. It
    can be negative or 0. A stretch is one or more days next to each other
    in the list. Count every stretch that matches.

    Return 0 when `changes` is empty. Do not change `changes`.
    """
    raise NotImplementedError


def slowest_speed(videos: list[int], hours: int) -> int:
    """Return the smallest whole-number speed that encodes every video in time.

    `videos` holds the length of each video in minutes. At speed `s`, a video
    of `m` minutes takes `m / s` hours, rounded up to a whole number. The
    encoder works on one video at a time. `hours` is never less than the
    number of videos.

    Return 0 when `videos` is empty. Do not change `videos`.
    """
    raise NotImplementedError
