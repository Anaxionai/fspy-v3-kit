"""Repeats change nothing (task 11, step 9).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 11)")
async def test_one_event_three_times_makes_one_payment(client):
    """Post the same signed payment.captured 3 times: 200 each time, one Payment row."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
async def test_the_same_order_request_twice_gives_one_order(client):
    """POST /payments/orders twice with the same Idempotency-Key and body: the same
    order_id, and the second reply has Idempotent-Replayed: true."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
async def test_the_same_key_with_another_pnr_gets_409(client):
    """Reuse the key with another booking's PNR: 409."""
    raise NotImplementedError("TODO(task 11): write this test")
