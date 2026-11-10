"""The API key check for every /v1 endpoint: `Authorization: Bearer mp_test_key`."""

import hmac
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mockpay.errors import ApiError

# auto_error=False: we raise our own error, in MockPay's JSON shape.
# Using HTTPBearer also adds an "Authorize" button to the /docs page.
_bearer = HTTPBearer(auto_error=False, description="Your MockPay API key, for example mp_test_key")


def require_api_key(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> None:
    expected = request.app.state.ctx.settings.api_key
    given = credentials.credentials if credentials else ""
    # compare_digest: the check takes the same time however much of the key is right.
    if not hmac.compare_digest(given.encode("utf-8"), expected.encode("utf-8")):
        raise ApiError(
            401,
            "invalid_api_key",
            "Missing or wrong API key. Send the header: Authorization: Bearer <MOCKPAY_API_KEY>",
        )
