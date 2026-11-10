"""Keyset pagination for long lists (P10 add-on, task 10).

A page holds `items` and `next_cursor`. The cursor is an opaque string that holds
the last row's `created_at` and `id`; the client sends it back as `after` to get the
next page. The pair is unique even when two bookings share a `created_at`.
"""

from datetime import datetime

from pydantic import BaseModel

from app.schemas import BookingOut


class BookingPage(BaseModel):
    items: list[BookingOut]
    next_cursor: str | None  # None on the last page


def encode_cursor(created_at: datetime, booking_id: int) -> str:
    """Pack the last row's `created_at` and `id` into one URL-safe string (step 4).

    For example base64 of "<ISO time>|<id>". Keep the time zone.
    """
    raise NotImplementedError("TODO(task 10): encode the cursor")


def decode_cursor(cursor: str) -> tuple[datetime, int]:
    """Unpack a cursor made by encode_cursor() (step 4).

    A cursor that is not one of yours raises ValueError: the route answers 400, never 500.
    """
    raise NotImplementedError("TODO(task 10): decode the cursor")
