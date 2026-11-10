# P5 Guided add-on: RailSeat accounts

New files for **your own** `railseat/` folder, the one you copy forward from P4. You get the
auth router, the security helpers, the React pages and one test file per task. Every piece of
logic is a TODO for you. Nothing here replaces a file you already have.

## What is included
| Path in `railseat/` | What it is |
|---|---|
| `api/app/settings.py` | Ready. Reads every P5 setting from `api/.env`. |
| `api/app/auth_schemas.py` | Ready. Request and response models; no reply holds a password. |
| `api/app/security.py` | Hashing, one-time tokens, JWTs, `current_user`, `require_role()`, lockout: TODOs. |
| `api/app/email.py`, `api/app/oidc.py` | `send_email()` and the Google helpers: TODOs. |
| `api/app/routers/auth.py`, `admin.py` | Every route's path and models; the bodies are TODOs. |
| `api/seed/make_users.py` | The four seed users; saving one user is a TODO. |
| `api/tests/test_*.py` | One file per task. Each test says what to check, and is skipped. |
| `web/src/auth/AuthContext.tsx`, `RequireRole.tsx` | The session context and the role guard: TODOs. |
| `web/src/routes/*.tsx` | Signup, Verify, Login, ResetPassword, Admin: forms ready, API calls TODO. Forbidden: ready. |
| `web/tests/e2e/roles.spec.ts` | The Playwright test, skipped. |
| `docs/permissions.md`, `docs/owasp-checklist.md` | Table skeletons for tasks 11 and 16. |

## Copy it in (task 7)
In Git Bash, in the task folder, after you copied `railseat/` from P4:
```bash
cp -rn ~/fspy-v3-kit/starters/p05-railseat-accounts/{api,web,docs} railseat/
cd railseat/api
uv add "pwdlib[argon2]" email-validator python-dotenv
```
`-n` never overwrites a file you have. `python-dotenv` lets `app/settings.py` read `api/.env`.
Then change your own files, in this order:
1. **`app/models.py` (task 7, steps 1-2):** write `Role`, `User` and `AuthToken` first; the add-on
   imports them. `SecurityEvent` comes in task 14.
2. **`web/src/api/client.ts`:** paste this block at the end now. The new pages import its names.
```ts
// ---- P5 accounts (from the p05 add-on's STARTER.md) ----
export type Role = "passenger" | "agent" | "admin";
export type AuthUser = { id: number; email: string; role: Role };
export class AuthError extends Error {}
export class ForbiddenError extends Error {}

let accessToken: string | null = null; // memory only, never localStorage
export function setAccessToken(token: string | null) {
  accessToken = token;
}
export function getAccessToken() {
  return accessToken;
}

export function refreshSession(): Promise<AuthUser> {
  throw new Error("TODO(task 9): POST /auth/refresh once for all callers, setAccessToken(), return the user");
}
// TODO(task 9): in api(), send `Authorization: Bearer <token>` and credentials: "include". On a 401
// from any path except /auth/login and /auth/refresh, await refreshSession() and retry once; if that
// fails, setAccessToken(null) and throw AuthError.
// TODO(task 13): in api(), throw ForbiddenError on a 403. Never refresh or log out on a 403.
```
3. **`app/main.py`:** `from app.routers import auth` and `app.include_router(auth.router)` (task 7);
   the same for `admin` (task 11). In task 9, besides `allow_credentials=True`, add
   `"Authorization"` to the CORS `allow_headers`, or the browser blocks every request with a token.
4. **`web/src/App.tsx`:** one `<Route>` per page when its task needs it: `/signup` and `/verify`
   (task 7), `/login` (task 9), `/reset` (task 10), and `/admin` as
   `<RequireRole roles={["admin"]}><Admin /></RequireRole>` (task 13). Pages are default exports;
   `RequireRole`, `AuthProvider` and `useAuth` are named exports.
5. **`web/src/main.tsx` (task 9):** wrap `<App />` in `<AuthProvider>`, inside `<QueryClientProvider>`.
6. **`api/.env.example`:** names only, never values: `SMTP_HOST`, `SMTP_PORT` (task 7);
   `JWT_SECRET`, `ACCESS_TOKEN_MINUTES`, `REFRESH_TOKEN_DAYS`, `COOKIE_SECURE` (task 8);
   `SEED_PASSWORD` (task 11); `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` (task 15).
