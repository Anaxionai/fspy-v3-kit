"""Week 21 problem session: greedy choices, and why they are safe.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def most_videos(lengths: list[int], free_minutes: int) -> int:
    """Return the largest number of uploads that fit in `free_minutes`.

    `lengths` holds the length of each upload in the ReelPipe queue, in
    minutes. You may pick any uploads, in any order. Their total length must
    be equal to or less than `free_minutes`.

    Return 0 when `lengths` is empty. Do not change `lengths`.
    """
    raise NotImplementedError


def most_bookings(requests: list[tuple[int, int]]) -> int:
    """Return the largest number of requests the retiring room can accept.

    Each request is (start, end) in hours after Monday 00:00. The room takes
    one guest at a time. Two requests overlap when one starts before the
    other ends. Touching requests do not overlap.

    Return 0 when `requests` is empty. Do not change `requests`.
    """
    raise NotImplementedError
