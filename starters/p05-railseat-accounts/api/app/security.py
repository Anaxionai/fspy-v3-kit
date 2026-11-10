"""Passwords, one-time tokens, access tokens, the current user and role checks (P5 add-on).

Every function here is yours to write. Each TODO names the task that writes it.
Rules for the whole file:
- Never log, print or store a plain password or a raw token.
- Store only hashes: argon2 for passwords, SHA-256 for random tokens.
- Use timezone-aware UTC times (`datetime.now(UTC)`) for every expiry check.
- Read settings with `from app import settings`, for example `settings.JWT_SECRET`.
"""

from collections.abc import Awaitable, Callable
from datetime import timedelta

from fastapi import Depends, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import AuthToken, User

# ----------------------------------------------------------------- task 7 ---


def hash_password(password: str) -> str:
    """Return an argon2 hash of `password`, made with pwdlib (task 7, step 4).

    - The brief says which pwdlib object to use. Make it once, at module level.
    - The result is text that starts with `$argon2id$` and holds its own salt, so
      the same password hashed twice gives two different texts.
    """
    raise NotImplementedError("TODO(task 7): hash the password with argon2 (pwdlib)")


def verify_password(password: str, password_hash: str) -> bool:
    """Return True when `password` matches `password_hash`, else False (task 7, step 4).

    A wrong password returns False and never raises.
    """
    raise NotImplementedError("TODO(task 7): check a password against its argon2 hash")


def new_token() -> str:
    """Return a new random, URL-safe token for a link or a cookie (task 7, step 7).

    Use the `secrets` module, as the brief says. The raw token goes to the user,
    in an email or a cookie, and is never stored.
    """
    raise NotImplementedError("TODO(task 7): make a random URL-safe token")


def hash_token(token: str) -> str:
    """Return the SHA-256 hash of a raw token as hex text (task 7, step 7).

    The database keeps only this hash, so a copy of the database cannot be used
    to verify, reset or refresh anything.
    """
    raise NotImplementedError("TODO(task 7): hash the token with SHA-256")


async def issue_token(
    session: AsyncSession, user: User, purpose: str, lifetime: timedelta
) -> str:
    """Save a new one-time token for `user` and return the raw token (task 7).

    - `purpose` is "verify" (24 hours), "reset" (30 minutes, task 10) or
      "refresh" (settings.REFRESH_TOKEN_DAYS, task 8).
    - Add an `AuthToken` row with only `hash_token(raw)`, `expires_at` = now plus
      `lifetime`, and no `used_at`.
    - Do not commit here; the route commits once at the end.
    """
    raise NotImplementedError(
        "TODO(task 7): store the token's hash with its expiry, return the raw token"
    )


async def use_token(
    session: AsyncSession, token: str, purpose: str
) -> AuthToken | None:
    """Find an unused, unexpired token of this `purpose` by its hash, and use it up (task 7).

    - Return the `AuthToken` row with `used_at` set to now.
    - Return None when the token is unknown, has another purpose, was used before
      or has expired. A token works once.
    - Do not commit here; the route commits.
    """
    raise NotImplementedError(
        "TODO(task 7): find the token by its hash and mark it used"
    )


# ----------------------------------------------------------------- task 8 ---


def create_access_token(user: User) -> str:
    """Return a signed JWT for `user` that lasts settings.ACCESS_TOKEN_MINUTES (task 8, step 2).

    - Claims: `sub` (the user id as text), `role` (the role's name) and `exp`.
    - Sign it with PyJWT, HS256 and settings.JWT_SECRET.
    - Refuse to sign when JWT_SECRET is empty.
    """
    raise NotImplementedError("TODO(task 8): build and sign the access token")


def set_refresh_cookie(response: Response, token: str) -> None:
    """Send the raw refresh token in the `refresh_token` cookie (task 8, steps 5-6).

    The brief, step 6, lists every flag: httpOnly, SameSite, secure from
    settings.COOKIE_SECURE, a max age of REFRESH_TOKEN_DAYS and the path that limits
    it to the /auth routes.
    """
    raise NotImplementedError("TODO(task 8): set the refresh cookie with safe flags")


def clear_refresh_cookie(response: Response) -> None:
    """Delete the `refresh_token` cookie (task 8, step 10).

    Pass the same path you set it with, or the browser keeps the cookie.
    """
    raise NotImplementedError("TODO(task 8): delete the refresh cookie")


bearer = HTTPBearer(auto_error=False)


async def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: AsyncSession = Depends(get_session),
) -> User:
    """FastAPI dependency: the signed-in user, from `Authorization: Bearer <token>` (task 8, step 7).

    - Decode the JWT, allowing only HS256, then load the user whose id is `sub`.
    - No header, a bad signature, an expired token or an unknown user: raise
      HTTPException 401 every time, with the same detail.
    - The user's role must load with the user (`lazy="joined"` on `User.role`).
    - The route gets the same session. Loading the user starts a transaction, and
      your P3 `book_seat()` then fails at `session.begin()` with "A transaction is
      already begun". So end the read with `await session.commit()` before you
      return the user. `expire_on_commit=False` (in db.py, and in your test session
      in conftest.py) keeps the user's fields loaded after that commit.
    """
    raise NotImplementedError(
        "TODO(task 8): decode the token and load the user, else 401"
    )


# ---------------------------------------------------------------- task 11 ---


def require_role(*roles: str) -> Callable[..., Awaitable[User]]:
    """Return a FastAPI dependency that lets in only users whose role is in `roles` (task 11, step 3).

    Used as `Depends(require_role("admin"))` or `Depends(require_role("agent", "admin"))`.
    - The dependency gets the user from `current_user`, so no token still means 401.
    - A role name not in `roles` raises HTTPException 403.
    - It returns the user, so a route can use it.
    """
    raise NotImplementedError(
        "TODO(task 11): return a dependency that checks the user's role"
    )


# ---------------------------------------------------------------- task 14 ---

MAX_FAILED_LOGINS = 5
LOCK_MINUTES = 15


async def log_event(
    session: AsyncSession,
    request: Request,
    event: str,
    user: User | None = None,
    email: str | None = None,
) -> None:
    """Add one `SecurityEvent` row (task 14, step 2).

    - Store the event name, the user id and email when known, the client IP from
      `request.client` (it can be None in tests) and the time.
    - Events: login_ok, login_failed, account_locked, password_reset, role_changed.
    - Never store a password or a token. Do not commit here; the route commits.
    - Import `SecurityEvent` from app.models when you write this.
    """
    raise NotImplementedError("TODO(task 14): add a SecurityEvent row without secrets")


def is_locked(user: User) -> bool:
    """True while `user.locked_until` is in the future (task 14, step 3)."""
    raise NotImplementedError("TODO(task 14): check locked_until")


async def record_failed_login(
    session: AsyncSession, request: Request, user: User
) -> None:
    """Count one wrong password for `user` (task 14, step 4).

    - Add 1 to `failed_logins` and log `login_failed`.
    - When the count reaches MAX_FAILED_LOGINS, lock the account for LOCK_MINUTES,
      reset the count to 0 and log `account_locked`.
    - Do not commit here; the route commits.
    """
    raise NotImplementedError(
        "TODO(task 14): count the failure and lock the account at the limit"
    )
