"""Webhook signatures: an HMAC-SHA256 of the raw request body.

MockPay sends the header

    X-MockPay-Signature: sha256=<64 hex characters>

The merchant computes the same HMAC over the bytes it received, with the
same shared secret, and compares. If one byte of the body changed, or the
sender did not know the secret, the two values differ.
"""

import hashlib
import hmac

PREFIX = "sha256="


def sign(body: bytes, secret: str) -> str:
    """Return the X-MockPay-Signature header value for this exact body."""
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return PREFIX + digest


def verify(body: bytes, header: str | None, secret: str) -> bool:
    """True when `header` is the right signature for `body`.

    hmac.compare_digest takes the same time wherever the first difference
    is, so an attacker cannot learn the right signature by timing answers.
    """
    if not header or not header.startswith(PREFIX):
        return False
    return hmac.compare_digest(sign(body, secret), header)
