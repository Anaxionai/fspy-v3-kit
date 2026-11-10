"""The data behind GET /dashboard: the latest rows of every table."""

import time
from typing import Any

from mockpay.context import Context
from mockpay.events import SENDING, WAITING


def dashboard_data(ctx: Context, limit: int = 50) -> dict[str, Any]:
    db = ctx.db
    waiting = db.query(
        "SELECT d.id, d.event_id, d.kind, d.status, d.attempts, d.next_attempt_at, e.type"
        " FROM deliveries d JOIN events e ON e.id = d.event_id"
        " WHERE d.status IN (?, ?) ORDER BY d.next_attempt_at, d.id",
        (WAITING, SENDING),
    )
    now = time.time()
    return {
        "settings": ctx.settings,
        "orders": db.query("SELECT * FROM orders ORDER BY rowid DESC LIMIT ?", (limit,)),
        "payments": db.query(
            "SELECT p.*, (SELECT COALESCE(SUM(r.amount_paise), 0) FROM refunds r"
            " WHERE r.payment_id = p.id) AS refunded_paise"
            " FROM payments p ORDER BY p.rowid DESC LIMIT ?",
            (limit,),
        ),
        "refunds": db.query(
            "SELECT r.*, p.order_id FROM refunds r JOIN payments p ON p.id = r.payment_id"
            " ORDER BY r.rowid DESC LIMIT ?",
            (limit,),
        ),
        "events": db.query(
            "SELECT e.*,"
            " (SELECT COUNT(*) FROM deliveries d WHERE d.event_id = e.id) AS copies,"
            " (SELECT COUNT(*) FROM deliveries d WHERE d.event_id = e.id"
            "  AND d.status = 'delivered') AS delivered"
            " FROM events e ORDER BY e.rowid DESC LIMIT ?",
            (limit,),
        ),
        "waiting": [
            {**dict(row), "due_in": max(0.0, (row["next_attempt_at"] or now) - now)}
            for row in waiting
        ],
        "attempts": db.query(
            "SELECT a.*, d.kind, d.event_id, e.type FROM delivery_attempts a"
            " JOIN deliveries d ON d.id = a.delivery_id JOIN events e ON e.id = d.event_id"
            " ORDER BY a.id DESC LIMIT ?",
            (limit * 2,),
        ),
    }
