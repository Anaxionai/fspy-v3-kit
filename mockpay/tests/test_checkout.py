"""The hosted checkout page: success, decline and timeout, and the redirect back."""

import time
from collections.abc import Callable
from urllib.parse import parse_qs, urlsplit

from fastapi.testclient import TestClient

from tests.helpers import WebhookReceiver, create_order, get_json, pay, payment_id_from

RETURN_URL = "http://localhost:5173/payments/return?from=mockpay"


def test_checkout_page_shows_the_amount_and_three_buttons(client: TestClient) -> None:
    order = create_order(client, 125_000)

    page = client.get(f"/checkout/{order['id']}")

    assert page.status_code == 200
    assert "₹1,250.00" in page.text
    for label in ("Pay with UPI (succeeds)", "Pay (bank declines)", "Pay (times out)"):
        assert label in page.text


def test_unknown_order_page_is_404(client: TestClient) -> None:
    assert client.get("/checkout/order_doesnotexist").status_code == 404


def test_success_captures_and_sends_payment_captured(
    client: TestClient, receiver: WebhookReceiver
) -> None:
    order = create_order(client, 125_000, return_url=RETURN_URL)

    response = pay(client, order["id"], "succeed")

    # Back to the shop, with the ids added to the return_url's own query.
    location = response.headers["location"]
    assert response.status_code == 303
    assert location.startswith("http://localhost:5173/payments/return?")
    query = parse_qs(urlsplit(location).query)
    assert query["from"] == ["mockpay"] and query["order_id"] == [order["id"]]
    payment_id = query["payment_id"][0]

    payment = get_json(client, f"/v1/payments/{payment_id}")
    assert payment["status"] == "captured"
    assert get_json(client, f"/v1/orders/{order['id']}")["status"] == "paid"

    [webhook] = receiver.wait_for(1)
    assert webhook.event["type"] == "payment.captured"
    assert webhook.event["data"] == {
        "order_id": order["id"],
        "payment_id": payment_id,
        "amount_paise": 125_000,
        "status": "captured",
    }


def test_decline_fails_and_sends_payment_failed(
    client: TestClient, receiver: WebhookReceiver
) -> None:
    order = create_order(client, 125_000, return_url=RETURN_URL)

    payment_id = payment_id_from(pay(client, order["id"], "decline"))

    payment = get_json(client, f"/v1/payments/{payment_id}")
    assert payment["status"] == "failed"
    assert payment["reason"] == "bank_declined"
    assert get_json(client, f"/v1/orders/{order['id']}")["status"] == "attempted"
    [webhook] = receiver.wait_for(1)
    assert webhook.event["type"] == "payment.failed"
    assert webhook.event["data"]["reason"] == "bank_declined"
    assert webhook.event["data"]["status"] == "failed"


def test_timeout_sends_nothing_until_the_timeout_then_payment_failed(
    make_client: Callable[..., TestClient], receiver: WebhookReceiver
) -> None:
    client = make_client(timeout_seconds=0.8)
    order = create_order(client, 125_000, return_url=RETURN_URL)
    pressed = time.monotonic()

    response = pay(client, order["id"], "timeout")

    # The customer is sent back at once, while the bank has not answered.
    payment_id = payment_id_from(response)
    assert get_json(client, f"/v1/payments/{payment_id}")["status"] == "pending"
    time.sleep(0.3)
    assert receiver.received() == []

    [webhook] = receiver.wait_for(1, "payment.failed")
    assert time.monotonic() - pressed >= 0.8
    assert webhook.event["data"]["reason"] == "timeout"
    assert webhook.event["data"]["payment_id"] == payment_id
    payment = get_json(client, f"/v1/payments/{payment_id}")
    assert (payment["status"], payment["reason"]) == ("failed", "timeout")


def test_without_return_url_mockpay_shows_its_own_result_page(client: TestClient) -> None:
    order = create_order(client, 125_000)

    response = pay(client, order["id"], "succeed")

    assert response.headers["location"].startswith(f"/checkout/{order['id']}/result?payment_id=")
    page = client.get(response.headers["location"])
    assert page.status_code == 200
    assert "captured" in page.text


def test_a_paid_order_cannot_be_paid_again(client: TestClient) -> None:
    order = create_order(client)
    pay(client, order["id"], "succeed")

    again = pay(client, order["id"], "succeed")

    assert again.status_code == 409
    assert "already paid" in client.get(f"/checkout/{order['id']}").text


def test_customer_can_try_again_after_a_decline(client: TestClient) -> None:
    order = create_order(client)
    pay(client, order["id"], "decline")
    pay(client, order["id"], "succeed")

    fetched = get_json(client, f"/v1/orders/{order['id']}")
    assert fetched["status"] == "paid"
    assert fetched["attempts"] == 2


def test_dashboard_lists_orders_and_webhook_attempts(
    client: TestClient, receiver: WebhookReceiver
) -> None:
    receiver.planned_statuses = [500]
    order = create_order(client)
    pay(client, order["id"], "succeed")
    receiver.wait_for(2)

    page = client.get("/dashboard")

    assert page.status_code == 200
    assert order["id"] in page.text
    assert ">500<" in page.text and ">200<" in page.text  # the status code of each attempt
