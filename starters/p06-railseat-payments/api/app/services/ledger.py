"""The double-entry ledger (P6 add-on, task 12).

Every movement of money is one transfer: two `LedgerEntry` rows with the same
`txn_key`, +amount on the debit account and -amount on the credit account, so
every transfer sums to 0 and so do all balances together.
Rows are never updated or deleted: a correction is a new transfer the other way.
Import `LedgerEntry` from app.models when you write these. Nothing here commits.
"""

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

# The only accounts RailSeat uses (step 3).
ACCOUNTS = (
    "mockpay_clearing",
    "bank",
    "ticket_sales",
    "cancellation_fees",
    "gateway_fees",
)


async def post(
    session: AsyncSession,
    txn_key: str,
    debit: str,
    credit: str,
    amount_paise: int,
    order_id: int | None = None,
) -> None:
    """Add one transfer as two rows: +amount_paise to `debit`, -amount_paise to `credit` (step 2).

    - An account not in ACCOUNTS, or an amount of 0 or less, raises ValueError (step 3).
    - The unique (`txn_key`, `account`) constraint refuses a second copy of a transfer.
    - Examples of keys: "capture:<payment id>", "refund:<refund id>", "fees:<date>".
    """
    raise NotImplementedError("TODO(task 12): add the two rows of one transfer")


async def balances(session: AsyncSession) -> dict[str, int]:
    """Each account's balance in paise: the sum of its rows, with GROUP BY (step 6).

    Accounts with no rows are left out. The values always add up to 0.
    """
    raise NotImplementedError("TODO(task 12): sum the rows of each account")


async def import_settlement(
    session: AsyncSession, day: date, report: dict
) -> list[str]:
    """Post one IST day's settlement report from MockPay; return the txn_keys posted (steps 8-9).

    - `fees:<day>`: debit `gateway_fees`, credit `mockpay_clearing`, `fees_paise`.
    - `payout:<day>`: debit `bank`, credit `mockpay_clearing`, `net_payout_paise`.
      A negative payout swaps the two accounts and posts the amount without its sign.
    - Skip an amount of 0, and skip a `txn_key` that is already in the ledger, so
      importing the same day twice adds nothing.
    """
    raise NotImplementedError("TODO(task 12): post the day's fees and payout once")
