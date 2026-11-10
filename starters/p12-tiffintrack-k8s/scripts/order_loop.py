"""Orders that keep flowing during a release (task 23).

Every 200 ms it places an order at http://localhost:8080, then moves it to picked_up, nearby and
delivered, which frees its rider. It counts every answer by status code and by its X-App-Version
header. A 5xx answer or a connection error is a failure.

Run it from tiffintrack/ while the cluster runs:
    uv run python scripts/order_loop.py --seconds 120

Your code here will need: time.
"""

import argparse
import asyncio
from collections import Counter
from dataclasses import dataclass, field

import httpx

BASE_URL = "http://localhost:8080"
EVERY_SECONDS = 0.2
STEPS = ["picked_up", "nearby", "delivered"]

# TODO(task 23): a body that your POST /orders accepts. This one fits the P9 starter's OrderIn.
ORDER_BODY = {
    "customer": {"name": "Asha Kulkarni", "phone": "9876543210"},
    "restaurant": {"name": "Shaniwar Thali House", "lat": 18.5195, "lng": 73.8553},
    "address": {"label": "Flat 4B, Karve Road", "lat": 18.5074, "lng": 73.8077},
    "items": [{"name": "Veg thali", "qty": 2, "price_paise": 18000}],
}


@dataclass
class Tally:
    """Every answer the loop got. main() prints it at the end."""

    by_status: Counter = field(default_factory=Counter)  # for example {201: 600, 200: 1800}
    by_version: Counter = field(default_factory=Counter)  # X-App-Version, or "none" without it
    failures: int = 0  # 5xx answers and connection errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Place orders and deliver them, on a timer.")
    parser.add_argument("--seconds", type=float, default=120, help="how long the loop runs")
    return parser.parse_args(argv)


async def one_order(client: httpx.AsyncClient, tally: Tally) -> None:
    """Place one order with ORDER_BODY, then move it through STEPS. Record every answer in tally.

    Edge cases: a 409 "No free rider nearby" is not a failure, but that order stops there;
    a connection error is a failure, and it must not stop the loop.
    TODO(task 23): write it.
    """
    raise NotImplementedError("TODO(task 23): place one order and deliver it")


async def main(argv: list[str] | None = None) -> None:
    """Start one_order every EVERY_SECONDS until args.seconds have passed, without waiting for the
    last one to finish. Then wait for the ones still running and print the tally, for example:
    failed=0 statuses={201: 600, 200: 1800} versions={'none': 1300, '0.3.0': 1100}

    TODO(task 23): write it.
    """
    args = parse_args(argv)
    raise NotImplementedError(f"TODO(task 23): run the loop for {args.seconds:g} seconds")


if __name__ == "__main__":
    asyncio.run(main())
