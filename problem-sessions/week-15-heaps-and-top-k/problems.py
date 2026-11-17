"""Week 15 problem session: heaps and the top k.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def give_seats(seat_count: int, requests: list[int]) -> list[int]:
    """Return the seat given to each booking, in order.

    Seats are numbered from 1 to `seat_count`, and all are free at the
    start. A request of 0 is a booking: give it the lowest free seat, or -1
    when no seat is free. Any other request is a cancelled seat, which is
    free again. Cancellations add nothing to the answer.

    Do not change `requests`.
    """
    raise NotImplementedError


def top_links(clicks: list[str], k: int) -> list[str]:
    """Return the `k` codes with the most clicks, most clicks first.

    `clicks` has one short code for each click. When two codes have the
    same number of clicks, the code that comes first in alphabetical order
    goes first.

    Return fewer than `k` codes when there are fewer different codes.
    Return [] for an empty list. Do not change `clicks`.
    """
    raise NotImplementedError
