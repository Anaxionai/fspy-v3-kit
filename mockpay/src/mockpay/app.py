"""Builds the MockPay web app."""

import random
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from mockpay import __version__
from mockpay.config import Settings
from mockpay.context import Context
from mockpay.db import Database
from mockpay.delivery import DeliveryWorker
from mockpay.errors import ApiError, handle_api_error, handle_validation_error
from mockpay.routes import api, pages

DESCRIPTION = """
MockPay is a **pretend** payment gateway for the FSPY-V3 course.
It is not a real payment gateway: never send real card or UPI details.

Every `/v1` endpoint needs `Authorization: Bearer <MOCKPAY_API_KEY>`
(default `mp_test_key`). Press **Authorize** to try them here.
"""


def create_app(settings: Settings | None = None) -> FastAPI:
    """Make the app. Tests pass their own settings; normally they come from the environment."""
    settings = settings if settings is not None else Settings.from_env()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # Runs once at start-up (before `yield`) and once at shut-down (after it).
        ctx = Context(settings=settings, db=Database(settings.db_path), rng=random.Random())
        app.state.ctx = ctx
        # trust_env=False: never send webhooks through a proxy from the environment.
        async with httpx.AsyncClient(
            timeout=settings.answer_timeout_seconds, trust_env=False
        ) as client:
            worker = DeliveryWorker(ctx, client)
            worker.start()
            try:
                yield
            finally:
                await worker.stop()
                ctx.db.close()

    app = FastAPI(
        title="MockPay",
        version=__version__,
        description=DESCRIPTION,
        lifespan=lifespan,
    )
    app.add_exception_handler(ApiError, handle_api_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.include_router(api.router)
    app.include_router(pages.router)
    return app
