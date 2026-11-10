"""Refunding a cancelled booking (task 13, step 10).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 13)")
async def test_a_refund_keeps_the_25_percent_fee(client):
    """A paid 120000 booking: the reply has refund_paise 90000 and fee_paise 30000,
    the payment is partially_refunded, the order cancelled, the booking cancelled."""
    raise NotImplementedError("TODO(task 13): write this test")


@pytest.mark.skip(reason="TODO(task 13)")
async def test_the_ledger_still_balances(client):
    """After the refund, the balances add up to 0 and mockpay_clearing holds 30000
    (no settlement imported)."""
    raise NotImplementedError("TODO(task 13): write this test")


@pytest.mark.skip(reason="TODO(task 13)")
async def test_a_second_refund_gets_409(client):
    """Refund the same booking again with a new key: 409."""
    raise NotImplementedError("TODO(task 13): write this test")
