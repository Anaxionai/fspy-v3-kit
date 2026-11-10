"""Refunds: give back part or all of a captured payment."""

import sqlite3
from typing import Any

from mockpay import clock, payments
from mockpay.context import Context
from mockpay.errors import ApiError
from mockpay.events import emit_event
from mockpay.ids import new_id
from mockpay.schemas import RefundCreate

PROCESSED = "processed"  # MockPay refunds at once; there is no other refund status


def create_refund(ctx: Context, request: RefundCreate) -> dict[str, Any]:
    with ctx.db.transaction() as conn:
        payment = conn.execute(
            "SELECT * FROM payments WHERE id = ?", (request.payment_id,)
        ).fetchone()
        if payment is None:
            raise ApiError(404, "payment_not_found", f"No payment with id {request.payment_id}.")
        if payment["status"] != payments.CAPTURED:
            raise ApiError(
                400,
                "payment_not_captured",
                f"Only captured payments can be refunded. This payment is {payment['status']}.",
            )

        # The cap: all refunds together may never be more than the captured amount.
        already = conn.execute(
            "SELECT COALESCE(SUM(amount_paise), 0) FROM refunds WHERE payment_id = ?",
            (request.payment_id,),
        ).fetchone()[0]
        left = payment["amount_paise"] - already
        if request.amount_paise > left:
            raise ApiError(
                400,
                "refund_exceeds_captured",
                f"You asked to refund {request.amount_paise} paise, but only {left} paise of this"
                f" payment can still be refunded (captured {payment['amount_paise']},"
                f" already refunded {already}).",
            )

        refund_id = new_id("rfnd")
        conn.execute(
            "INSERT INTO refunds (id, payment_id, amount_paise, status, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                refund_id,
                request.payment_id,
                request.amount_paise,
                PROCESSED,
                clock.iso(clock.now()),
            ),
        )
        refund = conn.execute(
            "SELECT r.*, p.order_id FROM refunds r JOIN payments p ON p.id = r.payment_id"
            " WHERE r.id = ?",
            (refund_id,),
        ).fetchone()
        emit_event(
            ctx,
            "refund.processed",
            {
                "order_id": refund["order_id"],
                "payment_id": refund["payment_id"],
                "refund_id": refund["id"],
                "amount_paise": refund["amount_paise"],
                "status": refund["status"],
            },
        )
        return refund_json(refund)


def refund_json(refund: sqlite3.Row) -> dict[str, Any]:
    """`refund` must include the payment's order_id (see the JOIN above)."""
    return {
        "id": refund["id"],
        "payment_id": refund["payment_id"],
        "order_id": refund["order_id"],
        "amount_paise": refund["amount_paise"],
        "currency": "INR",
        "status": refund["status"],
        "created_at": refund["created_at"],
    }
