"""Idempotency keys: a repeated request gets the first answer again.

The client sends `Idempotency-Key: <any unique text>` with a POST. If the
network fails and the client sends the same request again with the same
key, MockPay returns the answer it gave the first time. It does not create
a second order or a second refund.

The same key with a *different* body is a bug in the client, so MockPay
answers 409 Conflict.
"""

import hashlib
import json
from collections.abc import Callable
from typing import Any

from mockpay import clock
from mockpay.context import Context
from mockpay.errors import ApiError

MAX_KEY_LENGTH = 255


def fingerprint(request_data: dict[str, Any]) -> str:
    """SHA-256 of the request body. The order of the JSON keys does not matter."""
    canonical = json.dumps(request_data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_idempotent(
    ctx: Context,
    *,
    scope: str,
    key: str | None,
    request_data: dict[str, Any],
    action: Callable[[], dict[str, Any]],
) -> tuple[dict[str, Any], bool]:
    """Run `action` at most once per (scope, key). Returns (answer, replayed).

    Looking up the key, running the action and saving the answer happen in
    one transaction, so two requests with the same key cannot both run the
    action. If the action fails (raises), nothing is saved and the client
    may try again with the same key.
    """
    if key is None:
        return action(), False
    if not 1 <= len(key) <= MAX_KEY_LENGTH:
        raise ApiError(
            400,
            "invalid_idempotency_key",
            f"Idempotency-Key must be 1 to {MAX_KEY_LENGTH} characters.",
        )

    request_hash = fingerprint(request_data)
    with ctx.db.transaction() as conn:
        saved = conn.execute(
            "SELECT request_hash, response_body FROM idempotency_keys WHERE scope = ? AND key = ?",
            (scope, key),
        ).fetchone()
        if saved is not None:
            if saved["request_hash"] != request_hash:
                raise ApiError(
                    409,
                    "idempotency_key_reused",
                    "This Idempotency-Key was already used with a different request body. "
                    "Use a new key for a new request.",
                )
            return json.loads(saved["response_body"]), True

        answer = action()
        conn.execute(
            "INSERT INTO idempotency_keys (scope, key, request_hash, response_body, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (scope, key, request_hash, json.dumps(answer), clock.iso(clock.now())),
        )
        return answer, False
