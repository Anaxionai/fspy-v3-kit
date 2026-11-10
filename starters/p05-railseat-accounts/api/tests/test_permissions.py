"""Deny by default: every private route needs a token, and /admin needs an admin (task 11).

Each test says what to check. Write the body, then delete its skip line.
The four seed users come from seed/make_users.py; in tests, create them in the
test database instead, with a made-up password.
"""

import pytest

pytestmark = pytest.mark.anyio

# TODO(task 11): the (method, path) pairs anyone may call without a token, as your
# docs/permissions.md says, for example ("GET", "/trains/search"). Task 15 adds the
# two Google routes.
PUBLIC_ROUTES: set[tuple[str, str]] = set()


@pytest.mark.skip(reason="TODO(task 11)")
async def test_every_private_route_needs_a_token(client):
    """Loop over every route of the app (from app.main import app).

    Since FastAPI 0.137, `app.routes` keeps one entry per `include_router()`, not
    the routes inside it. Loop with `fastapi.routing.iter_route_contexts(app.routes)`:
    each item has the full `.path`, the `.methods` and the `APIRoute` in
    `.original_route`. Skip the docs routes, which are not `APIRoute`s.

    For each method of each route that is not in PUBLIC_ROUTES, put a dummy value
    in its path parameters (such as {pnr}), call it with no token and assert 401.
    Also assert that the loop checked your routes: a loop that finds none passes
    without testing anything.
    """
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
async def test_admin_users_is_for_admins_only(client):
    """GET /admin/users: 403 for a passenger and for an agent, 200 for an admin."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
async def test_only_an_admin_can_change_a_role(client):
    """PATCH /admin/users/{id}/role: 403 for an agent, 200 for an admin, and the
    user's role really changed."""
    raise NotImplementedError("TODO(task 11): write this test")
