"""Test set-up shared by every test file. Run the tests from tiffintrack/:  uv run pytest -q

Tests use their own MongoDB database, tiffintrack_test, so they never touch your real data.
Tests that use the `client` or `db` fixture need the cloud lab: Redis (core profile) and,
from task 15, MongoDB (mongo profile).
"""

import os
from collections.abc import AsyncIterator

import httpx
import pytest

# Settings are read once, when the app is first imported, so set them before any test imports it.
os.environ["MONGO_DB"] = "tiffintrack_test"
os.environ.setdefault("MONGO_URL", "mongodb://localhost:27017")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
API_URL = os.environ.get("API_URL", "http://localhost:8000")


@pytest.fixture
def anyio_backend() -> str:
    """Run async tests on asyncio. Mark them with @pytest.mark.anyio, as in P3."""
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    """Calls the API inside the test process, after its start-up code has run.

    The API's Redis and MongoDB clients are made inside the test, so each test has its own.
    """
    from app.main import app

    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
            yield c


@pytest.fixture
async def db(client: httpx.AsyncClient):
    """The test database, emptied before each test. Its indexes stay (the API makes them at start-up)."""
    from app.db import get_db

    database = get_db()
    for name in ("orders", "points", "riders"):
        await database[name].delete_many({})
    return database


@pytest.fixture
async def live_client() -> AsyncIterator[httpx.AsyncClient]:
    """Calls the API that you started in another terminal (the race test in task 9 uses it)."""
    async with httpx.AsyncClient(base_url=API_URL, timeout=10) as c:
        try:
            await c.get("/openapi.json")
        except httpx.ConnectError:
            pytest.fail(
                f"Nothing answers on {API_URL}. Start it: uv run fastapi dev api/app/main.py"
            )
        yield c


@pytest.fixture
def order_body() -> dict:
    """A valid body for POST /orders: a restaurant at Shaniwar Wada, delivering to Karve Road."""
    return {
        "customer": {"name": "Asha Kulkarni", "phone": "9876543210"},
        "restaurant": {"name": "Shaniwar Thali House", "lat": 18.5195, "lng": 73.8553},
        "address": {"label": "Flat 4B, Karve Road", "lat": 18.5074, "lng": 73.8077},
        "items": [{"name": "Veg thali", "qty": 2, "price_paise": 18000}],
    }


@pytest.fixture
async def free_rider(db, order_body: dict) -> int:
    """Rider 1, free, about 100 m north of order_body's restaurant. Returns the rider id.

    From task 19, POST /orders needs a free rider within 5 km of the restaurant,
    so add this fixture to every test that places an order.
    """
    restaurant = order_body["restaurant"]
    location = {"type": "Point", "coordinates": [restaurant["lng"], restaurant["lat"] + 0.0009]}
    await db.riders.insert_one({"_id": 1, "status": "free", "location": location})
    return 1
