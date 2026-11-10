"""Load for the WebSocket autoscaler (task 22): many customers open and reopen one order's live feed.

Run it from tiffintrack/ while the cluster runs, after placing an order that is not delivered:
    uv run python scripts/ws_load.py --seconds 240

Your code here will need: time, and connect from websockets.asyncio.client.
"""

import argparse
import asyncio
from dataclasses import dataclass

WS_ORDERS = "ws://localhost:8080/ws/orders/"
HOLD_SECONDS = 5  # how long each connection stays open before it closes and opens again

# TODO(task 22): the id of an order that is not delivered yet. Or pass it with --order <id>.
ORDER_ID = ""


@dataclass
class Stats:
    """What the whole run did. main() prints it as one summary line."""

    opened: int = 0  # connections opened
    errors: int = 0  # connections that failed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open many WebSockets to one order's live feed.")
    parser.add_argument("--seconds", type=float, default=240, help="how long the load lasts")
    parser.add_argument("--tasks", type=int, default=200, help="connections open at the same time")
    parser.add_argument(
        "--order", default=ORDER_ID, help="the id of an order that is not delivered"
    )
    return parser.parse_args(argv)


async def viewer(url: str, until: float, stats: Stats) -> None:
    """One customer: open the WebSocket, keep it open HOLD_SECONDS, close it, and repeat until `until`.

    Count each open in stats.opened and each failure in stats.errors.
    Edge case: a failed connection must not stop this viewer; it tries again.
    TODO(task 22): write it.
    """
    raise NotImplementedError("TODO(task 22): open, wait, close and repeat")


async def main(argv: list[str] | None = None) -> None:
    """Run args.tasks viewers at the same time on WS_ORDERS + the order id, then print a summary,
    for example: tasks=200 seconds=240 opened=9600 errors=0

    TODO(task 22): write it.
    """
    args = parse_args(argv)
    raise NotImplementedError(f"TODO(task 22): run {args.tasks} viewers at the same time")


if __name__ == "__main__":
    asyncio.run(main())
