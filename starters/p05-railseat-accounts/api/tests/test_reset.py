"""Forgot password and reset (task 10, step 8).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 10)")
async def test_known_and_unknown_emails_get_the_same_reply(client):
    """POST /auth/forgot for a real user and for nobody@example.com:
    the same status and the same body."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10)")
async def test_a_reset_token_works_once_and_the_old_password_fails(client):
    """Insert a `reset` token with a known hash. POST /auth/reset with it gets 204.

    The same token again gets 400. Logging in with the old password now gets
    401, and with the new password 200.
    """
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10)")
async def test_an_expired_reset_token_gets_400(client):
    """Insert a `reset` token that expired a minute ago: POST /auth/reset gets 400."""
    raise NotImplementedError("TODO(task 10): write this test")
