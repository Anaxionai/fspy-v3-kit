"""Checks on the starter's API. The first two pass before you write any code."""

import httpx
import pytest

from app.main import app
from app.models import Point

GOOD_POINT = {"seq": 1, "lat": 18.5204, "lng": 73.8567, "ts": "2026-11-10T10:00:00Z"}


def test_every_endpoint_is_there():
    routes = {
        (method, route.path) for route in app.routes for method in getattr(route, "methods", ())
    }
    assert ("POST", "/riders/{rider_id}/points") in routes
    assert ("GET", "/riders/nearest") in routes
    assert ("POST", "/orders") in routes
    assert ("GET", "/orders/{order_id}") in routes
    assert ("POST", "/orders/{order_id}/status") in routes


def test_a_point_has_the_course_fields():
    assert {"seq", "lat", "lng", "ts"} <= set(Point.model_fields)


@pytest.mark.skip(reason="TODO(task 7): delete this line when Point checks lat and lng")
@pytest.mark.anyio
async def test_a_point_out_of_range_gets_422():
    """No Redis or MongoDB needed: Pydantic refuses the body before the endpoint runs."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        lat_95 = await c.post("/riders/7/points", json={**GOOD_POINT, "lat": 95})
        lng_200 = await c.post("/riders/7/points", json={**GOOD_POINT, "lng": 200})
    assert lat_95.status_code == 422
    assert lng_200.status_code == 422
