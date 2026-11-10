"""Admin routes for the ledger and MockPay's settlement report (P6 add-on, task 12).

Include it in app/main.py in task 12, once it is admin-only (see STARTER.md).
"""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.payment_schemas import LedgerOut, SettlementImportOut
from app.services.mockpay import MockPayClient, get_mockpay

# TODO(task 12): make the whole router admin-only, as in P5: the APIRouter setting
# `dependencies=[...]` with your require_role("admin").
router = APIRouter(prefix="/admin", tags=["ledger"])


@router.get("/ledger", response_model=LedgerOut)
async def ledger(session: AsyncSession = Depends(get_session)):
    """Each account's balance and the total, which must be 0 (task 12, step 6)."""
    raise NotImplementedError("TODO(task 12): return balances() and their total")


@router.post("/settlements/import", response_model=SettlementImportOut)
async def import_settlements(
    day: date = Query(alias="date"),
    mockpay: MockPayClient = Depends(get_mockpay),
    session: AsyncSession = Depends(get_session),
):
    """Import one IST day of MockPay's settlement report (task 12, steps 7-9).

    Read it with `mockpay.settlement_report(day)`, post it with `import_settlement()`
    and commit once. Running it twice for the same day posts nothing new.
    """
    raise NotImplementedError("TODO(task 12): read the report and post it once")
