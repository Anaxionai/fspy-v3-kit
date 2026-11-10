"""The X-MockPay-Signature header: format, a known value, and what is really sent."""

import re

from fastapi.testclient import TestClient

from mockpay.signing import sign, verify
from tests.helpers import SECRET, WebhookReceiver, create_order, pay

# The same example as in README.md, so students can check their own code.
EXAMPLE_BODY = (
    b'{"id":"evt_test","type":"payment.captured","created_at":"2026-11-10T15:45:30+05:30",'
    b'"data":{"order_id":"order_test","payment_id":"pay_test","amount_paise":125000,'
    b'"status":"captured"}}'
)
EXAMPLE_SIGNATURE = "sha256=23700b83f23fd1091239618a650204c029bf32e6820d005a9595b0824a862844"

SIGNATURE_FORMAT = re.compile(r"^sha256=[0-9a-f]{64}$")


def test_signature_format() -> None:
    assert SIGNATURE_FORMAT.match(sign(b"{}", "any secret"))


def test_known_example_signature() -> None:
    assert sign(EXAMPLE_BODY, "mockpay_test_secret") == EXAMPLE_SIGNATURE


def test_verify_accepts_the_right_signature_only() -> None:
    assert verify(EXAMPLE_BODY, EXAMPLE_SIGNATURE, "mockpay_test_secret")
    assert not verify(
        EXAMPLE_BODY.replace(b"125000", b"1"), EXAMPLE_SIGNATURE, "mockpay_test_secret"
    )
    assert not verify(EXAMPLE_BODY, EXAMPLE_SIGNATURE, "another secret")
    assert not verify(
        EXAMPLE_BODY, EXAMPLE_SIGNATURE.removeprefix("sha256="), "mockpay_test_secret"
    )
    assert not verify(EXAMPLE_BODY, None, "mockpay_test_secret")


def test_sent_webhook_is_signed_over_its_raw_body(
    client: TestClient, receiver: WebhookReceiver
) -> None:
    order = create_order(client, 125_000)
    pay(client, order["id"], "succeed")

    [webhook] = receiver.wait_for(1)

    assert SIGNATURE_FORMAT.match(webhook.headers["x-mockpay-signature"])
    assert webhook.headers["x-mockpay-signature"] == sign(webhook.body, SECRET)
    assert webhook.headers["x-mockpay-event-id"] == webhook.event["id"]
    assert webhook.headers["content-type"] == "application/json"


def test_webhook_body_has_the_contract_fields(
    client: TestClient, receiver: WebhookReceiver
) -> None:
    order = create_order(client, 125_000)
    pay(client, order["id"], "succeed")

    [webhook] = receiver.wait_for(1)
    event = webhook.event

    assert event["id"].startswith("evt_")
    assert event["type"] == "payment.captured"
    assert event["created_at"].endswith("+05:30")
    assert set(event["data"]) == {"order_id", "payment_id", "amount_paise", "status"}
    assert event["data"]["order_id"] == order["id"]
    assert event["data"]["amount_paise"] == 125_000
    # Compact JSON: re-serialising with Python's default spacing would break the signature.
    assert b", " not in webhook.body
