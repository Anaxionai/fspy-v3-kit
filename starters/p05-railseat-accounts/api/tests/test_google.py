"""Sign in with Google: the callback refuses a wrong state (task 15, step 12).

Write the body, then delete the skip line. The test never calls Google.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 15)")
async def test_a_wrong_state_gets_400(client):
    """Call GET /auth/google/callback?code=x&state=one with the state cookie set to
    "two": 400, and no user is created."""
    raise NotImplementedError("TODO(task 15): write this test")
