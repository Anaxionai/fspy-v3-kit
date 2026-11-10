"""Order and payment statuses as state machines (P6 add-on, task 8).

Every status change goes through `move()`. A move that is not in the dicts
raises InvalidMove, so a late or repeated webhook can never, for example,
turn a cancelled order back into a paid one.
"""

# The statuses each column may hold. Use them in your CHECK constraints (step 8).
ORDER_STATUSES = ("created", "paid", "cancelled")
PAYMENT_STATUSES = ("captured", "failed", "partially_refunded", "refunded")


class InvalidMove(Exception):
    """A status change that the state machine does not allow."""


# TODO(task 8): fill both dicts from the brief's step 10. Each key is a status;
# its value is the set of statuses it may move to. A status with no way out
# still gets a key, with an empty set.
ORDER_MOVES: dict[str, set[str]] = {}
PAYMENT_MOVES: dict[str, set[str]] = {}


def move(obj: object, to: str) -> None:
    """Move an `Order` or a `Payment` to the status `to` (task 8, step 9).

    - Choose ORDER_MOVES or PAYMENT_MOVES by the object's table
      (`obj.__tablename__` is "orders" or "payments").
    - If `to` is not allowed from `obj.status`, raise InvalidMove with both
      statuses in the message. Otherwise set `obj.status = to`.
    - It never commits: the caller's transaction does.
    """
    raise NotImplementedError("TODO(task 8): allow only the moves in the dicts")
