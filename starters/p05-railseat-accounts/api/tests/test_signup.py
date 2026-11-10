"""Sign-up and email verification (task 7, step 11).

Each test says what to check. Write the body, then delete its skip line.
`client` is the test client from your tests/conftest.py (P3). Use your test
database session to read or insert rows directly.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 7)")
async def test_signup_stores_an_argon2_hash_and_the_passenger_role(client):
    """POST /auth/signup with a new email and a 10-character password gets 201.

    Load the user from the test database: `password_hash` starts with "$argon2id$"
    and is not the password, the role is `passenger` and `is_verified` is false,
    even when the request also sent "role": "admin".
    """
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7)")
async def test_a_taken_email_gets_409(client):
    """Sign up twice with the same email, the second time in capital letters: 409."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7)")
async def test_a_verify_token_works_once(client):
    """Insert a `verify` token whose `token_hash` is `hash_token("known-token")`.

    POST /auth/verify with "known-token" succeeds and the user is now verified.
    The same token a second time gets 400.
    """
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7)")
async def test_an_expired_verify_token_gets_400(client):
    """Insert a `verify` token that expired a minute ago: POST /auth/verify gets 400."""
    raise NotImplementedError("TODO(task 7): write this test")
