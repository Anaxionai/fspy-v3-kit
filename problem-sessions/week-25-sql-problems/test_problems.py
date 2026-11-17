"""Tests for the week 25 problem session.

Each test builds a small RailSeat database in memory with Python's built-in
`sqlite3` module, runs your query, and compares the rows it returns.
Run them in this folder with: uv run --with pytest pytest -q
"""

import sqlite3
from collections import Counter

import pytest

from problems import QUERY_A, QUERY_B

SCHEMA = """
CREATE TABLE trains (
    train_no TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    from_station TEXT NOT NULL,
    to_station TEXT NOT NULL
);
CREATE TABLE journeys (
    journey_id INTEGER PRIMARY KEY,
    train_no TEXT NOT NULL REFERENCES trains (train_no),
    journey_date TEXT NOT NULL
);
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY,
    journey_id INTEGER NOT NULL REFERENCES journeys (journey_id),
    user_id INTEGER NOT NULL,
    amount_paise INTEGER NOT NULL,
    status TEXT NOT NULL
);
"""

# The sample data in README.md.
TRAINS = [
    ("91001", "Deccan Link", "CSMT", "PUNE"),
    ("91002", "Konkan Breeze", "CSMT", "MAO"),
    ("91003", "Narmada Mail", "BCT", "BPL"),
    ("91004", "Vidarbha Link", "CSMT", "NGP"),
]

JOURNEYS = [
    (1, "91001", "2026-10-01"),
    (2, "91002", "2026-10-01"),
    (3, "91003", "2026-10-01"),
    (4, "91001", "2026-10-02"),
    (5, "91002", "2026-10-02"),
    (6, "91004", "2026-10-02"),
    (7, "91003", "2026-10-03"),
]

BOOKINGS = [
    (1, 1, 105, 45000, "confirmed"),
    (2, 1, 107, 45000, "confirmed"),
    (3, 1, 108, 52000, "confirmed"),
    (4, 1, 101, 45000, "cancelled"),
    (5, 2, 103, 120000, "confirmed"),
    (6, 2, 105, 95000, "confirmed"),
    (7, 2, 107, 120000, "confirmed"),
    (8, 2, 102, 120000, "cancelled"),
    (9, 2, 104, 95000, "cancelled"),
    (10, 3, 101, 60000, "confirmed"),
    (11, 3, 101, 60000, "cancelled"),
    (12, 3, 102, 60000, "cancelled"),
    (13, 3, 104, 75000, "cancelled"),
    (14, 3, 106, 60000, "cancelled"),
    (15, 4, 108, 45000, "confirmed"),
    (16, 4, 101, 45000, "cancelled"),
    (17, 4, 103, 90000, "cancelled"),
    (18, 5, 103, 120000, "confirmed"),
    (19, 5, 105, 95000, "confirmed"),
    (20, 5, 104, 120000, "cancelled"),
    (21, 6, 105, 155000, "confirmed"),
    (22, 6, 107, 155000, "confirmed"),
    (23, 6, 108, 130000, "confirmed"),
    (24, 6, 103, 155000, "confirmed"),
    (25, 6, 102, 155000, "cancelled"),
    (26, 7, 105, 60000, "confirmed"),
    (27, 7, 101, 60000, "cancelled"),
    (28, 7, 103, 75000, "cancelled"),
]


def only(*booking_ids: int) -> list[tuple]:
    """Return the sample bookings with these ids."""
    return [row for row in BOOKINGS if row[0] in booking_ids]


