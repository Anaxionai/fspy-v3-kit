"""Late events (task 14, steps 6-7).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 14)")
async def test_a_late_failed_payment_keeps_a_paid_order(client):
    """A paid order, then payment.failed (reason timeout) for a second payment of it:
    200, and the order stays paid."""
    raise NotImplementedError("TODO(task 14): write this test")


@pytest.mark.skip(reason="TODO(task 14)")
async def test_a_late_capture_after_a_refund_adds_nothing(client):
    """After refund.processed, a late copy of payment.captured: 200 and no new ledger rows."""
    raise NotImplementedError("TODO(task 14): write this test")
