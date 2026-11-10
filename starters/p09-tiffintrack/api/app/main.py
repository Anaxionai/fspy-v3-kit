"""TiffinTrack's API.

Run it from the tiffintrack/ folder:  uv run fastapi dev api/app/main.py
Then open http://localhost:8000/docs to try every endpoint.

The endpoints call the functions in points.py, riders.py and orders.py.
Import the modules you call, for example: from app import orders, points, riders
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import db
from app.models import OrderIn, Point, StatusIn

# Log lines appear in the terminal where the API runs, for example log.info("dropped ...").
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s: %(message)s")
log = logging.getLogger("tiffintrack")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start-up code runs before `yield`; shut-down code runs after it."""
    await db.open_connections()
    await db.create_indexes()  # does nothing until task 16
    yield
    await db.close_connections()


app = FastAPI(title="TiffinTrack API", lifespan=lifespan)

# The web app on http://localhost:5173 may call this API from the browser (CORS, as in P4).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/riders/{rider_id}/points")
async def post_point(rider_id: int, point: Point) -> dict:
    """Receive one GPS point from a rider (the simulator). Answers {"accepted": true} or false.

    TODO(task 7): answer {"accepted": True} for now.
    TODO(task 8): publish every valid point (points.publish_point).
    TODO(task 9): drop repeated and old points before you publish (points.is_new_point).
      A new point: publish it, remember it as the rider's latest, and answer {"accepted": True}.
      An old or repeated point: log the rider id and seq, and answer {"accepted": False}.
    TODO(task 16): store every valid point in MongoDB, late ones too (points.store_point).
      For a new point only, also update the rider's document (points.update_rider).
    """
    raise NotImplementedError("TODO(task 7): accept the point")


@app.get("/riders/nearest")
async def get_nearest_rider(lat: float, lng: float) -> dict:
    """The nearest free rider within 5 km of (lat, lng): {"rider_id": 7, "lat": ..., "lng": ...}.

    TODO(task 19): check that lat and lng are in range, as in Point (Query(ge=..., le=...)).
      Answer 404 with "No free rider within 5 km" when nobody free is in range (riders.py).
    """
    raise NotImplementedError("TODO(task 19): find the nearest free rider")


@app.post("/orders", status_code=201)
async def post_order(order: OrderIn) -> dict:
    """Place a new order. Answers {"id": "<the new order's id>"}.

    TODO(task 15): store it with orders.create_order and answer with its id.
    """
    raise NotImplementedError("TODO(task 15): place the order")


@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> dict:
    """One order, with its id as the string field "id". 404 for an unknown or malformed id.

    TODO(task 15): read it with orders.find_order.
    TODO(task 20): for an order that is not delivered, add distance_m and eta_minutes
      (orders.arrival_estimate).
    """
    raise NotImplementedError("TODO(task 15): read the order")


@app.post("/orders/{order_id}/status")
async def post_order_status(order_id: str, body: StatusIn) -> dict:
    """Move an order to its next status, for example {"status": "picked_up"}. 409 if not allowed.

    TODO(task 18): change it with orders.change_status and answer with the changed order.
    """
    raise NotImplementedError("TODO(task 18): change the order's status")
