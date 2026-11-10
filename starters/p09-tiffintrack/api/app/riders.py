"""Finding and claiming riders in the riders collection (task 19), and reading their points (task 20).

A rider document looks like this (task 16 writes it):
  {"_id": 7, "location": {"type": "Point", "coordinates": [lng, lat]},
   "status": "free", "last_seq": 1762761600, "updated_at": ...}
A busy rider also has "order_id".

Your code here will need get_db() from app.db.
"""

from bson import ObjectId

NEAREST_LIMIT = 5  # how many of the nearest free riders an order tries
MAX_DISTANCE_M = 5000  # no rider further than 5 km from the restaurant


async def nearest_free_riders(lat: float, lng: float, limit: int = NEAREST_LIMIT) -> list[dict]:
    """The free riders within MAX_DISTANCE_M of (lat, lng), nearest first, at most `limit` of them.

    Returns rider documents. Returns an empty list when nobody free is in range.
    Edge cases: busy riders never count; GeoJSON puts the longitude first.
    It needs the 2dsphere index on riders.location from task 16.
    TODO(task 19): write the geo query.
    """
    raise NotImplementedError("TODO(task 19): find the nearest free riders")


async def claim_rider(rider_id: int, order_id: ObjectId) -> bool:
    """Make a free rider busy with this order. Return True only if this call claimed the rider.

    Edge case: two orders can try to claim the same rider at the same moment. Only one may win,
    even with two API processes, so the check and the change must be one database operation.
    TODO(task 19): write it.
    """
    raise NotImplementedError("TODO(task 19): claim the rider")


async def free_rider(rider_id: int) -> None:
    """Make the rider free again after their order is delivered: status "free" and no order_id.

    TODO(task 19): write it.
    """
    raise NotImplementedError("TODO(task 19): set the rider free")


async def recent_points(rider_id: int, count: int = 10) -> list[dict]:
    """The rider's last `count` stored points (by seq), oldest first. Fewer if the rider has fewer.

    TODO(task 20): write it.
    """
    raise NotImplementedError("TODO(task 20): read the rider's recent points")
