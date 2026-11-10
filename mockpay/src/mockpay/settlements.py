"""The daily settlement report: what MockPay pays out to the merchant for one day.

MockPay keeps a fee of 2% of each captured payment. Refunds go back to
customers out of the merchant's money. So for one day (IST):

    net payout = captured - refunded - fees

The fee is worked out for each payment and then added up. MockPay does not
give the fee back when a payment is refunded. A day with more refunds than
payments has a negative net payout: the merchant owes MockPay.

A reconciliation job compares these numbers with the merchant's own ledger.
"""

from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any

from mockpay.context import Context
from mockpay.money import FEE_PERCENT, fee_paise


def settlement_report(ctx: Context, day: date) -> dict[str, Any]:
    """The report for one IST date.

    Times are stored as IST text ("2026-11-10T15:45:30+05:30"), so the first
    10 characters are the IST date.
    """
    day_text = day.isoformat()
    captured = ctx.db.query(
        "SELECT id, order_id, amount_paise, captured_at FROM payments"
        " WHERE status = 'captured' AND substr(captured_at, 1, 10) = ?"
        " ORDER BY captured_at, rowid",
        (day_text,),
    )
    refunds = ctx.db.query(
        "SELECT r.id, r.payment_id, p.order_id, r.amount_paise, r.created_at"
        " FROM refunds r JOIN payments p ON p.id = r.payment_id"
        " WHERE substr(r.created_at, 1, 10) = ?"
        " ORDER BY r.created_at, r.rowid",
        (day_text,),
    )
    return build_report(day, captured, refunds)


def build_report(
    day: date, captured: Sequence[Mapping[str, Any]], refunds: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """The maths, kept apart from the database so that it is easy to test."""
    payment_lines = [
        {
            "payment_id": p["id"],
            "order_id": p["order_id"],
            "amount_paise": p["amount_paise"],
            "fee_paise": fee_paise(p["amount_paise"]),
            "captured_at": p["captured_at"],
        }
        for p in captured
    ]
    refund_lines = [
        {
            "refund_id": r["id"],
            "payment_id": r["payment_id"],
            "order_id": r["order_id"],
            "amount_paise": r["amount_paise"],
            "created_at": r["created_at"],
        }
        for r in refunds
    ]
    captured_paise = sum(line["amount_paise"] for line in payment_lines)
    refunded_paise = sum(line["amount_paise"] for line in refund_lines)
    fees_paise = sum(line["fee_paise"] for line in payment_lines)
    return {
        "date": day.isoformat(),
        "currency": "INR",
        "fee_percent": FEE_PERCENT,
        "payments": payment_lines,
        "refunds": refund_lines,
        "captured_paise": captured_paise,
        "refunded_paise": refunded_paise,
        "fees_paise": fees_paise,
        "net_payout_paise": captured_paise - refunded_paise - fees_paise,
    }
