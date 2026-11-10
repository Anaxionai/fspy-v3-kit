"""GET /stations/search: station suggestions with full-text search (P10 add-on, task 11).

Public, like train search: add ("GET", "/stations/search") to PUBLIC_ROUTES and to
your docs/permissions.md. It needs the `name_search` column and its GIN index
(task 11, steps 1-2) in your Station model.
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session

router = APIRouter(tags=["stations"])


class StationOut(BaseModel):
    code: str
    name: str


def to_prefix_query(q: str) -> str | None:
    """Turn what the user typed into a safe prefix tsquery (step 3).

    Keep only letters and digits in each word, add `:*` to each word and join them
    with ` & `: "mum cen" gives "mum:* & cen:*". Return None when nothing is left,
    as for "&|!".
    """
    raise NotImplementedError(
        "TODO(task 11): build the prefix query from cleaned words"
    )


@router.get("/stations/search", response_model=list[StationOut])
async def search_stations(
    q: str = Query(min_length=2, max_length=50),
    session: AsyncSession = Depends(get_session),
):
    """Up to 10 stations, best match first (steps 3-4).

    - Query `name_search @@ to_tsquery('simple', :q)` with a bound parameter, never
      string formatting; order by `ts_rank`, then name.
    - When to_prefix_query() gives None, return an empty list: odd input is never a 500.
    """
    raise NotImplementedError(
        "TODO(task 11): search the stations with the GIN-indexed tsvector"
    )
