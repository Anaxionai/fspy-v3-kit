"""Fill RailSeat with 1,000,000 bookings for the P10 measurements (P10 add-on, task 7).

Run it from railseat/api, so it uses the API's Python and packages (asyncpg):

    uv run python ../perf/make_bookings.py --bookings 1000000

The loading is ready: it reads what the bookings point to, builds the rows in
batches of 100,000 and loads each batch with COPY. The rows are yours: every
schema differs, so you write `prepare()`, `load_context()` and `build_row()`.
Never commit generated data: this script makes the data in the database.
"""

import argparse
import asyncio
import os
import sys
import time

import asyncpg

# Run from railseat/api, so `from app.security import hash_password` finds your API code.
sys.path.insert(0, os.getcwd())

# asyncpg takes a plain postgresql:// URL, without SQLAlchemy's "+asyncpg".
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://railseat:railseat@localhost:5432/railseat"
).replace("+asyncpg", "")
BATCH = 100_000

# TODO(task 7): your bookings table's columns, in the order build_row() returns them,
# for example ["pnr", "journey_id", "seat_id", ...]. Every NOT NULL column without a
# default must be here.
COLUMNS: list[str] = []


async def prepare(conn: asyncpg.Connection) -> None:
    """Create what the bookings point to, before any booking (step 5).

    - Journeys for every date you use, if your seed made fewer.
    - 20,000 test users, all with one shared, pre-made password hash (made once
      with your hash_password(), never one hash per user: argon2 is slow on purpose).
    - Passengers, if your bookings need a passenger row each.
    Make it safe to run twice, for example by deleting earlier test rows first.
    """
    raise NotImplementedError(
        "TODO(task 7): create the journeys, users and passengers the bookings need"
    )


async def load_context(conn: asyncpg.Connection) -> dict:
    """Read the ids build_row() needs into memory, once, and return them in a dict (steps 6-7).

    For example: the journeys of the 50 busiest routes and of the rest, each
    journey's seat ids (or its train's seat count), the user ids and the fares.
    """
    raise NotImplementedError("TODO(task 7): load the ids that the rows point to")


def build_row(g: int, ctx: dict) -> tuple:
    """Booking number g (0 to total - 1) as one row, its values in COLUMNS order (steps 6-7).

    Give each value its column's Python type (str, int, datetime with a time zone),
    because COPY checks them.

    - Give each g its own (journey, seat) pair, so no pair is booked twice
      (the Stuck section shows one way to do it).
    - A unique 10-character PNR of capital letters and digits. Make it from g
      (for example g in base 36, padded), so two rows never get the same one.
    - Money in paise as int. About 85% confirmed; created_at spread over 180 days;
      the 50 busiest routes get half of the bookings.
    """
    raise NotImplementedError("TODO(task 7): build one valid, realistic booking row")


async def main(total: int) -> None:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        started = time.perf_counter()
        await prepare(conn)
        ctx = await load_context(conn)
        for start in range(0, total, BATCH):
            rows = [build_row(g, ctx) for g in range(start, min(start + BATCH, total))]
            await conn.copy_records_to_table("bookings", records=rows, columns=COLUMNS)
            print(f"loaded {start + len(rows):,} of {total:,} bookings")
        # TODO(task 7): run ANALYZE here, so the planner knows the new table sizes (step 8).
        print(f"done in {time.perf_counter() - started:.0f} seconds")
    finally:
        await conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate RailSeat test bookings.")
    parser.add_argument("--bookings", type=int, default=1_000_000)
    asyncio.run(main(parser.parse_args().bookings))
