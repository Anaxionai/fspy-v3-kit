"""POST /v1/refunds: partial refunds, the cap, idempotency and the webhook."""

from fastapi.testclient import TestClient

from tests.helpers import (
    AUTH,
    WebhookReceiver,
    captured_payment,
    create_order,
    get_json,
    pay,
    payment_id_from,
)


def refund(client: TestClient, payment_id: str, amount_paise: int, key: str | None = None):
    headers = dict(AUTH)
    if key is not None:
        headers["Idempotency-Key"] = key
    return client.post(
        "/v1/refunds",
        json={"payment_id": payment_id, "amount_paise": amount_paise},
        headers=headers,
    )


def test_partial_refunds_up_to_the_captured_amount(client: TestClient) -> None:
    payment_id = captured_payment(client, 10_000)

    first = refund(client, payment_id, 4_000)
    second = refund(client, payment_id, 6_000)
    one_paisa_too_many = refund(client, payment_id, 1)

    assert first.status_code == second.status_code == 201
    assert first.json()["id"].startswith("rfnd_")
    assert first.json()["status"] == "processed"
    assert one_paisa_too_many.status_code == 400
    assert one_paisa_too_many.json()["error"]["code"] == "refund_exceeds_captured"
    payment = get_json(client, f"/v1/payments/{payment_id}")
    assert payment["amount_refunded_paise"] == 10_000
    assert len(payment["refunds"]) == 2


def test_one_refund_above_the_captured_amount_is_400(client: TestClient) -> None:
    payment_id = captured_payment(client, 10_000)

    response = refund(client, payment_id, 10_001)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "refund_exceeds_captured"
    assert get_json(client, f"/v1/payments/{payment_id}")["amount_refunded_paise"] == 0


def test_failed_payment_cannot_be_refunded(client: TestClient) -> None:
    order = create_order(client)
    payment_id = payment_id_from(pay(client, order["id"], "decline"))

    response = refund(client, payment_id, 100)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "payment_not_captured"


def test_unknown_payment_is_404(client: TestClient) -> None:
    response = refund(client, "pay_doesnotexist", 100)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "payment_not_found"


def test_refund_amount_must_be_positive_whole_paise(client: TestClient) -> None:
    payment_id = captured_payment(client)
    for bad_amount in (0, -5, 10.5, "100"):
        assert refund(client, payment_id, bad_amount).status_code == 400, bad_amount


def test_refund_idempotency(client: TestClient) -> None:
    payment_id = captured_payment(client, 10_000)

    first = refund(client, payment_id, 3_000, key="refund-1")
    again = refund(client, payment_id, 3_000, key="refund-1")
    changed = refund(client, payment_id, 2_000, key="refund-1")

    assert again.status_code == 201
    assert again.json() == first.json()
    assert again.headers["Idempotent-Replayed"] == "true"
    assert changed.status_code == 409
    assert get_json(client, f"/v1/payments/{payment_id}")["amount_refunded_paise"] == 3_000


def test_failed_refund_does_not_use_up_the_key(client: TestClient) -> None:
    payment_id = captured_payment(client, 10_000)

    too_big = refund(client, payment_id, 20_000, key="refund-2")
    fixed = refund(client, payment_id, 2_000, key="refund-2")

    assert too_big.status_code == 400
    assert fixed.status_code == 201


def test_refund_sends_a_refund_processed_webhook(
    client: TestClient, receiver: WebhookReceiver
) -> None:
    order = create_order(client, 10_000)
    payment_id = payment_id_from(pay(client, order["id"], "succeed"))
    refund_id = refund(client, payment_id, 2_500).json()["id"]

    [webhook] = receiver.wait_for(1, "refund.processed")

    assert webhook.event["data"] == {
        "order_id": order["id"],
        "payment_id": payment_id,
        "refund_id": refund_id,
        "amount_paise": 2_500,
        "status": "processed",
    }
