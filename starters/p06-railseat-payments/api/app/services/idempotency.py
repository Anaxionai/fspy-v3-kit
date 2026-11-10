"""Making repeats harmless (P6 add-on, task 11).

Two tools, both enforced by a unique key in the database, not by a check in Python:
- Webhook events: one row per MockPay event id (`WebhookEvent`).
- Idempotency keys: one row per (user, `Idempotency-Key`) with the saved reply
  (`IdempotencyKey`).

Import `WebhookEvent` and `IdempotencyKey` from app.models when you write these.
Use `insert` from `sqlalchemy.dialects.postgresql`: it has `on_conflict_do_nothing`.
None of these functions commits: the route keeps them in one transaction with its work.
"""

from sqlalchemy.ext.asyncio import AsyncSession


async def record_event(session: AsyncSession, event_id: str, event_type: str) -> bool:
    """Insert the webhook event; True when it is new, False for a repeat (steps 2-3).

    Insert with ON CONFLICT DO NOTHING on `event_id` and RETURNING the id: no row
    back means another delivery of this event got there first.
    """
    raise NotImplementedError(
        "TODO(task 11): record the event once, by its unique event_id"
    )


def body_hash(raw_body: bytes) -> str:
    """The SHA-256 hex digest of a request body, stored as `request_hash` (step 4)."""
    raise NotImplementedError("TODO(task 11): hash the request body")


async def claim_key(
    session: AsyncSession, user_id: int, key: str, request_hash: str
) -> object | None:
    """Claim an `Idempotency-Key` for this user before doing the work (step 5).

    Insert (user_id, key, request_hash) with ON CONFLICT DO NOTHING.
    - Return None when the insert made a new row: this request is new, so do the work.
    - Else return the existing `IdempotencyKey` row. The route then answers 409 when
      its `request_hash` differs, replays its saved `status_code` and `response_body`
      with `Idempotent-Replayed: true` when it matches, and answers 409 when it has
      no saved reply yet (the first request is still running).
    - Read the row's fields before the route rolls back: a rollback expires them, and
      reading them afterwards fails with MissingGreenlet.
    """
    raise NotImplementedError(
        "TODO(task 11): claim the key with ON CONFLICT DO NOTHING"
    )


async def save_reply(
    session: AsyncSession, user_id: int, key: str, status_code: int, body: dict
) -> None:
    """Save the reply on the claimed key's row, in the same transaction as the work (step 6)."""
    raise NotImplementedError("TODO(task 11): save the status code and the reply body")
