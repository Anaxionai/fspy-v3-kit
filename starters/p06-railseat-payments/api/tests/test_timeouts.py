"""MockPay timing out (task 14, step 8).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 14)")
async def test_a_timeout_gives_504_and_a_retry_works(client):
    """Set fail_next on the fake: POST /payments/orders gives 504 and saves no order.
    Retry with the same Idempotency-Key: 201, and the fake saw booking-<PNR> both times."""
    raise NotImplementedError("TODO(task 14): write this test")
