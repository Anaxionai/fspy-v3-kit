"""Payments: what happens when the customer presses a button on the checkout page."""

import sqlite3
import time
from enum import StrEnum
from typing import Any

from mockpay import clock, orders
from mockpay.context import Context
from mockpay.errors import ApiError
from mockpay.events import emit_event
from mockpay.ids import new_id

# Payment statuses.
PENDING = "pending"  # waiting for the bank (only the "times out" button)
CAPTURED = "captured"  # the money is taken
FAILED = "failed"  # see `reason`: bank_declined or timeout


class Outcome(StrEnum):
    """The three test buttons on the checkout page."""

    SUCCEED = "succeed"  # "Pay with UPI (succeeds)"
    DECLINE = "decline"  # "Pay (bank declines)"
    TIMEOUT = "timeout"  # "Pay (times out)"


def start_payment(ctx: Context, order_id: str, outcome: Outcome) -> sqlite3.Row:
    """Create a pay_... for the order, with the result the customer chose."""
    with ctx.db.transaction() as conn:
        order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if order is None:
            raise ApiError(404, "order_not_found", f"No order with id {order_id}.")
        if order["status"] == orders.PAID:
            raise ApiError(409, "order_already_paid", "This order is already paid.")

        payment_id = new_id("pay")
        now = clock.iso(clock.now())
        new = {
            "id": payment_id,
            "order_id": order_id,
            "amount_paise": order["amount_paise"],
            "created_at": now,
        }

        if outcome is Outcome.SUCCEED:
            insert_payment(conn, **new, status=CAPTURED, captured_at=now)
            conn.execute("UPDATE orders SET status = ? WHERE id = ?", (orders.PAID, order_id))
        elif outcome is Outcome.DECLINE:
            insert_payment(conn, **new, status=FAILED, reason="bank_declined", failed_at=now)
        else:
            # The bank never answers. No webhook now: the webhook sender fails
            # this payment once `fail_after` has passed (see fail_timed_out_payments).
            fail_after = time.time() + ctx.settings.timeout_seconds
            insert_payment(conn, **new, status=PENDING, fail_after=fail_after)

        if outcome is not Outcome.SUCCEED:
            conn.execute(
                "UPDATE orders SET status = ? WHERE id = ? AND status = ?",
                (orders.ATTEMPTED, order_id, orders.CREATED),
            )

        payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
        if payment["status"] == CAPTURED:
            emit_event(ctx, "payment.captured", event_data(payment))
        elif payment["status"] == FAILED:
            emit_event(ctx, "payment.failed", event_data(payment))
    return payment


def insert_payment(conn: sqlite3.Connection, **values: Any) -> None:
    """Insert one payment row. Columns you leave out are NULL."""
    row = {"reason": None, "captured_at": None, "failed_at": None, "fail_after": None, **values}
    conn.execute(
        "INSERT INTO payments (id, order_id, amount_paise, status, reason, created_at,"
        " captured_at, failed_at, fail_after) VALUES (:id, :order_id, :amount_paise, :status,"
        " :reason, :created_at, :captured_at, :failed_at, :fail_after)",
        row,
    )


def fail_timed_out_payments(ctx: Context) -> int:
    """Fail every pending payment whose bank never answered. Returns how many."""
    with ctx.db.transaction() as conn:
        due = conn.execute(
            "SELECT id FROM payments WHERE status = ? AND fail_after <= ?",
            (PENDING, time.time()),
        ).fetchall()
        now = clock.iso(clock.now())
        for row in due:
            conn.execute(
                "UPDATE payments SET status = ?, reason = ?, failed_at = ? WHERE id = ?",
                (FAILED, "timeout", now, row["id"]),
            )
            payment = conn.execute("SELECT * FROM payments WHERE id = ?", (row["id"],)).fetchone()
            emit_event(ctx, "payment.failed", event_data(payment))
    return len(due)


def event_data(payment: sqlite3.Row) -> dict[str, Any]:
    """The `data` part of a payment.captured or payment.failed webhook."""
    data: dict[str, Any] = {
        "order_id": payment["order_id"],
        "payment_id": payment["id"],
        "amount_paise": payment["amount_paise"],
        "status": payment["status"],
    }
    if payment["reason"]:
        data["reason"] = payment["reason"]
    return data


def find_payment(ctx: Context, payment_id: str) -> sqlite3.Row | None:
    return ctx.db.query_one("SELECT * FROM payments WHERE id = ?", (payment_id,))


def payments_for_order(ctx: Context, order_id: str) -> list[sqlite3.Row]:
    return ctx.db.query("SELECT * FROM payments WHERE order_id = ? ORDER BY rowid", (order_id,))


def payment_json(ctx: Context, payment: sqlite3.Row) -> dict[str, Any]:
    refunds = ctx.db.query(
        "SELECT id, amount_paise FROM refunds WHERE payment_id = ? ORDER BY rowid",
        (payment["id"],),
    )
    return {
        "id": payment["id"],
        "order_id": payment["order_id"],
        "amount_paise": payment["amount_paise"],
        "currency": "INR",
        "status": payment["status"],
        "reason": payment["reason"],
        "amount_refunded_paise": sum(r["amount_paise"] for r in refunds),
        "refunds": [r["id"] for r in refunds],
        "created_at": payment["created_at"],
        "captured_at": payment["captured_at"],
        "failed_at": payment["failed_at"],
    }
