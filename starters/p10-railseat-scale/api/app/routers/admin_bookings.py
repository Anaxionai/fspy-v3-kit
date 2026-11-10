"""GET /admin/bookings: every booking, newest first, page by page (P10 add-on, task 10).

Use it only if you have no admin list of all bookings yet (step 1). Include it in
app/main.py once it is admin-only (see STARTER.md).
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.pagination import BookingPage

# TODO(task 10): admin only, as in P5: give APIRouter the setting `dependencies=[...]`
# with your require_role("admin").
router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/bookings", response_model=BookingPage)
async def all_bookings(
    limit: int = Query(20, ge=1, le=100),
    after: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    """One page of bookings, ordered by `created_at DESC, id DESC` (steps 3-4).

    - No `after`: the first page. With `after`: only rows whose (created_at, id) is
      below the cursor's pair, as the brief's step 3 shows. Never OFFSET.
    - `next_cursor` comes from the page's last row, or is None when no row is left.
    - A bad cursor gets 400. Time OFFSET first in psql (step 2), for perf.md.
    """
    raise NotImplementedError(
        "TODO(task 10): page with a keyset condition and return next_cursor"
    )
