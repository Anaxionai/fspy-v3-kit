"""MockPay's webhook and its signature (task 10, steps 8-9).

Each test says what to check. Write the body, then delete its skip line.

tests/fixtures/payment_captured.json is README section 5's example body, on one
line with no newline at the end. Read it with `read_bytes()`, never re-dump it.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 10)")
async def test_sign_matches_the_readme_example(client):
    """sign(fixture bytes, "mockpay_test_secret") equals the README's value:
    sha256=23700b83f23fd1091239618a650204c029bf32e6820d005a9595b0824a862844"""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10)")
async def test_a_signed_capture_confirms_the_booking(client):
    """Make an order whose gateway_order_id is "order_test" (125000 paise), post the
    fixture with its signature: 200, the order is paid and the booking confirmed."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10)")
async def test_a_changed_body_gets_400_and_changes_nothing(client):
    """Change one byte of the fixture and keep the old signature: 400, and the order is
    still created, with no payment."""
    raise NotImplementedError("TODO(task 10): write this test")
