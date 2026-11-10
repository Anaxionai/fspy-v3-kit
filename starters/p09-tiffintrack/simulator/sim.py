"""TiffinTrack's rider simulator: many riders move around Pune at once and post GPS points.

Start the API first, then run from the tiffintrack/ folder:
    uv run python simulator/sim.py --riders 50 --interval 2 --seconds 60

Your code here will need: math, random, time, and datetime with UTC.
"""

import argparse
import asyncio
import os
from dataclasses import dataclass

import httpx

API_URL = os.environ.get("API_URL", "http://localhost:8000")

PUNE = (18.5204, 73.8567)  # Pune centre: (lat, lng)
START_SPREAD = 0.045  # degrees: riders start within about 5 km of the centre
STEP = 0.00015  # degrees per point: about 16 m, so about 30 km/h at one point every 2 s
NEAR_TARGET = 0.00045  # degrees: about 50 m. Closer than this, pick a new target.

# For --flaky (task 9): the chance per point to go offline, how long, and how many to resend.
OFFLINE_CHANCE = 1 / 20
OFFLINE_SECONDS = (5, 15)
RESEND_LAST = 3


@dataclass
class Stats:
    """What the whole run did. main() prints it as one summary line."""

    sent: int = 0  # points posted
    errors: int = 0  # failed requests and answers that were not 2xx


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate delivery riders around Pune.")
    parser.add_argument("--riders", type=int, default=50, help="how many riders ride at once")
    parser.add_argument("--interval", type=float, default=2.0, help="seconds between points")
    parser.add_argument("--seconds", type=float, default=60.0, help="how long the run lasts")
    parser.add_argument("--flaky", action="store_true", help="riders sometimes go offline (task 9)")
    return parser.parse_args(argv)


async def report_progress(stats: Stats, every: float = 10.0) -> None:
    """Print the counts so far every `every` seconds, until it is cancelled.

    A long run shows that it is working. In P12, `kubectl logs deployment/sim` shows these lines.
    """
    while True:
        await asyncio.sleep(every)
        print(f"progress: sent={stats.sent} errors={stats.errors}", flush=True)


def random_spot() -> tuple[float, float]:
    """A random (lat, lng) within START_SPREAD degrees of PUNE, for a start or a target.

    TODO(task 7): write it.
    """
    raise NotImplementedError("TODO(task 7): pick a random spot near Pune")


def step_towards(lat: float, lng: float, target: tuple[float, float]) -> tuple[float, float]:
    """The new (lat, lng) after one STEP from (lat, lng) straight towards target.

    Edge case: if the rider is already on the target, stay where you are.
    TODO(task 7): write it.
    """
    raise NotImplementedError("TODO(task 7): move one step towards the target")


async def ride(
    rider_id: int, client: httpx.AsyncClient, args: argparse.Namespace, stats: Stats
) -> None:
    """One rider: until args.seconds have passed, move one step, post a point, then wait args.interval.

    Post each point to /riders/{rider_id}/points as JSON with seq, lat, lng and ts (now, in UTC).
    The first seq is int(time.time()), then it grows by 1 per point, so a restarted
    simulator never reuses a number. Count every point in stats.sent and every failure in stats.errors.
    Edge case: wait without blocking, so all riders keep moving together.
    TODO(task 7): write it.
    TODO(task 9): with args.flaky, the rider sometimes goes offline (OFFLINE_CHANCE, OFFLINE_SECONDS).
      While offline it keeps its points. Back online, it sends them oldest first,
      then sends its last RESEND_LAST points again.
    """
    raise NotImplementedError("TODO(task 7): move, post a point and wait, until the time is up")


async def main(argv: list[str] | None = None) -> None:
    """Run args.riders riders at the same time with one shared HTTP client, then print a summary.

    The summary is one line, for example: riders=50 seconds=60 sent=1500 errors=0
    While the riders run, also run report_progress(stats) as a task, and cancel it at the end.
    TODO(task 7): write it.
    """
    args = parse_args(argv)
    raise NotImplementedError(f"TODO(task 7): run {args.riders} riders at the same time")


if __name__ == "__main__":
    asyncio.run(main())
