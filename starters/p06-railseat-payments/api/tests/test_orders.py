"""Creating a MockPay order (task 9, step 10).

Each test says what to check. Write the body, then delete its skip line.

Swap MockPay for FakeMockPay (tests/fakes.py) with
`app.dependency_overrides[get_mockpay]`, so no test calls the real MockPay.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 9)")
async def test_the_order_amount_is_the_fare(client):
    """A pending booking with fare_paise 120000: POST /payments/orders gives 201, and
    the fake saw amount_paise 120000 and the PNR as the receipt."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9)")
async def test_an_amount_in_the_body_is_ignored(client):
    """Send {"pnr": ..., "amount_paise": 1}: the order still has the fare."""
    raise NotImplementedError("TODO(task 9): write this test")


@pytest.mark.skip(reason="TODO(task 9)")
async def test_another_passengers_pnr_gets_404(client):
    """Ravi asks to pay for Asha's booking: 404, and the fake saw no call."""
    raise NotImplementedError("TODO(task 9): write this test")
