"""Shortly's API: create short links and redirect them.

Routes, in the order they are declared. Keep this order: FastAPI tries routes
from the top, and GET /{code} matches any single word, /healthz included.

  POST  /links               create a link                 task 7 (rate limit: task 18)
  GET   /healthz             can the API reach PostgreSQL?   task 7
  GET   /links/{code}/stats  the details of one link        task 7 (per_day: task 21)
  PATCH /links/{code}        change a link's target         task 17
  GET   /stats/top           the most-clicked links         task 21
  GET   /{code}              the redirect                   task 7 (cache: 17, worker: 19)

Run it on your laptop from api/:  uv run fastapi dev app/main.py --port 8080
"""

from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

from app.db import SessionDep

app = FastAPI(title="Shortly")

# TODO(task 21): add CORSMiddleware here, allowing the origins in settings.cors_origins.


class LinkIn(BaseModel):
    """Body of POST /links. HttpUrl refuses text that is not an http or https URL (422)."""

    target_url: HttpUrl


class LinkOut(BaseModel):
    """Answer of POST /links."""

    code: str
    short_url: str


class LinkStats(BaseModel):
    """Answer of GET /links/{code}/stats."""

    code: str
    target_url: str
    clicks: int
    created_at: datetime
    # TODO(task 21): add per_day, a list of {"day", "clicks"} read from the hash clicks:<code>, sorted by day.


class LinkUpdate(BaseModel):
    """Body of PATCH /links/{code}."""

    target_url: HttpUrl


class TopLink(BaseModel):
    """One row of GET /stats/top."""

    code: str
    clicks: int


# TODO(task 18): add dependencies=[Depends(rate_limit)] to this decorator
#   (Depends from fastapi, rate_limit from app/ratelimit.py).
@app.post("/links", status_code=201)
async def create_link(body: LinkIn, session: SessionDep) -> LinkOut:
    """Create a short link. Answer 201 with its code and short_url.

    - Insert a Link whose code is new_code() (app/codes.py).
    - The unique index on code can refuse the insert with sqlalchemy.exc.IntegrityError.
      Then roll back the session and retry with a new code, up to 3 times.
    - short_url is the public base URL plus the code, such as http://localhost:8080/aZ3kP9q.
      Task 10 moves that base URL into settings.public_base_url.
    """
    raise NotImplementedError("TODO(task 7): insert a new_code(), retry on IntegrityError, answer 201")


@app.get("/healthz")
async def healthz(session: SessionDep) -> dict[str, str]:
    """Health check for Compose (task 9): run SELECT 1, then answer {"status": "ok"}.

    If PostgreSQL is down, the query raises and the answer is not 200,
    which is what a health check needs to see.
    """
    raise NotImplementedError("TODO(task 7): run SELECT 1")


@app.get("/links/{code}/stats")
async def link_stats(code: str, session: SessionDep) -> LinkStats:
    """The code, target, clicks and creation time of one link, or 404 for an unknown code."""
    raise NotImplementedError("TODO(task 7): read the link, or answer 404")


@app.patch("/links/{code}")
async def update_link(
    code: str,
    body: LinkUpdate,
    session: SessionDep,
    x_admin_token: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    """Change a link's target, and answer with the code and the new target. Admin only.

    - 403 unless settings.admin_token is set (not empty) and the X-Admin-Token header
      matches it. Compare them with secrets.compare_digest, never with ==.
    - 404 for an unknown code.
    - After the commit, delete link:<code> from Redis, so the next redirect reads the new target.
    """
    raise NotImplementedError("TODO(task 17): check the token, update, commit, then delete link:<code>")


@app.get("/stats/top")
async def top_links(limit: int = 10) -> list[TopLink]:
    """The `limit` most-clicked links, highest first, from the sorted set top:links."""
    raise NotImplementedError("TODO(task 21): read top:links, highest first")


@app.get("/{code}")
async def follow(code: str, session: SessionDep) -> RedirectResponse:
    """The redirect: 302 to the link's target, or 404 for an unknown code.

    - Task 7: read the link, add 1 to clicks, commit, and answer
      RedirectResponse(target, status_code=302).
    - Task 17: get the target with get_target(code, session) from app/cache.py instead.
    - Task 19: stop changing clicks here. Call send_click(code) from app/clicks.py
      inside try/except, so a broker that is down never breaks the redirect.
    """
    raise NotImplementedError("TODO(task 7): answer 404 or 302, and count the click")