# A larger data set: 4 trains on 10 dates (40 journeys) and 400 bookings from 60 users.
LARGE_JOURNEYS = [
    (100 + 4 * day + position, train[0], f"2026-11-{day + 1:02}")
    for day in range(10)
    for position, train in enumerate(TRAINS)
]
LARGE_BOOKINGS = [
    (
        k + 1,
        LARGE_JOURNEYS[(k * 7 + k // 40) % 40][0],
        300 + (k * 13) % 60,
        30000 + (k * 37) % 50 * 1000,
        "cancelled" if k % 5 == 0 or k % 7 == 0 else "confirmed",
    )
    for k in range(400)
]


def large_expected_a() -> list[tuple]:
    """Work out the answer to problem A for the larger data set in plain Python."""
    count: Counter = Counter()
    paise: Counter = Counter()
    for _, _, user_id, amount, status in LARGE_BOOKINGS:
        if status == "cancelled":
            count[user_id] += 1
            paise[user_id] += amount
    rows = [(user_id, n, paise[user_id]) for user_id, n in count.items() if n >= 3]
    return sorted(rows, key=lambda row: (-row[1], row[0]))


def large_expected_b() -> list[tuple]:
    """Work out the answer to problem B for the larger data set in plain Python."""
    journey = {journey_id: (date, train_no) for journey_id, train_no, date in LARGE_JOURNEYS}
    names = {train_no: name for train_no, name, _, _ in TRAINS}
    count: Counter = Counter()
    for _, journey_id, _, _, status in LARGE_BOOKINGS:
        if status == "confirmed":
            count[journey[journey_id]] += 1
    rows = []
    for date in sorted({date for date, _ in count}):
        on_date = sorted(
            ((train_no, n) for (d, train_no), n in count.items() if d == date),
            key=lambda pair: (-pair[1], pair[0]),
        )
        for day_rank, (train_no, n) in enumerate(on_date[:2], start=1):
            rows.append((date, train_no, names[train_no], n, day_rank))
    return rows


def run(query: str, query_name: str, journeys: list[tuple], bookings: list[tuple]) -> list[tuple]:
    assert query.strip(), f"{query_name} is empty. Write your SQL between the triple quotes in problems.py."
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(SCHEMA)
        db.executemany("INSERT INTO trains VALUES (?, ?, ?, ?)", TRAINS)
        db.executemany("INSERT INTO journeys VALUES (?, ?, ?)", journeys)
        db.executemany("INSERT INTO bookings VALUES (?, ?, ?, ?, ?)", bookings)
        return db.execute(query).fetchall()
    finally:
        db.close()


@pytest.mark.parametrize(
    ("journeys", "bookings", "expected"),
    [
        pytest.param(
            JOURNEYS,
            BOOKINGS,
            [(101, 4, 210000), (102, 3, 335000), (104, 3, 290000)],
            id="readme-1-sample-data",
        ),
        pytest.param(JOURNEYS, [], [], id="readme-2-no-bookings"),
        pytest.param(JOURNEYS, only(8, 12, 25), [(102, 3, 335000)], id="readme-3-one-user"),
        pytest.param(JOURNEYS, only(4), [], id="one-booking"),
        pytest.param(
            JOURNEYS,
            only(1, 6, 19, 21, 26, 4, 16),
            [],
            id="confirmed-bookings-do-not-count",
        ),
        pytest.param(
            JOURNEYS,
            [
                (1, 1, 9, 10000, "cancelled"),
                (2, 2, 9, 20000, "cancelled"),
                (3, 3, 9, 30000, "cancelled"),
                (4, 1, 5, 40000, "cancelled"),
                (5, 2, 5, 40000, "cancelled"),
                (6, 3, 5, 40000, "cancelled"),
                (7, 4, 7, 5000, "cancelled"),
                (8, 5, 7, 5000, "cancelled"),
                (9, 6, 7, 5000, "cancelled"),
                (10, 7, 7, 5000, "cancelled"),
                (11, 1, 8, 90000, "cancelled"),
                (12, 2, 8, 90000, "cancelled"),
            ],
            [(7, 4, 20000), (5, 3, 120000), (9, 3, 60000)],
            id="most-first-then-smaller-user-id",
        ),
        pytest.param(LARGE_JOURNEYS, LARGE_BOOKINGS, large_expected_a(), id="larger-400-bookings"),
    ],
)
def test_query_a(journeys, bookings, expected):
    assert run(QUERY_A, "QUERY_A", journeys, bookings) == expected


@pytest.mark.parametrize(
    ("journeys", "bookings", "expected"),
    [
        pytest.param(
            JOURNEYS,
            BOOKINGS,
            [
                ("2026-10-01", "91001", "Deccan Link", 3, 1),
                ("2026-10-01", "91002", "Konkan Breeze", 3, 2),
                ("2026-10-02", "91004", "Vidarbha Link", 4, 1),
                ("2026-10-02", "91002", "Konkan Breeze", 2, 2),
                ("2026-10-03", "91003", "Narmada Mail", 1, 1),
            ],
            id="readme-1-sample-data",
        ),
        pytest.param(JOURNEYS, [], [], id="readme-2-no-bookings"),
        pytest.param(JOURNEYS, only(10), [("2026-10-01", "91003", "Narmada Mail", 1, 1)], id="readme-3-one-booking"),
        pytest.param(JOURNEYS, only(11), [], id="readme-4-cancelled-does-not-count"),
        pytest.param(
            JOURNEYS,
            only(3, 7, 10, 23),
            [
                ("2026-10-01", "91001", "Deccan Link", 1, 1),
                ("2026-10-01", "91002", "Konkan Breeze", 1, 2),
                ("2026-10-02", "91004", "Vidarbha Link", 1, 1),
            ],
            id="three-trains-tie",
        ),
        pytest.param(
            JOURNEYS,
            only(1, 2, 15, 18, 19, 21),
            [
                ("2026-10-01", "91001", "Deccan Link", 2, 1),
                ("2026-10-02", "91002", "Konkan Breeze", 2, 1),
                ("2026-10-02", "91001", "Deccan Link", 1, 2),
            ],
            id="each-date-ranked-on-its-own",
        ),
        pytest.param(LARGE_JOURNEYS, LARGE_BOOKINGS, large_expected_b(), id="larger-400-bookings"),
    ],
)
def test_query_b(journeys, bookings, expected):
    assert run(QUERY_B, "QUERY_B", journeys, bookings) == expected
