"""Webhook delivery: retries until 2xx, giving up, duplicates, late webhooks, re-sending."""

import random
import socket
import time
from collections.abc import Callable

from fastapi.testclient import TestClient

from mockpay.config import Settings
from mockpay.events import first_delay
from tests.helpers import (
    AUTH,
    WebhookReceiver,
    create_order,
    get_json,
    pay,
    wait_until,
)


def paid_order_event_id(client: TestClient, receiver: WebhookReceiver) -> str:
    order = create_order(client)
    pay(client, order["id"], "succeed")
    return receiver.wait_for(1)[0].event["id"]


def delivery_states(client: TestClient, event_id: str) -> list[dict]:
    return get_json(client, f"/v1/events/{event_id}")["deliveries"]


def test_retries_until_a_2xx_answer(client: TestClient, receiver: WebhookReceiver) -> None:
    receiver.planned_statuses = [500, 503]  # then the default 200
    order = create_order(client)
    pay(client, order["id"], "succeed")

    webhooks = receiver.wait_for(3)
    event_id = webhooks[0].event["id"]
    assert {w.event["id"] for w in webhooks} == {event_id}
    assert len({w.body for w in webhooks}) == 1  # every try sends the same bytes

    deliveries = wait_until(
        lambda: (d := delivery_states(client, event_id)) and d[0]["status"] == "delivered" and d,
        what="the delivery to be marked delivered",
    )
    attempts = deliveries[0]["attempts"]
    assert [a["status_code"] for a in attempts] == [500, 503, 200]
    assert [a["attempt_no"] for a in attempts] == [1, 2, 3]

    time.sleep(0.5)  # longer than all the test retry delays together
    assert len(receiver.received()) == 3  # nothing more after the 2xx


def test_gives_up_after_the_last_retry(client: TestClient, receiver: WebhookReceiver) -> None:
    receiver.default_status = 500
    order = create_order(client)
    pay(client, order["id"], "succeed")

    webhooks = receiver.wait_for(4)  # the first try + 3 retries
    event_id = webhooks[0].event["id"]
    wait_until(
        lambda: delivery_states(client, event_id)[0]["status"] == "gave_up",
        what="MockPay to give up",
    )
    time.sleep(0.5)
    assert len(receiver.received()) == 4


def test_no_answer_counts_as_a_failed_try(make_client: Callable[..., TestClient]) -> None:
    with socket.socket() as probe:  # find a port where nothing is listening
        probe.bind(("127.0.0.1", 0))
        closed_port = probe.getsockname()[1]
    # Windows takes about 2 s to report a refused connection (Linux: at once),
    # so this test allows a longer answer time and makes only one retry.
    client = make_client(
        webhook_url=f"http://127.0.0.1:{closed_port}/payments/webhook",
        answer_timeout_seconds=8.0,
        retry_delays=(0.05,),
    )
    order = create_order(client)
    pay(client, order["id"], "succeed")

    # The event is created when the button is pressed; only sending it takes time.
    event_id = get_json(client, f"/v1/events?order_id={order['id']}")["items"][0]["id"]
    deliveries = wait_until(
        lambda: (d := delivery_states(client, event_id)) and d[0]["status"] == "gave_up" and d,
        timeout=20.0,
        what="MockPay to give up",
    )
    attempts = deliveries[0]["attempts"]
    assert len(attempts) == 2  # the first try + 1 retry
    assert all(a["status_code"] is None and "could not connect" in a["error"] for a in attempts)


def test_every_webhook_is_sent_twice_at_duplicate_rate_1(
    make_client: Callable[..., TestClient], receiver: WebhookReceiver
) -> None:
    client = make_client(duplicate_rate=1.0)
    order = create_order(client)
    pay(client, order["id"], "succeed")

    first, second = receiver.wait_for(2)

    assert first.event["id"] == second.event["id"]
    assert first.body == second.body
    assert first.headers["x-mockpay-signature"] == second.headers["x-mockpay-signature"]
    kinds = {d["kind"] for d in delivery_states(client, first.event["id"])}
    assert kinds == {"first", "duplicate"}


def test_no_duplicates_at_duplicate_rate_0(client: TestClient, receiver: WebhookReceiver) -> None:
    paid_order_event_id(client, receiver)
    time.sleep(0.3)
    assert len(receiver.received()) == 1


def test_simulate_resends_a_past_event(client: TestClient, receiver: WebhookReceiver) -> None:
    event_id = paid_order_event_id(client, receiver)

    response = client.post(
        "/v1/simulate/webhook", json={"event_id": event_id, "copies": 2}, headers=AUTH
    )

    assert response.status_code == 202
    webhooks = receiver.wait_for(3)
    assert {w.event["id"] for w in webhooks} == {event_id}
    assert len({w.body for w in webhooks}) == 1


def test_simulate_unknown_event_is_404(client: TestClient) -> None:
    response = client.post("/v1/simulate/webhook", json={"event_id": "evt_nope"}, headers=AUTH)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "event_not_found"


def test_events_can_be_listed_by_order(client: TestClient, receiver: WebhookReceiver) -> None:
    order = create_order(client)
    pay(client, order["id"], "decline")
    receiver.wait_for(1)

    listed = get_json(client, f"/v1/events?order_id={order['id']}&type=payment.failed")

    assert listed["count"] == 1
    assert listed["items"][0]["data"]["reason"] == "bank_declined"


def test_default_back_off_is_1_5_25_seconds() -> None:
    assert Settings().retry_delays == (1.0, 5.0, 25.0)


def test_first_delay_without_late_webhooks_is_the_base_delay() -> None:
    settings = Settings(delay_seconds=2.0, late_rate=0.0)
    rng = random.Random(1)
    assert {first_delay(settings, rng) for _ in range(100)} == {2.0}


def test_late_webhooks_get_0_to_10_extra_seconds() -> None:
    settings = Settings(delay_seconds=2.0, late_rate=1.0, late_max_seconds=10.0)
    rng = random.Random(2)
    delays = [first_delay(settings, rng) for _ in range(500)]
    assert all(2.0 <= d <= 12.0 for d in delays)
    assert max(delays) > 10.0  # the extra really is spread over 0..10 s


def test_about_one_in_five_webhooks_is_late_by_default() -> None:
    settings = Settings()
    rng = random.Random(3)
    late = sum(first_delay(settings, rng) > settings.delay_seconds for _ in range(5000))
    assert 0.17 < late / 5000 < 0.23
