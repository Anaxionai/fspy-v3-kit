"""Tests for creating and following links (task 7). They use the client fixture from conftest.py."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 7)")
async def test_create_link_returns_201(client: AsyncClient) -> None:
    """POST /links with a valid target_url: 201, a 7-character code, and a short_url that ends with it."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7)")
async def test_follow_link_returns_302(client: AsyncClient) -> None:
    """Create a link, then GET /<code>: 302, with the target in the Location header."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7)")
async def test_unknown_code_returns_404(client: AsyncClient) -> None:
    """GET a code that was never created: 404."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7)")
async def test_clicks_rise(client: AsyncClient) -> None:
    """Follow a link twice: GET /links/<code>/stats shows clicks 2.

    In task 19 the worker counts clicks instead, so this test changes then (see test_clicks.py).
    """
    raise NotImplementedError("TODO(task 7): write this test")
