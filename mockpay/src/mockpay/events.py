"""Webhook events, and the plan for sending them.

Creating an event sends nothing. It writes the event and one or two
"delivery" rows (the plan) in the same transaction as the payment or the
refund. The webhook sender (delivery.py) carries the plan out later. This
is the "outbox pattern": a crash cannot leave a payment without its webhook.

Two things here are deliberate, to copy real gateways:
- some webhooks are late (a random extra delay), and
- some are sent twice (the same event id and the same bytes).
"""

import json
import random
import sqlite3
import time
from typing import Any

from mockpay import clock
from mockpay.config import Settings
from mockpay.context import Context
from mockpay.errors import ApiError
from mockpay.ids import new_id

# Kinds of delivery: why this copy of the event is being sent.
FIRST = "first"
DUPLICATE = "duplicate"  # a deliberate second copy (MOCKPAY_DUPLICATE_RATE)
RESEND = "resend"  # asked for with POST /v1/simulate/webhook or the dashboard

# Delivery statuses.
WAITING = "waiting"
SENDING = "sending"
DELIVERED = "delivered"
GAVE_UP = "gave_up"


def emit_event(ctx: Context, event_type: str, data: dict[str, Any]) -> str:
    """Save a new event and plan its delivery. Returns the event id."""
    event_id = new_id("evt")
    event = {
        "id": event_id,
        "type": event_type,
        "created_at": clock.iso(clock.now()),
        "data": data,
    }
    # This exact text is what MockPay signs and sends, every time.
    body = json.dumps(event, separators=(",", ":"))
    settings, rng = ctx.settings, ctx.rng

    with ctx.db.transaction() as conn:
        conn.execute(
            "INSERT INTO events (id, type, order_id, body, created_at) VALUES (?, ?, ?, ?, ?)",
            (event_id, event_type, data["order_id"], body, event["created_at"]),
        )
        send_at = time.time() + first_delay(settings, rng)
        add_delivery(conn, event_id, FIRST, send_at)
        if rng.random() < settings.duplicate_rate:
            # Real gateways send an event again when they did not see your
            # answer in time. Sometimes the copy arrives at almost the same
            # moment as the first one.
            gap = rng.uniform(0, settings.duplicate_gap_seconds)
            add_delivery(conn, event_id, DUPLICATE, send_at + gap)
    return event_id


def first_delay(settings: Settings, rng: random.Random) -> float:
    """Seconds to wait before the first try: the base delay, plus a random extra for some."""
    delay = settings.delay_seconds
    if rng.random() < settings.late_rate:
        delay += rng.uniform(0, settings.late_max_seconds)
    return delay


def add_delivery(conn: sqlite3.Connection, event_id: str, kind: str, send_at: float) -> int:
    cursor = conn.execute(
        "INSERT INTO deliveries (event_id, kind, status, next_attempt_at) VALUES (?, ?, ?, ?)",
        (event_id, kind, WAITING, send_at),
    )
    assert cursor.lastrowid is not None
    return cursor.lastrowid


def resend_event(ctx: Context, event_id: str, copies: int = 1) -> list[int]:
    """Send a past event again, now, as `copies` separate requests at the same moment."""
    with ctx.db.transaction() as conn:
        if conn.execute("SELECT 1 FROM events WHERE id = ?", (event_id,)).fetchone() is None:
            raise ApiError(404, "event_not_found", f"No event with id {event_id}.")
        now = time.time()
        return [add_delivery(conn, event_id, RESEND, now) for _ in range(copies)]


def find_event(ctx: Context, event_id: str) -> sqlite3.Row | None:
    return ctx.db.query_one("SELECT * FROM events WHERE id = ?", (event_id,))


def list_events(
    ctx: Context, *, limit: int, event_type: str | None, order_id: str | None
) -> list[sqlite3.Row]:
    sql = "SELECT * FROM events WHERE 1 = 1"
    params: list[Any] = []
    if event_type:
        sql += " AND type = ?"
        params.append(event_type)
    if order_id:
        sql += " AND order_id = ?"
        params.append(order_id)
    sql += " ORDER BY rowid DESC LIMIT ?"
    params.append(limit)
    return ctx.db.query(sql, params)


def event_json(ctx: Context, event: sqlite3.Row) -> dict[str, Any]:
    """The event exactly as sent, plus how each copy of it was delivered."""
    deliveries = ctx.db.query(
        "SELECT * FROM deliveries WHERE event_id = ? ORDER BY id", (event["id"],)
    )
    result = json.loads(event["body"])
    result["deliveries"] = [
        {
            "id": delivery["id"],
            "kind": delivery["kind"],
            "status": delivery["status"],
            "attempts": [
                {
                    "attempt_no": attempt["attempt_no"],
                    "url": attempt["url"],
                    "status_code": attempt["status_code"],
                    "error": attempt["error"],
                    "duration_ms": attempt["duration_ms"],
                    "attempted_at": attempt["attempted_at"],
                }
                for attempt in ctx.db.query(
                    "SELECT * FROM delivery_attempts WHERE delivery_id = ? ORDER BY id",
                    (delivery["id"],),
                )
            ],
        }
        for delivery in deliveries
    ]
    return result
