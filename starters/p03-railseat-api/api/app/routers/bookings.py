"""Bookings by PNR: POST /bookings, GET /bookings/{pnr} and DELETE /bookings/{pnr}.

The rules live in app/services/booking.py. These routes call them and turn
their exceptions into HTTP status codes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import BookingIn, BookingOut

router = APIRouter(tags=["bookings"])


# TODO(task 13): add `responses={404: {...}, 409: {...}}` to this decorator,
#   with a description of each, so /docs shows both errors.
@router.post("/bookings", status_code=201)
async def create_booking(
    data: BookingIn,
    session: AsyncSession = Depends(get_session),
) -> BookingOut:
    """Book a free seat for a passenger, and answer 201 with the new booking.

    TODO(task 11): call `book_seat`. Turn its NotFound (unknown journey or
    seat) into HTTP 404, and its SeatTaken into HTTP 409, each with a clear
    `detail` message.
    """
    raise NotImplementedError("TODO(task 11): book the seat")


@router.get("/bookings/{pnr}")
async def read_booking(
    pnr: str,
    session: AsyncSession = Depends(get_session),
) -> BookingOut:
    """Return the booking with this PNR.

    TODO(task 11): call `get_booking`, and turn NotFound into HTTP 404.
    """
    raise NotImplementedError("TODO(task 11): read the booking")


@router.delete("/bookings/{pnr}")
async def delete_booking(
    pnr: str,
    session: AsyncSession = Depends(get_session),
) -> BookingOut:
    """Cancel the booking and answer 200 with it. RailSeat web reads its journey_id.

    TODO(task 11): call `cancel_booking`. Turn NotFound into HTTP 404, and
    AlreadyCancelled (a second cancel) into HTTP 409.
    """
    raise NotImplementedError("TODO(task 11): cancel the booking")
