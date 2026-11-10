# Shortly starter (P7, Guided level)

This folder is a `shortly/` product folder with the set-up done: project files, folder
layout, configuration, test set-up, types and function signatures. Every piece of logic
that a task asks for is a stub marked `TODO(task NN)`. The numbers are the tasks of
module 9. You write all of them.

## What is included
- `api/`: the uv project (`pyproject.toml`, `uv.lock`, Python 3.12) with every package the
  module uses, the FastAPI app with typed route stubs, Alembic set up (no migration yet),
  `tests/conftest.py`, and a skipped test stub for each test the tasks ask for.
- `worker/tasks.py`: the Celery app and a sync database engine; `count_click` is a stub.
- `web/`: the Vite React TypeScript app (as `npm create vite` makes it), with Vitest added,
  types and stubs in `src/api.ts` and `src/days.ts`, and a placeholder page.
- `Dockerfile` and `compose.yaml`: outlines with the project and service names fixed.
- `k6/redirects.js` and `k6/seed.sql`: skeletons. `.env.example`, `.dockerignore`: stubs.

## Copy it in (task 7)
In Git Bash, in task 7's folder:
```bash
git -C ~/fspy-v3-kit pull
cp -r ~/fspy-v3-kit/starters/p07-shortly shortly
ls shortly          # Dockerfile  STARTER.md  api  compose.yaml  k6  web  worker
```
Then, once:
```bash
cd shortly/api
uv sync
uv run pytest -q    # 15 skipped: the tests are stubs until you write them
```

## Steps the starter has already done
- Task 7 step 1: `uv init` and `uv add` are done. Every later `uv add` in the module
  (`pydantic-settings`, `redis`, `celery[redis]`) is already in `pyproject.toml`.
  Running one again changes nothing.
- Task 7 step 3: `app/db.py` is written. Task 10 switches it to your settings.
- Task 7 step 11: `tests/conftest.py` is written. You write the tests themselves.
- Task 19 step 1: `worker/tasks.py` has the Celery app and the engine. You write the task.
- Task 21 step 5: skip `npm create vite`. In `web/`, run `npm install`, then
  `cp .env.example .env`.

## Run it
```bash
cd shortly/api
uv run fastapi dev app/main.py --port 8080     # the API on your laptop (task 7)
uv run pytest -q                               # the tests (cloud lab running)
cd ..
docker compose up -d --build --wait            # the whole stack (from task 9)
cd web && npm run dev                          # the analytics page (task 21)
```
The tests use the cloud lab: PostgreSQL database `shortly_test` and Redis database 1.
After each new migration, migrate the test database too:
`DATABASE_URL=postgresql+psycopg://railseat:railseat@localhost:5432/shortly_test uv run alembic upgrade head`

## Your TODOs
Find them all with `grep -rn "TODO(task" .` in `shortly/`.

| Task | Files | What you write |
|---|---|---|
| 7 | `api/app/codes.py` | `encode_base62`, `new_code` |
| 7 | `api/app/models.py`, `api/alembic/versions/` | the `Link` columns, then the migration |
| 7 | `api/app/main.py` | `create_link`, `healthz`, `link_stats`, `follow` |
| 7 | `api/tests/test_codes.py`, `test_links.py` | the tests (remove each `skip`) |
| 8 | `Dockerfile`, `.dockerignore` | both stages, the user, the `CMD`; the ignore lines |
| 9 | `compose.yaml` | ports, `DATABASE_URL`, health checks, `depends_on`, the volume |
| 10 | `api/app/settings.py`, `app/db.py`, `alembic/env.py` | `Settings`, then use it everywhere |
| 10 | `.env.example`, `compose.yaml`, `api/tests/test_settings.py` | the settings; `env_file`; the test |
| 17 | `api/app/cache.py`, `app/main.py` (`update_link`, `follow`) | cache-aside; `PATCH` |
| 17 | `api/tests/test_cache.py`, settings, `.env.example` | the three cache tests |
| 18 | `api/app/ratelimit.py`, `app/main.py` (decorator) | the Lua bucket, `take_token`, `rate_limit` |
| 18 | `api/tests/test_ratelimit.py`, settings, `.env.example` | the fake-clock tests |
| 19 | `worker/tasks.py`, `api/app/clicks.py`, `app/main.py` | `count_click`, `send_click` |
| 19 | `Dockerfile`, `compose.yaml`, `api/tests/test_clicks.py` | copy `worker/`; the worker service |
| 20 | `k6/redirects.js`, `k6/seed.sql` | the load test and the seed |
| 21 | `worker/tasks.py`, `app/main.py`, settings, `.env.example` | per-day clicks, top links, CORS |
| 21 | `web/src/App.tsx`, `api.ts`, `days.ts`, `days.test.ts` | the page, the fetches, `fillDays` |

No TODO for task 22: the wrap-up writes `shortly/README.md` and `EXPLAIN.md`, which the
starter does not include. Task 6 (the practice Dockerfile) is not part of Shortly: it starts
from an empty `practice/` folder at every level.

## What you still write yourself
- Every TODO above, including every test. A test only counts once you remove its `skip`.
- The Alembic migration (`uv run alembic revision --autogenerate -m "create links"`, then read it).
- `evidence.md`, `NOTES.md` and `AI_LOG.md` in each task folder, and the wrap-up files.

## Small differences from the brief
- `get_target(code, session)` takes the request's database session as well as the code.
  Routes get sessions only through `Depends(get_session)`, as in RailSeat, so the tests can
  swap in the test database.
- The image names in `compose.yaml` are the cloud lab's PostgreSQL 16 and Redis 7 images,
  so nothing new is downloaded.

## Windows notes
- Start the API on your laptop with `fastapi dev`, not `fastapi run`. psycopg's async mode
  cannot use Windows' default event loop, and `fastapi dev` picks one that works.
  `tests/conftest.py` does the same for the tests, and keeps one event loop for the whole run.
- A Celery worker on your laptop (outside Docker) needs `--pool=solo`. Run it from `shortly/`
  with `REDIS_URL` and `DATABASE_URL` set:
  `uv run --project api celery -A worker.tasks worker --pool=solo --loglevel=INFO`
- A `docker` command that names a path inside a container needs `MSYS_NO_PATHCONV=1` in front.
  The commands in this module's briefs do not.
