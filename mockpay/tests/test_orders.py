"""POST /v1/orders and GET /v1/orders/{id}, including idempotency keys."""

from fastapi.testclient import TestClient

from tests.helpers import AUTH, create_order, get_json, pay

ORDER = {"amount_paise": 125_000, "currency": "INR", "receipt": "PNR4F7K2Q9"}


def post_order(client: TestClient, body: dict, key: str | None = None):
    headers = dict(AUTH)
    if key is not None:
        headers["Idempotency-Key"] = key
    return client.post("/v1/orders", json=body, headers=headers)


def test_create_order_returns_the_contract_fields(client: TestClient) -> None:
    response = post_order(client, ORDER)

    assert response.status_code == 201
    order = response.json()
    assert order["id"].startswith("order_")
    assert order["amount_paise"] == 125_000
    assert order["status"] == "created"
    assert order["checkout_url"] == f"http://localhost:9090/checkout/{order['id']}"


def test_same_key_and_same_body_return_the_same_order(client: TestClient) -> None:
    first = post_order(client, ORDER, key="key-1")
    second = post_order(client, ORDER, key="key-1")

    assert first.status_code == second.status_code == 201
    assert second.json() == first.json()
    assert second.headers["Idempotent-Replayed"] == "true"
    assert "Idempotent-Replayed" not in first.headers


def test_key_order_of_json_fields_does_not_matter(client: TestClient) -> None:
    first = post_order(client, ORDER, key="key-2")
    reordered = {"receipt": "PNR4F7K2Q9", "currency": "INR", "amount_paise": 125_000}
    second = post_order(client, reordered, key="key-2")

    assert second.json()["id"] == first.json()["id"]


def test_same_key_with_a_different_body_is_409(client: TestClient) -> None:
    post_order(client, ORDER, key="key-3")
    response = post_order(client, {**ORDER, "amount_paise": 99_900}, key="key-3")

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "idempotency_key_reused"


def test_without_a_key_every_request_makes_a_new_order(client: TestClient) -> None:
    first = post_order(client, ORDER)
    second = post_order(client, ORDER)

    assert first.json()["id"] != second.json()["id"]


def test_amount_must_be_a_whole_number_of_paise(client: TestClient) -> None:
    for bad_amount in (1250.5, 1250.0, "1250", 99, -100):
        response = post_order(client, {**ORDER, "amount_paise": bad_amount})
        assert response.status_code == 400, bad_amount
        assert response.json()["error"]["code"] == "invalid_request"
        assert "amount_paise" in response.json()["error"]["message"]


def test_only_inr_is_accepted(client: TestClient) -> None:
    response = post_order(client, {**ORDER, "currency": "USD"})
    assert response.status_code == 400


def test_unknown_fields_are_refused(client: TestClient) -> None:
    response = post_order(client, {**ORDER, "amount_rupees": 1250})
    assert response.status_code == 400


def test_api_key_is_required(client: TestClient) -> None:
    missing = client.post("/v1/orders", json=ORDER)
    wrong = client.post("/v1/orders", json=ORDER, headers={"Authorization": "Bearer nope"})

    for response in (missing, wrong):
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "invalid_api_key"


def test_get_order_shows_its_payments(client: TestClient) -> None:
    order = create_order(client, 50_000, notes={"pnr": "PNR4F7K2Q9"})
    pay(client, order["id"], "decline")
    pay(client, order["id"], "succeed")

    fetched = get_json(client, f"/v1/orders/{order['id']}")

    assert fetched["status"] == "paid"
    assert fetched["attempts"] == 2
    assert len(fetched["payments"]) == 2
    assert fetched["amount_paid_paise"] == 50_000
    assert fetched["notes"] == {"pnr": "PNR4F7K2Q9"}


def test_unknown_order_is_404(client: TestClient) -> None:
    response = client.get("/v1/orders/order_doesnotexist", headers=AUTH)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "order_not_found"
