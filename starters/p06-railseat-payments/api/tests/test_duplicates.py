"""Duplicate webhooks (task 14, steps 4-5).

Each test says what to check. Write the body, then delete its skip line.

Use signed_event() from tests/fakes.py for every body.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 14)")
async def test_three_copies_make_one_payment(client):
    """Post one signed payment.captured 3 times: 200 each time, one payment, two
    ledger rows for it and a ledger total of 0."""
    raise NotImplementedError("TODO(task 14): write this test")


@pytest.mark.skip(reason="TODO(task 14)")
async def test_two_copies_at_the_same_moment(client):
    """Post two copies at once with asyncio.gather: exactly one is processed, the
    other answers {"status": "duplicate"}."""
    raise NotImplementedError("TODO(task 14): write this test")
