"""Ownership checks: a passenger sees and cancels only their own bookings (task 12, step 8).

Each test says what to check. Write the body, then delete its skip line.
Use your P3 data fixture for a journey and a seat, and make Asha, Ravi and the
agent in the test database.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 12)")
async def test_another_passenger_gets_404_and_nothing_changes(client):
    """Asha books a seat. With Ravi's token, GET and DELETE /bookings/{her pnr}
    both get 404, and her booking is still `confirmed`."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
async def test_my_bookings_lists_only_mine(client):
    """After Asha books, GET /bookings returns her booking to her and an empty
    list to Ravi."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
async def test_an_agent_can_open_any_booking(client):
    """With the agent's token, GET /bookings/{Asha's pnr} gets 200."""
    raise NotImplementedError("TODO(task 12): write this test")
