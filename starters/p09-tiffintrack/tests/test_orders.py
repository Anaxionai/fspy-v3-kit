"""Orders in MongoDB (task 15). Needs the cloud lab with MongoDB. Uses the tiffintrack_test database.

From task 19, placing an order needs a free rider nearby: add the free_rider fixture to these tests.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 15)")
async def test_create_then_read_an_order(client, db, order_body):
    """POST /orders with order_body, then GET /orders/{id}: the same order comes back,
    with status "placed" and a timeline of one entry."""
    raise NotImplementedError("TODO(task 15): create an order and read it back")


@pytest.mark.skip(reason="TODO(task 15)")
async def test_a_malformed_id_gives_404(client, db):
    """GET /orders/not-an-id answers 404, not 500."""
    raise NotImplementedError("TODO(task 15): read an order with a malformed id")
