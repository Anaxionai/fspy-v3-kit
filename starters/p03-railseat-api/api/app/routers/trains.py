"""Train search and seat lists: GET /trains/search and GET /journeys/{journey_id}/seats."""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import SeatOut, TrainResult

router = APIRouter(tags=["trains"])


# TODO(task 13): give `from` and `to` a `pattern` of ^[A-Z]{2,5}$, a `description`
#   and `examples=["NDLS"]`. Add `limit` (1 to 50, default 20) and `offset`
#   (0 or more, default 0) as query parameters.
@router.get("/trains/search")
async def search_trains(
    # `from` is a Python keyword, so this parameter is named from_.
    from_: str = Query(alias="from"),
    to: str = Query(),
    travel_date: date = Query(alias="date"),
    session: AsyncSession = Depends(get_session),
) -> list[TrainResult]:
    """Find the journeys on `travel_date` whose train stops at `from_` before `to`.

    Example: GET /trains/search?from=NDLS&to=BCT&date=2026-12-01

    TODO(task 10):
    - Copy your query from sql/search.sql into `text()`, with bound parameters
      such as `:from_code`. Never build SQL with f-strings.
    - Run it with `await session.execute(...)` and return one TrainResult per row.
    - No journey on that date is not an error: return an empty list.
    TODO(task 13):
    - If `from_` equals `to`, answer 422 with a message that names the problem.
    - Add ORDER BY the departure time, then `LIMIT :limit OFFSET :offset`.
    """
    raise NotImplementedError("TODO(task 10): run the search and return the trains")


@router.get("/journeys/{journey_id}/seats")
async def list_seats(
    journey_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[SeatOut]:
    """List every seat of the journey's train, with `booked` true or false.

    TODO(task 10):
    - Raise HTTPException(404, ...) if the journey does not exist.
    - Copy your query from sql/seats.sql into `text()`, with `:journey_id` bound.
    - Return one SeatOut per seat. Only confirmed bookings make a seat booked.
    """
    raise NotImplementedError("TODO(task 10): list the seats of one journey")
