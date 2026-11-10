"""TiffinTrack's WebSocket server: it forwards live messages from Redis pub/sub to browsers.

It is a separate program from the API, so you can run many copies behind one address.
Run it from the tiffintrack/ folder:  uv run fastapi dev ws/server.py --port 8001
For the fan-out check in task 8, start a second copy with --port 8002.
Watch it:  uv run websockets ws://localhost:8001/ws/riders

Your code here will need json, and httpx for the order feed (task 18).
"""

import os
from contextlib import asynccontextmanager

import redis.asyncio
from fastapi import FastAPI, WebSocket

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
API_URL = os.environ.get("API_URL", "http://localhost:8000")  # the order feed reads orders here

# One Redis client for the whole server. Each WebSocket opens its own pub/sub with r.pubsub().
r = redis.asyncio.from_url(REDIS_URL, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await r.aclose()


app = FastAPI(title="TiffinTrack live", lifespan=lifespan)


@app.websocket("/ws/riders")
async def riders_feed(websocket: WebSocket) -> None:
    """The dispatcher feed: every rider's points, live, as the JSON text the API published.

    Messages come from the Redis channels rider:1, rider:2 and so on (the pattern rider:*).
    Edge case: when the browser leaves (WebSocketDisconnect), stop and end the subscription.
    TODO(task 8): accept the socket and forward every message from rider:* to it.
    TODO(task 9): when a browser connects, first subscribe, then send the latest point of
      every rider from riders:latest. In that order, no point is lost between the two.
    """
    raise NotImplementedError("TODO(task 8): forward every rider:* message to this socket")


@app.websocket("/ws/orders/{order_id}")
async def order_feed(websocket: WebSocket, order_id: str) -> None:
    """One customer's order, live: its status changes and its rider's points.

    Read the order (with its rider_id) from GET {API_URL}/orders/{order_id}.
    Messages come from the channels order:{order_id} and rider:{rider_id}.
    On connect, subscribe first, then send a snapshot:
      {"type": "snapshot", "timeline": [...], "rider": <the rider's latest point, or null>}
    Edge cases: an unknown order; a browser that leaves; an order that becomes "delivered"
    (close the socket with code 1000).
    TODO(task 18): write it.
    """
    raise NotImplementedError("TODO(task 18): forward one order's status changes and rider points")
