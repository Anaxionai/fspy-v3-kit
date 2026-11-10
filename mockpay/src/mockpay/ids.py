"""Ids like order_Kq3vX9mT2bLw8P: a prefix that says what it is, then random letters."""

import secrets
import string

_ALPHABET = string.ascii_letters + string.digits


def new_id(prefix: str) -> str:
    """A new id such as new_id("pay") -> "pay_8fJ2kLmQ0rTz1x".

    `secrets` (not `random`) makes ids impossible to guess, so nobody can
    find another customer's order by trying ids one after another.
    """
    return f"{prefix}_" + "".join(secrets.choice(_ALPHABET) for _ in range(14))
