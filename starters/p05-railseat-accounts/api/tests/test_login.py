"""Login, the refresh cookie, /auth/me and logout (task 8, step 11).

Each test says what to check. Write the body, then delete its skip line.
Make a verified user in the test database first (hash its password with your
`hash_password()`). Never put a real password in a test: a made-up one is fine.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 8)")
async def test_unknown_email_and_wrong_password_get_the_same_401(client):
    """Both replies have status 401 and exactly the same JSON body."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
async def test_login_sets_an_httponly_refresh_cookie(client):
    """A good login returns `access_token`, `token_type` and `user`.

    Its `set-cookie` header names `refresh_token` and has HttpOnly, SameSite=lax
    and Path=/auth.
    """
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
async def test_me_needs_a_valid_token(client):
    """GET /auth/me without a token gets 401; with the login's token it gets 200."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
async def test_an_expired_access_token_gets_401(client):
    """Build a token in the test with `exp` one minute in the past: /auth/me gets 401."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
async def test_refresh_rotates_and_logout_stops_refresh(client):
    """Log in, then POST /auth/refresh: 200 and a new cookie.

    Sending the first, used cookie again gets 401. After POST /auth/logout
    (204), refresh gets 401.
    """
    raise NotImplementedError("TODO(task 8): write this test")
