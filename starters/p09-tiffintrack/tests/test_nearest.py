"""The nearest free rider (task 19). Needs the cloud lab with Redis and MongoDB.

Put riders north of the order at known distances. 0.001 degrees of latitude is about 111 m,
so a rider 300 m north sits at the order's latitude plus 0.0027.
"""

import pytest

pytestmark = pytest.mark.anyio

ORDER_LAT, ORDER_LNG = 18.5195, 73.8553  # Shaniwar Wada


@pytest.mark.skip(reason="TODO(task 19)")
async def test_the_nearest_free_rider_wins(client, db):
    """Free at 300 m, busy at 100 m, free at 2 km and free at 8 km: GET /riders/nearest
    answers with the 300 m rider."""
    raise NotImplementedError("TODO(task 19): place four riders and ask for the nearest")


@pytest.mark.skip(reason="TODO(task 19)")
async def test_a_busy_rider_is_skipped(client, db):
    """The same riders, but the 300 m rider is busy too: the answer is the 2 km rider."""
    raise NotImplementedError("TODO(task 19): check that busy riders are skipped")


@pytest.mark.skip(reason="TODO(task 19)")
async def test_nobody_free_within_5_km_gives_404(client, db):
    """Only the 8 km rider is free: GET /riders/nearest answers 404."""
    raise NotImplementedError("TODO(task 19): check the 5 km limit")


@pytest.mark.skip(reason="TODO(task 19)")
async def test_two_orders_at_once_cannot_share_a_rider(client, db, order_body):
    """One free rider near the restaurant, two POST /orders at the same moment (asyncio.gather):
    one answers 201 and the other 409."""
    raise NotImplementedError("TODO(task 19): place two orders at once")
