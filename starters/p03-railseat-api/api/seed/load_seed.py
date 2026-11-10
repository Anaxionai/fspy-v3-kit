"""Load the course kit's RailSeat CSV files into your tables.

Run it from railseat/api/, so Python can find the `app` package:

    uv run python -m seed.load_seed ~/fspy-v3-kit/data/railseat

The kit's data/railseat/README.md explains every column of the four files.
"""

import asyncio
from pathlib import Path


def read_csv(folder: Path, name: str) -> list[dict[str, str]]:
    """Return the rows of `folder/name` as dictionaries, one per line.

    TODO(task 9): open the file with encoding="utf-8" and newline="", and read
    it with `csv.DictReader`. Every value comes back as text, so convert
    numbers, times and dates before you insert them.
    """
    raise NotImplementedError("TODO(task 9): read one CSV file")


async def main() -> None:
    """Fill every RailSeat table from the CSV files in the folder in sys.argv[1].

    TODO(task 9):
    - Start with one `TRUNCATE ... RESTART IDENTITY CASCADE` of all eight
      tables, so the loader can run twice.
    - Read stations.csv, trains.csv, schedules.csv and coaches.csv.
    - Insert parents before children: stations and trains first, then stops
      and coaches.
    - Create every seat of each coach, numbered from 1 to its seat count.
    - Create one journey per train for each of the next 60 days, starting today.
    - Commit, then print how many rows each table got.
    Use a session from `SessionLocal` in app/db.py.
    """
    raise NotImplementedError("TODO(task 9): load the seed data")


if __name__ == "__main__":
    asyncio.run(main())
