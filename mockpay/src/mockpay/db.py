"""SQLite storage: the tables, and a small helper for transactions.

MockPay is one process with one SQLite connection. A lock lets only one
piece of code use the connection at a time, so web requests and the
webhook sender never get in each other's way.

Rule for this code base: never `await` inside a transaction. A transaction
holds the lock, and everything else would wait for it.
"""

from __future__ import annotations

import sqlite3
import threading
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id           TEXT PRIMARY KEY,                -- order_...
    amount_paise INTEGER NOT NULL CHECK (amount_paise > 0),
    currency     TEXT NOT NULL,
    receipt      TEXT NOT NULL,                   -- the merchant's own reference
    notes        TEXT NOT NULL,                   -- a JSON object
    return_url   TEXT,                            -- where checkout sends the customer back
    status       TEXT NOT NULL,                   -- created | attempted | paid
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id           TEXT PRIMARY KEY,                -- pay_...
    order_id     TEXT NOT NULL REFERENCES orders (id),
    amount_paise INTEGER NOT NULL,
    status       TEXT NOT NULL,                   -- pending | captured | failed
    reason       TEXT,                            -- bank_declined | timeout (failed only)
    created_at   TEXT NOT NULL,
    captured_at  TEXT,
    failed_at    TEXT,
    fail_after   REAL                             -- Unix time when a pending payment fails
);

CREATE TABLE IF NOT EXISTS refunds (
    id           TEXT PRIMARY KEY,                -- rfnd_...
    payment_id   TEXT NOT NULL REFERENCES payments (id),
    amount_paise INTEGER NOT NULL CHECK (amount_paise > 0),
    status       TEXT NOT NULL,                   -- processed
    created_at   TEXT NOT NULL
);

-- Every webhook event, with the exact JSON text that is signed and sent.
-- type is payment.captured, payment.failed or refund.processed.
CREATE TABLE IF NOT EXISTS events (
    id         TEXT PRIMARY KEY,                  -- evt_...
    type       TEXT NOT NULL,
    order_id   TEXT NOT NULL,
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- The "outbox": one row for each copy of an event that must be sent.
CREATE TABLE IF NOT EXISTS deliveries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id        TEXT NOT NULL REFERENCES events (id),
    kind            TEXT NOT NULL,                -- first | duplicate | resend
    status          TEXT NOT NULL,                -- waiting | sending | delivered | gave_up
    attempts        INTEGER NOT NULL DEFAULT 0,
    next_attempt_at REAL                          -- Unix time of the next try
);

-- One row for each HTTP request MockPay made to the webhook URL.
CREATE TABLE IF NOT EXISTS delivery_attempts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id  INTEGER NOT NULL REFERENCES deliveries (id),
    attempt_no   INTEGER NOT NULL,
    url          TEXT NOT NULL,
    status_code  INTEGER,                         -- NULL when there was no HTTP answer
    error        TEXT,
    duration_ms  INTEGER NOT NULL,
    attempted_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
    scope         TEXT NOT NULL,                  -- orders | refunds
    key           TEXT NOT NULL,
    request_hash  TEXT NOT NULL,                  -- SHA-256 of the request body
    response_body TEXT NOT NULL,                  -- the JSON MockPay answered with
    created_at    TEXT NOT NULL,
    PRIMARY KEY (scope, key)
);

CREATE INDEX IF NOT EXISTS payments_by_order ON payments (order_id);
CREATE INDEX IF NOT EXISTS refunds_by_payment ON refunds (payment_id);
CREATE INDEX IF NOT EXISTS deliveries_by_event ON deliveries (event_id);
CREATE INDEX IF NOT EXISTS deliveries_due ON deliveries (status, next_attempt_at);
CREATE INDEX IF NOT EXISTS attempts_by_delivery ON delivery_attempts (delivery_id);
"""


class Database:
    def __init__(self, path: str) -> None:
        # isolation_level=None: we start and end transactions ourselves (below).
        self._conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self._conn.row_factory = sqlite3.Row  # rows can be read like dicts: row["id"]
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(SCHEMA)
        self._lock = threading.RLock()
        self._depth = 0  # how many transaction blocks are open (they may be nested)

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Run a block of SQL as one transaction: all of it is saved, or none of it.

        Blocks may be nested. Only the outermost block commits, so a function
        that opens a transaction can be called from inside another one.
        """
        with self._lock:
            outermost = self._depth == 0
            if outermost:
                self._conn.execute("BEGIN IMMEDIATE")
            self._depth += 1
            try:
                yield self._conn
            except BaseException:
                self._depth -= 1
                if outermost:
                    self._conn.execute("ROLLBACK")
                raise
            self._depth -= 1
            if outermost:
                self._conn.execute("COMMIT")

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._conn.execute(sql, params).fetchall()

    def query_one(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Row | None:
        with self._lock:
            return self._conn.execute(sql, params).fetchone()

    def close(self) -> None:
        with self._lock:
            self._conn.close()
