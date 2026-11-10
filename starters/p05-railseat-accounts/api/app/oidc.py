"""Sign in with Google through OpenID Connect (P5 add-on, task 15).

The flow:
1. GET /auth/google/login sends the browser to Google with random `state` and `nonce`.
2. Google sends the browser back to GET /auth/google/callback with a `code` and the `state`.
3. The API swaps the code for tokens on the server, with the client secret.
4. The API checks the ID token itself before it trusts any claim in it.

Read GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET and GOOGLE_REDIRECT_URI from `app.settings`.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_ISSUERS = ["https://accounts.google.com", "accounts.google.com"]


async def google_config() -> dict:
    """Return Google's discovery document from GOOGLE_DISCOVERY_URL (task 15, step 6).

    It is a dict with `authorization_endpoint`, `token_endpoint` and `jwks_uri`.
    Fetch it with httpx and keep it in a module variable, so it is fetched once per run.
    """
    raise NotImplementedError("TODO(task 15): fetch Google's discovery document once")


async def authorization_url(state: str, nonce: str) -> str:
    """Return the Google URL that /auth/google/login redirects to (task 15, step 7).

    It is the `authorization_endpoint` with the query parameters the brief lists:
    `client_id`, `redirect_uri`, `response_type`, `scope`, `state` and `nonce`.
    Build the query with `urllib.parse.urlencode`.
    """
    raise NotImplementedError("TODO(task 15): build the authorisation URL")


async def exchange_code(code: str) -> dict:
    """Swap the authorisation `code` for Google's tokens, on the server (task 15, step 8).

    POST a form to the `token_endpoint` with httpx: `code`, `client_id`,
    `client_secret`, `redirect_uri` and `grant_type=authorization_code`.
    Return the JSON reply, which holds `id_token`. A reply that is not 200 raises
    HTTPException 400. Never log the reply: it holds tokens.
    """
    raise NotImplementedError("TODO(task 15): exchange the code for tokens")


def verify_id_token(id_token: str, nonce: str, jwks_uri: str) -> dict:
    """Check Google's ID token and return its claims (task 15, steps 9-10).

    - Check the signature with the key from Google's `jwks_uri`, the algorithm,
      the audience (your client ID), the issuer (GOOGLE_ISSUERS) and the expiry,
      as the brief's step 9 says.
    - Then check that the `nonce` claim equals `nonce` (from its cookie) and that
      `email_verified` is true.
    - Any failure raises HTTPException 400. Never trust a claim before these checks.
    """
    raise NotImplementedError(
        "TODO(task 15): verify the ID token's signature and claims"
    )


async def find_or_create_google_user(session: AsyncSession, claims: dict) -> User:
    """Return the RailSeat user for checked Google claims (task 15, step 10).

    1. A user whose `google_sub` equals `claims["sub"]`.
    2. Else a user with the same email (lower-case): save `google_sub` on it, so
       the two accounts are linked.
    3. Else a new verified `passenger` with no password and this `google_sub`.
    Do not commit here; the route commits.
    """
    raise NotImplementedError("TODO(task 15): find, link or create the user")
