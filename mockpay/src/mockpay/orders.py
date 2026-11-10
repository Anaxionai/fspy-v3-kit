"""Orders: what the merchant wants to be paid, before any payment is tried."""

import json
import sqlite3
from typing import Any

from mockpay import clock
from mockpay.context import Context
from mockpay.ids import new_id
from mockpay.schemas import OrderCreate

# Order statuses.
CREATED = "created"  # no payment tried yet
ATTEMPTED = "attempted"  # a payment was tried; it failed, or the bank has not answered
PAID = "paid"  # a payment was captured


def create_order(ctx: Context, request: OrderCreate) -> dict[str, Any]:
    order_id = new_id("order")
    with ctx.db.transaction() as conn:
        conn.execute(
            "INSERT INTO orders"
            " (id, amount_paise, currency, receipt, notes, return_url, status, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                order_id,
                request.amount_paise,
                request.currency,
                request.receipt,
                json.dumps(request.notes or {}),
                request.return_url,
                CREATED,
                clock.iso(clock.now()),
            ),
        )
    order = find_order(ctx, order_id)
    assert order is not None
    return order_json(ctx, order)


def find_order(ctx: Context, order_id: str) -> sqlite3.Row | None:
    return ctx.db.query_one("SELECT * FROM orders WHERE id = ?", (order_id,))


def checkout_url(ctx: Context, order_id: str) -> str:
    return f"{ctx.settings.public_url}/checkout/{order_id}"


def order_json(ctx: Context, order: sqlite3.Row) -> dict[str, Any]:
    payments = ctx.db.query(
        "SELECT id, status, amount_paise FROM payments WHERE order_id = ? ORDER BY rowid",
        (order["id"],),
    )
    return {
        "id": order["id"],
        "amount_paise": order["amount_paise"],
        "currency": order["currency"],
        "receipt": order["receipt"],
        "notes": json.loads(order["notes"]),
        "status": order["status"],
        "amount_paid_paise": sum(p["amount_paise"] for p in payments if p["status"] == "captured"),
        "attempts": len(payments),
        "payments": [p["id"] for p in payments],
        "return_url": order["return_url"],
        "checkout_url": checkout_url(ctx, order["id"]),
        "created_at": order["created_at"],
    }