7. **`tests/conftest.py`:** add `users` and `auth_tokens` (task 7) and `security_events` (task 14)
   to the tables your data fixture empties. Never empty `roles`: your migration inserted them.
8. **After task 11** every booking route needs a token, so your P3 booking tests get 401. Make a
   verified user in those tests and send its token.

The briefs add the other packages: `uv add pyjwt` (task 8) and `uv add httpx "pyjwt[crypto]"` (task 15).

## Run it
- From `railseat/api`: `uv run fastapi dev app/main.py` (http://localhost:8000/docs) and
  `uv run pytest -q`. The new tests show as skipped until you write them and delete the skip line.
- Seed users (task 11): `uv run python -m seed.make_users`.
- From `railseat/web`: `npm run dev`, `npm run build` and `npm test`.

## TODO map
| Task | File | What you write |
|---|---|---|
| 7 | `app/security.py` | `hash_password`, `verify_password`, `new_token`, `hash_token`, `issue_token`, `use_token` |
| 7 | `app/email.py`, `app/routers/auth.py` | `send_email`; `signup`, `verify` |
| 7 | `routes/Signup.tsx`, `routes/Verify.tsx`, `tests/test_signup.py` | `signUp()`, `verifyToken()`; 4 tests |
| 8 | `app/security.py` | `create_access_token`, `set_refresh_cookie`, `clear_refresh_cookie`, `current_user` |
| 8 | `app/routers/auth.py`, `tests/test_login.py` | `login`, `me`, `refresh`, `logout`; 5 tests |
| 9 | `src/api/client.ts` (block above) | `refreshSession()`, the bearer header, credentials, one retry |
| 9 | `auth/AuthContext.tsx`, `routes/Login.tsx` | restore on start, `login`, `logout`; the submit |
| 10 | `app/routers/auth.py`, `tests/test_reset.py` | `forgot`, `reset`; 3 tests |
| 10 | `routes/ResetPassword.tsx`, `routes/Login.tsx` | the two-state switch, both API calls; the "Forgot password?" link |
| 11 | `app/security.py`, `app/routers/admin.py` | `require_role`; the router's dependencies, `list_users`, `change_role` |
| 11 | `seed/make_users.py`, `docs/permissions.md` | `save_user`; the matrix |
| 11 | `tests/test_permissions.py` | `PUBLIC_ROUTES` and 3 tests |
| 12 | your `app/services/booking.py`, `tests/test_ownership.py` | `get_booking_for()` (below); 3 tests |
| 13 | `auth/RequireRole.tsx`, `routes/Admin.tsx` | the guard; `useAdminUsers()` |
| 13 | `src/api/client.ts` (block above), `tests/e2e/roles.spec.ts` | `ForbiddenError` on 403; 1 test |
| 14 | `app/security.py`, `tests/test_lockout.py` | `log_event`, `is_locked`, `record_failed_login`; 3 tests |
| 14 | `app/routers/auth.py`, `app/routers/admin.py` | the lockout in `login`; log `password_reset` and `role_changed` |
| 15 | `app/oidc.py` | `google_config`, `authorization_url`, `exchange_code`, `verify_id_token`, `find_or_create_google_user` |
| 15 | `app/routers/auth.py`, `routes/Login.tsx`, `tests/test_google.py` | `google_login`, `google_callback`; the Google link; 1 test |
| 16 | `docs/owasp-checklist.md` | all ten rows, and your two fixes in your own files |
| 17 | none | The wrap-up writes `railseat/README.md` and `EXPLAIN.md` only, so it has no TODO. |

For task 12, add this to your own `app/services/booking.py` and write the body:
```python
async def get_booking_for(session: AsyncSession, user: User, pnr: str) -> Booking:
    """The booking with this PNR for this user, or raise your NotFound (404).
    A passenger who does not own it gets the same NotFound; agents and admins pass.
    If your cancel_booking() then calls session.begin(), end this read first."""
    raise NotImplementedError("TODO(task 12): load the booking and check its owner")
```

## What you still write yourself
- Every TODO above, the models, the Alembic migrations (with `op.bulk_insert` for the three
  roles) and `GET /bookings` with `user_id` set in `POST /bookings` (task 12).
- `useMyBookings()` in `queries.ts` (task 12), navigation by role (task 13), the `QueryClient`
  retry rule (task 9) and logging in first in `booking.spec.ts` (task 13).
- `evidence.md`, `AI_LOG.md`, `railseat/README.md` and `EXPLAIN.md`.
