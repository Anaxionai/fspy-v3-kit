"""The app starts and still offers RailSeat's endpoints. Needs no database."""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_app_lists_the_railseat_endpoints(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    # RailSeat web (P4) calls these paths, so keep them.
    assert "/trains/search" in paths
    assert "/journeys/{journey_id}/seats" in paths
    assert "/bookings" in paths
    assert "/bookings/{pnr}" in paths
