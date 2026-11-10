"""Accounts: sign-up, verification, login, refresh, logout, reset and Google (P5 add-on).

Include it in app/main.py with `app.include_router(auth.router)` (task 7).
Every route has its path, its request model and its response model. You write
each body in the task its TODO names. Commit the session once, at the end of a
route that changes data.
"""

from fastapi import APIRouter, Cookie, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth_schemas import (
    ForgotIn,
    LoginIn,
    LoginOut,
    ResetIn,
    SignupIn,
    TokenIn,
    UserOut,
)
from app.db import get_session
from app.models import User
from app.security import current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# The texts the briefs fix. React shows some of them. WRONG_LOGIN is the same
# for an unknown email and for a wrong password.
WRONG_LOGIN = "Wrong email or password"
VERIFY_FIRST = "Verify your email first"
TOO_MANY_FAILURES = "Too many failed logins. Try again in 15 minutes."
FORGOT_REPLY = "If an account exists, we have emailed a reset link."
BAD_LINK = "This link is invalid or has expired."


@router.post("/signup", status_code=201, response_model=UserOut)
async def signup(data: SignupIn, session: AsyncSession = Depends(get_session)):
    """Create an account and email a verification link (task 7, steps 5-8).

    - Lower-case the email. A taken email gets 409.
    - Store only the password's argon2 hash. The role is always `passenger`.
      `is_verified` starts false.
    - Issue a `verify` token for 24 hours and email the link
      http://localhost:5173/verify?token=<token> with `send_email()`.
    - Return 201 with the new user.
    """
    raise NotImplementedError("TODO(task 7): write the sign-up")


@router.post("/verify")
async def verify(data: TokenIn, session: AsyncSession = Depends(get_session)):
    """Verify an email with its one-time token (task 7, step 9).

    Use up an unused, unexpired `verify` token, then set the user's `is_verified`.
    An unknown, used or expired token gets 400 with BAD_LINK.
    """
    raise NotImplementedError("TODO(task 7): verify the email with the one-time token")


@router.post("/login", response_model=LoginOut)
async def login(
    data: LoginIn,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Sign in with an email and a password (task 8, steps 3-6).

    - An unknown email and a wrong password both get 401 with WRONG_LOGIN.
    - A user who is not verified gets 403 with VERIFY_FIRST.
    - On success: issue a `refresh` token, set the cookie with `set_refresh_cookie()`,
      and return `access_token`, `token_type` and `user`.
    """
    # TODO(task 14): check is_locked() before the password (429 with TOO_MANY_FAILURES),
    # call record_failed_login() on a wrong password, reset failed_logins and log
    # login_ok on success, and give an unknown email the same password work (step 6).
    raise NotImplementedError("TODO(task 8): write the login")


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(current_user)):
    """The signed-in user's `id`, `email` and `role` (task 8, step 8)."""
    raise NotImplementedError("TODO(task 8): return the current user")


@router.post("/refresh", response_model=LoginOut)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_session),
):
    """Swap the refresh cookie for a new access token (task 8, step 9).

    - A missing, unknown, used or expired refresh token gets 401.
    - Use the old token up, issue a new one and set the new cookie: each refresh
      token works once (rotation).
    - Return a new access token and the user, as login does.
    """
    raise NotImplementedError("TODO(task 8): rotate the refresh token")


@router.post("/logout", status_code=204)
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_session),
):
    """End this session (task 8, step 10).

    Mark the cookie's refresh token used, delete the cookie with
    `clear_refresh_cookie()` and return 204, also when there is no cookie.
    """
    raise NotImplementedError(
        "TODO(task 8): revoke the refresh token and delete the cookie"
    )


@router.post("/forgot", status_code=202)
async def forgot(data: ForgotIn, session: AsyncSession = Depends(get_session)):
    """Email a reset link without saying whether the account exists (task 10, steps 1-3).

    - Always return 202 with `{"detail": FORGOT_REPLY}`.
    - Only for a real account: mark its unused `reset` tokens used, issue a new one
      for 30 minutes and email http://localhost:5173/reset?token=<token>.
    """
    raise NotImplementedError("TODO(task 10): write the forgot-password route")


@router.post("/reset", status_code=204)
async def reset(
    data: ResetIn, request: Request, session: AsyncSession = Depends(get_session)
):
    """Set a new password with a `reset` token (task 10, steps 4-5).

    - An unknown, used or expired token gets 400 with BAD_LINK.
    - Save the new password's argon2 hash and mark every `refresh` token of the
      user used, so all old sessions end. Return 204.
    """
    # TODO(task 14): log password_reset with log_event().
    raise NotImplementedError("TODO(task 10): write the password reset")


@router.get("/google/login")
async def google_login():
    """Start Sign in with Google (task 15, step 7).

    Make random `state` and `nonce` values and put each in an httpOnly cookie with
    SameSite=Lax (Google's redirect back is cross-site, so Strict cookies would not
    come back). Redirect to `authorization_url(state, nonce)` from app/oidc.py.
    """
    raise NotImplementedError("TODO(task 15): redirect to Google with state and nonce")


@router.get("/google/callback")
async def google_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    """Finish Sign in with Google (task 15, steps 8-11).

    - A missing `state`, or one that differs from its cookie: 400.
    - `exchange_code()`, then `verify_id_token()` with the nonce from its cookie.
    - `find_or_create_google_user()`, then start a normal RailSeat session: issue a
      refresh token, set the cookie and redirect to http://localhost:5173/.
    """
    raise NotImplementedError(
        "TODO(task 15): check state, exchange the code and start a session"
    )
