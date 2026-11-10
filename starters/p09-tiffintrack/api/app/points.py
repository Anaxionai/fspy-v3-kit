"""What happens to a GPS point after the API accepts it. post_point() in main.py calls these.

Redis names used here:
  rider:{rider_id}   pub/sub channel with one rider's live points (task 8)
  riders:last_seq    the highest seq seen for each rider (task 9)
  riders:latest      the latest point message of each rider (task 9)

Your code here will need: json, get_redis() and get_db() from app.db,
and DuplicateKeyError from pymongo.errors (task 16).
"""

from app.models import Point


def point_message(rider_id: int, point: Point) -> dict:
    """The message for one point, as the WebSocket server and the web page expect it:
    {"type": "point", "rider_id": 7, "seq": 1762761600, "lat": 18.52, "lng": 73.85, "ts": "..."}
    Send it as text with json.dumps(...).
    """
    return {
        "type": "point",
        "rider_id": rider_id,
        "seq": point.seq,
        "lat": point.lat,
        "lng": point.lng,
        "ts": point.ts.isoformat(),
    }


async def publish_point(rider_id: int, point: Point) -> None:
    """Publish the point's message, as JSON text, on the Redis channel rider:{rider_id}.

    Every WebSocket server that listens to rider:* receives it, however many there are.
    TODO(task 8): write it. Check it with PSUBSCRIBE rider:* in redis-cli while the simulator runs.
    """
    raise NotImplementedError("TODO(task 8): publish the point on rider:{rider_id}")


async def is_new_point(rider_id: int, seq: int) -> bool:
    """True only if `seq` is higher than every seq this rider sent before; False for a repeat or an old point.

    Edge case: copies of one point can arrive at the same moment, in one API process or in two.
    Exactly one copy may get True. tests/test_duplicates.py checks this.
    TODO(task 9): first write it the simple way from the brief, and watch the test fail.
      Then make the check and the update one atomic Redis operation on riders:last_seq.
    """
    raise NotImplementedError("TODO(task 9): decide whether this point is new")


async def remember_latest(rider_id: int, point: Point) -> None:
    """Keep the point's message as this rider's latest, in the Redis hash riders:latest.

    The WebSocket server sends these to a browser that has just connected (task 9).
    TODO(task 9): write it. Call it for new points only.
    """
    raise NotImplementedError("TODO(task 9): save the rider's latest point")


async def store_point(rider_id: int, point: Point) -> bool:
    """Insert the point into the points collection. Return True if stored, False if it was a copy.

    Store rider_id, seq, ts and location as a GeoJSON point, longitude first:
    {"type": "Point", "coordinates": [lng, lat]}. Store late points too: the route keeps them all.
    Edge case: an exact copy breaks the unique (rider_id, seq) index. That is a dropped copy, not an error.
    TODO(task 16): write it.
    """
    raise NotImplementedError("TODO(task 16): store the point in MongoDB")


async def update_rider(rider_id: int, point: Point) -> None:
    """Keep this rider's latest position in the riders collection, one document per rider.

    The document's _id is the rider id. It holds location (GeoJSON, as in store_point), last_seq
    and updated_at, and a rider seen for the first time starts with status "free".
    TODO(task 16): write it as one upsert. Call it for new points only.
    """
    raise NotImplementedError("TODO(task 16): upsert the rider's latest position")
