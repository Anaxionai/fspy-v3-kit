"""Request and response models: the shapes of RailSeat's JSON.

Keep these field names: RailSeat web (P4) reads them. You may change a type
to match your own tables; the comments say when.
"""

from datetime import date, datetime

from pydantic import BaseModel


class TrainResult(BaseModel):
    """One journey in the search results of GET /trains/search."""

    journey_id: int
    train_number: str  # use int if your trains table stores the number as an integer
    train_name: str
    departs: datetime  # date and time at the "from" station; use time if your query returns only a time
    arrives: datetime  # date and time at the "to" station
    free_seats: int


class SeatOut(BaseModel):
    """One seat of a journey's train, in GET /journeys/{journey_id}/seats."""

    seat_id: int
    coach: str  # the coach code, such as "B1"
    travel_class: str  # "1A", "2A", "3A", "SL" or "CC"
    number: int  # the seat number in its coach, from 1
    booked: bool  # true when a confirmed booking holds this seat on this journey


class PassengerIn(BaseModel):
    """The passenger in a booking request."""

    # TODO(task 13): use `Field` for a name of 2 to 60 characters and an age of 1 to 120.
    name: str
    age: int


class BookingIn(BaseModel):
    """The body of POST /bookings."""

    # TODO(task 13): add a `json_schema_extra` example with a real journey, seat and passenger.
    journey_id: int
    seat_id: int
    passenger: PassengerIn


class BookingOut(BaseModel):
    """One booking, as POST /bookings, GET /bookings/{pnr} and DELETE /bookings/{pnr} return it."""

    pnr: str  # 10 characters: uppercase letters and digits
    status: str  # "confirmed" or "cancelled"
    journey_id: int
    travel_date: date
    train_number: str  # same type as in TrainResult
    train_name: str
    coach: str
    seat_number: int
    passenger_name: str
