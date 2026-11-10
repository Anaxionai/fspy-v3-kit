"""Errors. Every API error has the same JSON shape:

    {"error": {"code": "refund_exceeds_captured", "message": "..."}}

`code` is stable, for your program to check. `message` is for people.
"""

from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


def error_response(
    status_code: int, code: str, message: str, headers: dict[str, str] | None = None
) -> JSONResponse:
    body = {"error": {"code": code, "message": message}}
    return JSONResponse(body, status_code=status_code, headers=headers)


async def handle_api_error(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, ApiError)
    headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
    return error_response(exc.status_code, exc.code, exc.message, headers)


async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
    """A bad request body or query becomes a 400 in MockPay's shape, like real gateways.

    (FastAPI's own default is a 422 with a different shape.)
    """
    assert isinstance(exc, RequestValidationError)
    problems = [f"{_field_name(error['loc'])}: {error['msg']}" for error in exc.errors()]
    return error_response(400, "invalid_request", "; ".join(problems))


def _field_name(location: tuple[Any, ...]) -> str:
    # FastAPI gives a path like ("body", "amount_paise"); the first part says where.
    return ".".join(str(part) for part in location[1:]) or str(location[0])
