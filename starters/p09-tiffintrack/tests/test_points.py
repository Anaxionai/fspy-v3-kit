"""Points in MongoDB (task 16). Needs the cloud lab with Redis and MongoDB.

Use a rider id above 900 and seq=int(time.time() * 1000), so the simulator's riders
and earlier test runs do not get in the way.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 16)")
async def test_a_point_is_stored_longitude_first(client, db):
    """Post one point, then find it in db.points: location.coordinates is [lng, lat]."""
    raise NotImplementedError("TODO(task 16): check the coordinate order")


@pytest.mark.skip(reason="TODO(task 16)")
async def test_the_same_point_twice_is_stored_once(client, db):
    """Post the same point twice: db.points has one document for that rider and seq."""
    raise NotImplementedError("TODO(task 16): check that a copy is stored once")
