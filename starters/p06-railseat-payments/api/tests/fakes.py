"""A fake MockPay and signed test events, so no test calls the real MockPay (P6 add-on).

The brief puts these in tests/conftest.py. Your conftest.py is your own file, so
they live here: import them in conftest.py (STARTER.md shows the lines).
"""


class FakeMockPay:
    """Has the same methods as MockPayClient and records every call.

    `calls` holds one dict per call: the method name, its arguments and the
    Idempotency-Key it would send. Set `fail_next = True` to make the next call
    raise `httpx.ReadTimeout`, then go back to normal.
    """

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.fail_next = False

    async def create_order(
        self, amount_paise: int, receipt: str, return_url: str
    ) -> dict:
        """Record the call (with the key `booking-<receipt>`) and return an order
        shaped like MockPay's: `id`, `amount_paise`, `receipt`, `status` and
        `checkout_url`. The same receipt gives the same order id, as MockPay does."""
        # TODO(task 14): when fail_next is set, clear it and raise httpx.ReadTimeout.
        raise NotImplementedError("TODO(task 9): return a fake MockPay order")

    async def settlement_report(self, day) -> dict:
        """Return a report shaped like README section 7, from values the test sets."""
        raise NotImplementedError("TODO(task 12): return a fake settlement report")

    async def refund(self, payment_id: str, amount_paise: int, key: str) -> dict:
        """Record the call and its key and return a refund with a new `id`."""
        raise NotImplementedError("TODO(task 13): return a fake MockPay refund")

    async def aclose(self) -> None:
        pass


def signed_event(
    event_type: str, data: dict, event_id: str = "evt_test"
) -> tuple[bytes, str]:
    """Build a webhook body shaped like the README's events and sign it (task 14, step 3).

    Return `(raw_body, signature)`: the JSON bytes without spaces (as MockPay sends
    them) and the `sha256=...` value from your `sign()` with MockPay's test secret.
    Post it with `content=raw_body` and the header `X-MockPay-Signature: signature`.
    """
    raise NotImplementedError("TODO(task 14): build and sign a test event")
