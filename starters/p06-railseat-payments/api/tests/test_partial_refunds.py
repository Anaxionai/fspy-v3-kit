"""Partial refunds (task 14, steps 9-10).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 14)")
async def test_a_partial_refund_balances(client):
    """Refund a 120000 fare: 90000 refunded, payment partially_refunded,
    mockpay_clearing at 30000 and a ledger total of 0."""
    raise NotImplementedError("TODO(task 14): write this test")


@pytest.mark.skip(reason="TODO(task 14)")
async def test_the_same_key_replays_the_refund(client):
    """Repeat the refund with the same Idempotency-Key: the same reply with
    Idempotent-Replayed: true, and one call on the fake. A new key gets 409."""
    raise NotImplementedError("TODO(task 14): write this test")
