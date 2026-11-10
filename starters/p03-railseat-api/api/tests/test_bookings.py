"""Two edge cases of POST /bookings that the chat AI missed (task 12, AI move)."""

import pytest
from httpx import AsyncClient


@pytest.mark.skip(reason="TODO(task 12)")
@pytest.mark.anyio
async def test_edge_case_one(client: AsyncClient, one_seat: dict[str, int]) -> None:
    """TODO(task 12): rename this test after the first edge case it checks.

    Send the request, then assert the status code and the body your API
    should give. Delete the @pytest.mark.skip line above when you start.
    """
    raise NotImplementedError("TODO(task 12): write the first edge case")


@pytest.mark.skip(reason="TODO(task 12)")
@pytest.mark.anyio
async def test_edge_case_two(client: AsyncClient, one_seat: dict[str, int]) -> None:
    """TODO(task 12): rename this test after the second edge case it checks."""
    raise NotImplementedError("TODO(task 12): write the second edge case")
