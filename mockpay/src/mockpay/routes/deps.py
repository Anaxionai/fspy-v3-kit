"""Shared FastAPI dependencies for the routes."""

from typing import Annotated

from fastapi import Depends, Request

from mockpay.context import Context


def get_context(request: Request) -> Context:
    """The Context made at start-up (see app.py)."""
    return request.app.state.ctx


# Write `ctx: Ctx` in a route to receive the Context.
Ctx = Annotated[Context, Depends(get_context)]
