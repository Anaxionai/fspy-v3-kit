"""RailSeat settings (P5 add-on, ready to use).

Every value comes from an environment variable. For local work, put the real
values in `api/.env`, which Git ignores, and list only the names in
`api/.env.example`. This file loads `api/.env` itself, so
`uv run fastapi dev app/main.py` and `uv run pytest` both see it.
A variable that is already set in the environment wins over `api/.env`.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _int(name: str, default: int) -> int:
    return int(os.environ.get(name, str(default)))


def _bool(name: str, default: bool) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes"}


# Task 7: email. Locally, Mailpit takes SMTP on port 1025;
# read the mail at http://localhost:8025.
SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
SMTP_PORT = _int("SMTP_PORT", 1025)

# Task 8: tokens and the refresh cookie.
# JWT_SECRET has no default on purpose: never sign tokens with an empty secret.
JWT_SECRET = os.environ.get("JWT_SECRET", "")
ACCESS_TOKEN_MINUTES = _int("ACCESS_TOKEN_MINUTES", 15)
REFRESH_TOKEN_DAYS = _int("REFRESH_TOKEN_DAYS", 7)
# COOKIE_SECURE is false on http://localhost, and true once the site uses HTTPS.
COOKIE_SECURE = _bool("COOKIE_SECURE", False)

# Task 11: the password of the four seed users (seed/make_users.py).
SEED_PASSWORD = os.environ.get("SEED_PASSWORD", "")

# Task 15: Sign in with Google.
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.environ.get(
    "GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback"
)
