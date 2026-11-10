"""Orders: create, read, move through the statuses, and estimate the arrival time.

You design the order document in docs/data-model.md (task 15). Redis channel used here:
  order:{order_id}   pub/sub channel with one order's status changes (task 18)

Your code here will need: json, datetime and UTC, ObjectId (from bson), InvalidId (from bson.errors),
HTTPException (from fastapi), get_db() and get_redis() from app.db, and the functions in riders.py and geo.py.
"""

from datetime import datetime

from app.models import OrderIn, Status

# The state machine: for each status, the only status it may move to next. You met these in P6.
# TODO(task 18): fill it in, for example "placed" -> "picked_up". "delivered" moves nowhere.
NEXT: dict[str, str] = {}


async def create_order(order: OrderIn) -> str:
    """Store a new order and return its id as a string.

    A new order has status "placed" and a timeline with one entry, such as {"status": "placed", "at": ...}.
    TODO(task 15): write it. For now, give it a random rider_id from 1 to 50.
    TODO(task 19): give it the nearest free rider instead: try the nearest free riders to the
      restaurant in order, and claim the first one that works. If no claim works, answer 409
      "No free rider nearby" and save nothing.
    """
    raise NotImplementedError("TODO(task 15): store the order")


async def find_order(order_id: str) -> dict | None:
    """The order as a dict, with its id as the string field "id" (not ObjectId "_id").

    Returns None for an unknown id, and for a malformed one (not 24 hexadecimal characters).
    TODO(task 15): write it.
    """
    raise NotImplementedError("TODO(task 15): read the order")


async def change_status(order_id: str, new_status: Status) -> dict:
    """Move the order to new_status, record it in the timeline, and return the changed order.

    Answers 404 for an unknown order, and 409 unless new_status is NEXT[current status].
    Edge case: two requests for the same change at the same moment must not both succeed,
    so the check and the change must be one database operation.
    TODO(task 18): write it, then call publish_status.
    TODO(task 19): when the order becomes "delivered", make its rider free again.
    """
    raise NotImplementedError("TODO(task 18): change the status with the state machine")


async def publish_status(order_id: str, status: Status, at: datetime) -> None:
    """Publish {"type": "status", "status": ..., "at": ...} as JSON text on the channel order:{order_id}.

    TODO(task 18): write it.
    """
    raise NotImplementedError("TODO(task 18): publish the status change")


async def arrival_estimate(order: dict) -> dict:
    """{"distance_m": ..., "eta_minutes": ...} for an order that is not delivered yet.

    Before pickup, the distance is rider to restaurant plus restaurant to customer.
    After pickup, it is rider to customer. Use the rider's latest position and average speed.
    TODO(task 20): write it with haversine_m, average_speed_kmh and eta_minutes from geo.py.
    """
    raise NotImplementedError("TODO(task 20): estimate the arrival time")
