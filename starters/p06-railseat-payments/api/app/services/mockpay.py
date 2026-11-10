"""Talking to MockPay (P6 add-on). MockPay's README in the kit is the reference.

- Calls to MockPay go through `MockPayClient` (tasks 9, 12 and 13).
- Routes get the client from the `get_mockpay()` dependency, so tests can swap
  in a fake with `app.dependency_overrides[get_mockpay]`.
- `sign()` and `signature_ok()` check MockPay's webhook signature (task 10).
"""

from collections.abc import AsyncIterator
from datetime import date

from app import settings


class MockPayError(Exception):
    """MockPay answered with an error status. Your route turns it into 502."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class MockPayClient:
    """A small client for MockPay's API. Every method raises `httpx.TimeoutException`
    on a timeout and `MockPayError` for an error answer; the route decides what to do."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """Make `self.http`, an `httpx.AsyncClient` for MockPay (task 9, step 1).

        The brief's step 1 lists its settings: the base URL, the timeout and the
        `Authorization: Bearer <api_key>` header.
        """
        raise NotImplementedError(
            "TODO(task 9): make the httpx.AsyncClient for MockPay"
        )

    async def create_order(
        self, amount_paise: int, receipt: str, return_url: str
    ) -> dict:
        """POST /v1/orders and return MockPay's order as a dict (task 9, steps 2 and 5).

        Send `amount_paise`, `currency` ("INR"), `receipt` (the PNR) and `return_url`.
        The reply holds `id` and `checkout_url`. An answer of 400 or more raises
        MockPayError with the `message` from MockPay's error body.
        Task 11, step 7: also send the header `Idempotency-Key: booking-<receipt>`.
        """
        raise NotImplementedError("TODO(task 9): create the order at MockPay")

    async def settlement_report(self, day: date) -> dict:
        """GET /v1/settlements?date=YYYY-MM-DD for one IST day (task 12, step 7).

        Return the report as a dict (README section 7). Errors raise MockPayError.
        """
        raise NotImplementedError("TODO(task 12): read the day's settlement report")

    async def refund(self, payment_id: str, amount_paise: int, key: str) -> dict:
        """POST /v1/refunds with the header `Idempotency-Key: <key>` (task 13, step 1).

        Send `payment_id` and `amount_paise`; return MockPay's refund (it has `id`).
        Errors such as `refund_exceeds_captured` raise MockPayError.
        """
        raise NotImplementedError("TODO(task 13): refund a payment at MockPay")

    async def aclose(self) -> None:
        await self.http.aclose()


async def get_mockpay() -> AsyncIterator[MockPayClient]:
    """FastAPI dependency: one MockPayClient per request, closed afterwards.

    Reads MOCKPAY_URL and MOCKPAY_API_KEY from app/settings.py (see STARTER.md).
    """
    client = MockPayClient(settings.MOCKPAY_URL, settings.MOCKPAY_API_KEY)
    try:
        yield client
    finally:
        await client.aclose()


def sign(raw_body: bytes, secret: str) -> str:
    """Return the `X-MockPay-Signature` value for these exact bytes (task 10, steps 4 and 8).

    That is "sha256=" followed by the HMAC-SHA256 hex digest of `raw_body` with
    `secret`. README section 5 has a body and the value it must give.
    """
    raise NotImplementedError("TODO(task 10): compute the HMAC-SHA256 signature")


def signature_ok(raw_body: bytes, header: str | None, secret: str) -> bool:
    """True when `header` is the right signature for `raw_body` (task 10, step 4).

    A missing header is False. Compare with `hmac.compare_digest`, never `==`.
    """
    raise NotImplementedError("TODO(task 10): compare the signatures safely")
