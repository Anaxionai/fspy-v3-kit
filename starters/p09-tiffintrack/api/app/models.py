"""The shapes of the data the API receives. Pydantic checks every request body against them."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

# An order moves forwards through these four statuses, one step at a time (task 18).
Status = Literal["placed", "picked_up", "nearby", "delivered"]


class Point(BaseModel):
    """One GPS point from a rider's phone, the body of POST /riders/{rider_id}/points (task 7)."""

    seq: int  # the rider's point number: it grows by 1 with every point
    # TODO(task 7): accept a latitude only from -90 to 90 and a longitude only from -180 to 180,
    #   so that a latitude of 95 gets HTTP 422. tests/test_app.py has a test for it.
    lat: float
    lng: float
    ts: datetime  # when the phone took the point, in UTC


# TODO(task 15): decide what makes an order valid and add the checks to the models below.
#   For example: names and labels are not empty, every lat and lng is in range as in Point,
#   a phone number has 10 digits, a quantity is at least 1, and an order has at least one item.


class Customer(BaseModel):
    """The person who placed the order."""

    name: str
    phone: str


class Restaurant(BaseModel):
    """Where the rider picks the food up."""

    name: str
    lat: float
    lng: float


class Address(BaseModel):
    """Where the rider delivers the food."""

    label: str  # for example "Flat 4B, Karve Road"
    lat: float
    lng: float


class Item(BaseModel):
    """One line of the order. Money is in paise, as a whole number: Rs 90.00 is 9000."""

    name: str
    qty: int
    price_paise: int


class OrderIn(BaseModel):
    """The body of POST /orders (task 15). The API adds the status, the timeline and the rider."""

    customer: Customer
    restaurant: Restaurant
    address: Address
    items: list[Item]


class StatusIn(BaseModel):
    """The body of POST /orders/{order_id}/status, for example {"status": "picked_up"} (task 18)."""

    status: Status
