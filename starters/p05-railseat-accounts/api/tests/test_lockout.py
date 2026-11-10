"""Account lockout and security events (task 14, steps 8-9).

Each test says what to check. Write the body, then delete its skip line.
Never wait 15 minutes in a test: change `locked_until` in the test database.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 14)")
async def test_the_sixth_login_is_locked_even_with_the_right_password(client):
    """Five wrong passwords get 401. The right password next gets 429."""
    raise NotImplementedError("TODO(task 14): write this test")


@pytest.mark.skip(reason="TODO(task 14)")
async def test_the_lock_ends_when_locked_until_has_passed(client):
    """Lock the user, set `locked_until` a minute in the past, then the right
    password gets 200 and `failed_logins` is 0."""
    raise NotImplementedError("TODO(task 14): write this test")


@pytest.mark.skip(reason="TODO(task 14)")
async def test_the_lockout_is_logged_without_the_password(client):
    """After a lockout, `security_events` has an `account_locked` row for the user,
    and no row contains the password the test sent."""
    raise NotImplementedError("TODO(task 14): write this test")
