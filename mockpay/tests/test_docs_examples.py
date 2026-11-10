"""The request examples on /docs must work as they stand, because "Try it out" pre-fills them."""

from fastapi.testclient import TestClient

from tests.helpers import AUTH


def docs_example(client: TestClient, path: str) -> dict:
    spec = client.get("/openapi.json").json()
    examples = spec["paths"][path]["post"]["requestBody"]["content"]["application/json"]["examples"]
    return next(iter(examples.values()))["value"]


def test_the_order_example_creates_an_order_with_a_return_url(client: TestClient) -> None:
    body = docs_example(client, "/v1/orders")

    response = client.post("/v1/orders", json=body, headers=AUTH)

    assert response.status_code == 201
    assert response.json()["return_url"] == "http://localhost:5173/bookings"


def test_the_refund_and_resend_examples_only_need_a_real_id(client: TestClient) -> None:
    refund = docs_example(client, "/v1/refunds")
    resend = docs_example(client, "/v1/simulate/webhook")

    assert set(refund) == {"payment_id", "amount_paise"}
    assert set(resend) == {"event_id", "copies"}
    assert client.post("/v1/refunds", json=refund, headers=AUTH).status_code == 404
    assert client.post("/v1/simulate/webhook", json=resend, headers=AUTH).status_code == 404
