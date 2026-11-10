"""Order and payment state machines (task 8, step 11).

Each test says what to check. Write the body, then delete its skip line.

These tests need no database: a small object with a `status` and a
`__tablename__` is enough.
"""

import pytest


@pytest.mark.skip(reason="TODO(task 8)")
def test_every_allowed_move_works():
    """Parametrise over every (from, to) pair in ORDER_MOVES and PAYMENT_MOVES:
    move() sets the new status."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
def test_forbidden_moves_raise():
    """Parametrise forbidden moves, such as an order from "cancelled" to "paid" or a
    payment from "refunded" to "captured": each raises InvalidMove and keeps the status."""
    raise NotImplementedError("TODO(task 8): write this test")
