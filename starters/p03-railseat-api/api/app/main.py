"""The RailSeat API. Start it from railseat/api/ with:

    uv run fastapi dev app/main.py

Then open http://localhost:8000/docs to try every endpoint.
"""

from fastapi import FastAPI

from app.routers import bookings, trains

app = FastAPI(title="RailSeat API", version="0.1.0")

app.include_router(trains.router)
app.include_router(bookings.router)
