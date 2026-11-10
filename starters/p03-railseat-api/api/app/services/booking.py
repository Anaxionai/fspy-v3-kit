"""The booking service: RailSeat's rules for booking and cancelling a seat.

The routes in app/routers/bookings.py call these functions. The functions
raise the exceptions below, and the routes turn them into status codes.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import BookingIn, BookingOut


class NotFound(Exception):
    """The journey, the seat or the PNR does not exist (HTTP 404)."""


class SeatTaken(Exception):
    """A confirmed booking already holds this seat on this journey (HTTP 409)."""


class AlreadyCancelled(Exception):
    """The booking was cancelled before (HTTP 409)."""


def new_pnr() -> str:
    """Return a new PNR: 10 characters, each an uppercase letter or a digit.

    TODO(task 11): pick each character with `secrets.choice` from
    `string.ascii_uppercase + string.digits`.
    """
    raise NotImplementedError("TODO(task 11): make a random 10-character PNR")


async def book_seat(session: AsyncSession, data: BookingIn) -> BookingOut:
    """Book seat `data.seat_id` on journey `data.journey_id` for `data.passenger`.

    TODO(task 11): inside one `async with session.begin():` block, before any
    other query in this request,
    - raise NotFound if the journey does not exist;
    - raise NotFound if the seat's coach is not on the journey's train;
    - raise SeatTaken if a confirmed booking already holds the seat on this journey;
    - add a Passenger, and a Booking with status "confirmed" and a new_pnr().
    Return the new booking (get_booking can build it after the commit).

    TODO(task 12): two requests can pass the checks at the same moment. Catch
    `sqlalchemy.exc.IntegrityError` around the transaction and raise SeatTaken,
    so the database's refusal becomes HTTP 409, not 500.
    """
    raise NotImplementedError("TODO(task 11): book the seat in one transaction")


async def cancel_booking(session: AsyncSession, pnr: str) -> BookingOut:
    """Cancel the booking with this PNR, and return it with status "cancelled".

    TODO(task 11): inside one `async with session.begin():` block, set the
    status to "cancelled" and keep the row (P6 refunds need it). Raise
    NotFound for an unknown PNR, and AlreadyCancelled if it was cancelled
    before. Afterwards the seat can be booked again.
    """
    raise NotImplementedError("TODO(task 11): cancel the booking and keep the row")


async def get_booking(session: AsyncSession, pnr: str) -> BookingOut:
    """Return the booking with this PNR, with its train, seat and passenger.

    TODO(task 11): write one query that joins booking, journey, train, seat,
    coach and passenger, and returns the fields of BookingOut. Raise NotFound
    if no booking has this PNR.
    """
    raise NotImplementedError("TODO(task 11): read one booking with one query")
