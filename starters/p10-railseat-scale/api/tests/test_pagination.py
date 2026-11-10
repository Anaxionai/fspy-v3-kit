"""Keyset pagination of GET /admin/bookings (task 10, step 10).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 10)")
async def test_following_next_cursor_returns_every_booking_once(client):
    """Make 45 bookings in the test database (some with the same created_at) and an
    admin token. Follow next_cursor with limit=20: 20, 20 and 5 rows, 45 different
    PNRs, newest first, and the last next_cursor is None."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10)")
async def test_a_bad_cursor_gets_400(client):
    """GET /admin/bookings?after=not-a-cursor gets 400, never 500."""
    raise NotImplementedError("TODO(task 10): write this test")
