"""Short codes for Shortly: random 7-character base62 text.

Base62 uses the 62 characters 0-9, a-z and A-Z, so a code is safe in a URL.
Card 4 of this module teaches it.
"""

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
CODE_LENGTH = 7


def encode_base62(n: int) -> str:
    """Return `n` (a whole number, 0 or more) written in base62 with ALPHABET.

    Examples: 0 -> "0", 61 -> "Z", 62 -> "10", 125 -> "21".
    Edge case: 0 must give "0", not an empty string.
    """
    raise NotImplementedError("TODO(task 7): write n in base62 with ALPHABET, as in card 4")


def new_code() -> str:
    """Return a new random code: CODE_LENGTH characters, each one picked from ALPHABET.

    Pick each character with `secrets.choice`, not with `random`: the `random`
    module is predictable, so someone could guess other people's links.
    """
    raise NotImplementedError("TODO(task 7): pick CODE_LENGTH characters with secrets.choice")
