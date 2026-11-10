"""Test helpers: a real local webhook receiver, and short-cuts for common API calls."""

import json
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlsplit

import httpx
from fastapi.testclient import TestClient

API_KEY = "test_key"
SECRET = "test_secret"
AUTH = {"Authorization": f"Bearer {API_KEY}"}


def wait_until[T](check: Callable[[], T], timeout: float = 5.0, what: str = "a condition") -> T:
    """Call `check` until it returns something truthy, and return that."""
    deadline = time.monotonic() + timeout
    while True:
        result = check()
        if result:
            return result
        if time.monotonic() > deadline:
            raise AssertionError(f"Timed out after {timeout} s waiting for {what}")
        time.sleep(0.02)


@dataclass
class Received:
    """One webhook request, exactly as it arrived."""

    headers: dict[str, str]  # names in lower case
    body: bytes

    @property
    def event(self) -> dict[str, Any]:
        return json.loads(self.body)


class WebhookReceiver:
    """A real HTTP server on 127.0.0.1 that plays the merchant's webhook endpoint.

    `planned_statuses` are the answers for the next requests, in order;
    after those it answers `default_status`.
    """

    def __init__(self) -> None:
        self.planned_statuses: list[int] = []
        self.default_status = 200
        self._received: list[Received] = []
        self._lock = threading.Lock()
        receiver = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                item = Received(
                    headers={name.lower(): value for name, value in self.headers.items()},
                    body=self.rfile.read(length),
                )
                status = receiver._record(item)
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"{}")

            def log_message(self, format: str, *args: Any) -> None:
                pass  # keep the test output quiet

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        # A short poll interval makes shutdown() quick (the default waits up to 0.5 s).
        self._thread = threading.Thread(
            target=self._server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True
        )

    def _record(self, item: Received) -> int:
        with self._lock:
            self._received.append(item)
            return self.planned_statuses.pop(0) if self.planned_statuses else self.default_status

    @property
    def url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}/payments/webhook"

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()

    def received(self, event_type: str | None = None) -> list[Received]:
        with self._lock:
            items = list(self._received)
        return [r for r in items if event_type is None or r.event["type"] == event_type]

    def wait_for(
        self, count: int, event_type: str | None = None, timeout: float = 5.0
    ) -> list[Received]:
        """Wait until at least `count` webhooks (of this type) have arrived."""
        return wait_until(
            lambda: (items := self.received(event_type)) and len(items) >= count and items,
            timeout,
            f"{count} webhook(s) of type {event_type or 'any'}",
        )


def fast_settings(db_path: str, webhook_url: str) -> dict[str, Any]:
    """Settings that make MockPay quick and predictable in tests."""
    return {
        "webhook_secret": SECRET,
        "webhook_url": webhook_url,
        "api_key": API_KEY,
        "duplicate_rate": 0.0,
        "delay_seconds": 0.0,
        "late_rate": 0.0,
        "duplicate_gap_seconds": 0.0,
        "retry_delays": (0.05, 0.1, 0.2),
        "timeout_seconds": 0.5,
        "answer_timeout_seconds": 2.0,
        "poll_seconds": 0.02,
        "db_path": db_path,
    }


def create_order(
    client: TestClient, amount_paise: int = 10_000, key: str | None = None, **fields: Any
) -> dict[str, Any]:
    headers = dict(AUTH)
    if key is not None:
        headers["Idempotency-Key"] = key
    body = {"amount_paise": amount_paise, "currency": "INR", "receipt": "PNR4F7K2Q9", **fields}
    response = client.post("/v1/orders", json=body, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()


def pay(client: TestClient, order_id: str, outcome: str) -> httpx.Response:
    """Press one of the checkout buttons (the form posts outcome=succeed|decline|timeout)."""
    return client.post(
        f"/checkout/{order_id}/pay", data={"outcome": outcome}, follow_redirects=False
    )


def payment_id_from(response: httpx.Response) -> str:
    """After paying, the redirect carries ?payment_id=pay_..."""
    assert response.status_code == 303, response.text
    query = parse_qs(urlsplit(response.headers["location"]).query)
    return query["payment_id"][0]


def captured_payment(client: TestClient, amount_paise: int = 10_000) -> str:
    """Create an order, pay it successfully, and return the payment id."""
    order = create_order(client, amount_paise)
    return payment_id_from(pay(client, order["id"], "succeed"))


def get_json(client: TestClient, path: str) -> dict[str, Any]:
    response = client.get(path, headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()
