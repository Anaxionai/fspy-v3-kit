"""Twenty bookings for one seat at the same moment: exactly one may win."""

import pytest
from httpx import AsyncClient


@pytest.mark.skip(reason="TODO(task 12)")
@pytest.mark.anyio
async def test_twenty_bookings_for_one_seat(
    client: AsyncClient, one_seat: dict[str, int]
) -> None:
    """Exactly one of 20 bookings sent at once gets 201; the other 19 get 409.

    TODO(task 12):
    - Build 20 `client.post("/bookings", json=...)` calls for the journey and
      seat in `one_seat`, each with its own passenger.
    - Start all 20 together with `asyncio.gather`, so they overlap.
    - Count the status codes: assert exactly one 201 and nineteen 409.
    Delete the @pytest.mark.skip line above when you start.
    """
    raise NotImplementedError("TODO(task 12): send 20 bookings at once, count them")
