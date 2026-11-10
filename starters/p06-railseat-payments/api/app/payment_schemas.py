"""Request and response models for payments (P6 add-on, ready to use).

There is no amount in any request model: RailSeat takes every amount from its
own data (the booking's `fare_paise`), never from the browser.
"""

from pydantic import BaseModel


class OrderIn(BaseModel):
    """POST /payments/orders. Any other field, such as an amount, is ignored."""

    pnr: str


class OrderOut(BaseModel):
    """The reply of POST /payments/orders."""

    order_id: int
    checkout_url: str


class RefundOut(BaseModel):
    """The reply of POST /bookings/{pnr}/refund. React shows
    "Refunded ₹900.00 (fee ₹300.00)" from it."""

    pnr: str
    refund_paise: int
    fee_paise: int
    payment_status: str


class LedgerOut(BaseModel):
    """GET /admin/ledger: each account's balance in paise, and their total (always 0)."""

    balances: dict[str, int]
    total: int


class SettlementImportOut(BaseModel):
    """POST /admin/settlements/import: what one import posted."""

    date: str
    fees_paise: int
    net_payout_paise: int
    # The txn_keys this run posted: empty when the day was imported before.
    posted: list[str]
