"""The order's state machine (task 18). Needs the cloud lab with Redis and MongoDB.

From task 19, placing an order needs a free rider nearby: add the free_rider fixture to these tests.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 18)")
async def test_the_three_allowed_moves(client, db, order_body):
    """placed to picked_up, picked_up to nearby, nearby to delivered: each answers 200."""
    raise NotImplementedError("TODO(task 18): walk an order through every status")


@pytest.mark.skip(reason="TODO(task 18)")
async def test_skipping_a_status_gives_409(client, db, order_body):
    """placed to delivered answers 409, and the order is still placed."""
    raise NotImplementedError("TODO(task 18): try to skip a status")


@pytest.mark.skip(reason="TODO(task 18)")
async def test_two_changes_at_once_only_one_wins(client, db, order_body):
    """Two picked_up requests at the same moment (asyncio.gather): one 200 and one 409."""
    raise NotImplementedError("TODO(task 18): send two changes at once")
