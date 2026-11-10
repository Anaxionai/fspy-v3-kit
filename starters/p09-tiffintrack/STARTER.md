# TiffinTrack starter (P9, Guided level)

This folder is the start of your `tiffintrack/` product folder. It has the set-up done for you:
project files, folder layout, settings, the Pydantic models, function signatures, test set-up and
the web app. Every piece of logic is yours. It is marked `TODO(task N)`, where N is the task number.

## What is included

- `pyproject.toml` and `uv.lock`: Python 3.12 with FastAPI, httpx, redis, websockets, pymongo, and pytest and ruff for development.
- `api/app/`: the API. `main.py` has the endpoints, `settings.py` reads the settings, `models.py` has the request bodies,
  `db.py` opens Redis and MongoDB, and `points.py`, `riders.py`, `orders.py` and `geo.py` have stubs for your logic.
- `ws/server.py`: the WebSocket server, with the endpoints `/ws/riders` and `/ws/orders/{order_id}` as stubs.
- `simulator/sim.py`: the rider simulator, with `--riders`, `--interval`, `--seconds` and `--flaky` ready,
  and `report_progress`, which prints the counts every 10 seconds during a long run.
- `tests/`: `conftest.py` with fixtures (`client`, `db`, `live_client`, `order_body`, `free_rider`) and test
  stubs for tasks 7, 9, 15, 16, 18, 19 and 20.
- `docs/data-model.md`: the headings for your design note.
- `web/`: a Vite React TypeScript app with Leaflet 1.9.4 (`L.map`), its types and Vitest. `src/config.ts` holds the two addresses.
- `.env.example`, `.gitignore` and `.python-version`.

## Copy it in (task 7)

In Git Bash, in this task's folder (there must be no `tiffintrack/` folder yet):

```bash
git -C ~/fspy-v3-kit pull
cp -r ~/fspy-v3-kit/starters/p09-tiffintrack tiffintrack
cd tiffintrack
uv sync
uv run pytest -q
```

You should see `2 passed, 17 skipped`. Then check the web app:

```bash
cd web
npm install
npm test
```

You should see `3 passed | 6 skipped`.

## Run it

Start the cloud lab in `~/fspy-v3-kit/cloudlab`: `docker compose --profile core up -d` (Redis).
From task 15 add MongoDB: `docker compose --profile core --profile mongo up -d`.
Then use one terminal per part, each in `tiffintrack/`:

| Part | Command | Address |
|---|---|---|
| API | `uv run fastapi dev api/app/main.py` | http://localhost:8000/docs |
| WebSocket server | `uv run fastapi dev ws/server.py --port 8001` | ws://localhost:8001/ws/riders |
| Simulator | `uv run python simulator/sim.py --riders 50 --interval 2 --seconds 60` | posts to port 8000 |
| Web app | `cd web && npm run dev` | http://localhost:5173 |

Every setting has a default for your laptop. To change one, copy `.env.example` to `.env` and start a
program with `uv run --env-file .env ...`. A stub that you have not written yet fails with
`NotImplementedError: TODO(task N)`, so the log tells you which task it belongs to.

## Steps already done for you

- Task 7, step 1 (`uv init`, `uv add`) and the empty `api/app/__init__.py`.
- Task 8, steps 1, 2 and 9: `redis` and `websockets` added, `REDIS_URL` read and listed, one Redis client
  made in the API's lifespan, and the web app created.
- Task 15, step 5 and the `.env.example` part of step 11: `pymongo` added and one `AsyncMongoClient` made in the lifespan.
- Task 17, step 1: Leaflet 1.9.4 and `@types/leaflet` installed.
- Task 18, step 7: CORS allows http://localhost:5173.

## Your TODOs

| Task | Files | What you write |
|---|---|---|
| 7 | `api/app/models.py`, `api/app/main.py` | the `lat` and `lng` ranges of `Point`; `post_point` answers `{"accepted": true}` |
| 7 | `simulator/sim.py` | `random_spot`, `step_towards`, `ride` and `main` |
| 7 | `tests/test_app.py` | remove the skip line when `Point` checks its ranges |
| 8 | `api/app/points.py`, `api/app/main.py` | `publish_point`, called from `post_point` |
| 8 | `ws/server.py` | `riders_feed`: forward every `rider:*` message |
| 8 | `web/src/LiveTable.tsx` | the live table |
| 9 | `api/app/points.py`, `api/app/main.py` | `is_new_point` (simple, then atomic) and `remember_latest` |
| 9 | `tests/test_duplicates.py` | the race test with 20 copies of one point |
| 9 | `ws/server.py` | subscribe first, then send `riders:latest` |
| 9 | `web/src/live.ts`, `web/src/live.test.ts` | `connectLive`, `retryDelayMs`, `isNewer`; then remove `.skip` |
| 9 | `simulator/sim.py`, `web/src/LiveTable.tsx` | `--flaky` in `ride`; use `connectLive` and `isNewer` |
| 15 | `docs/data-model.md` | every section |
| 15 | `api/app/models.py`, `api/app/orders.py`, `api/app/main.py` | order checks, `create_order`, `find_order`, `POST /orders`, `GET /orders/{order_id}` |
| 15 | `tests/test_orders.py` | create, read back, malformed id |
| 16 | `api/app/db.py` | `create_indexes` |
| 16 | `api/app/points.py`, `api/app/main.py` | `store_point` and `update_rider`, called from `post_point` |
| 16 | `tests/test_points.py` | longitude first; a copy is stored once |
| 17 | `web/src/RiderMap.tsx`, `web/src/App.tsx` | the Leaflet map, shown above the table |
| 18 | `api/app/orders.py`, `api/app/main.py` | `NEXT`, `change_status`, `publish_status`, `POST /orders/{order_id}/status` |
| 18 | `ws/server.py` | `order_feed` |
| 18 | `web/src/OrderTracker.tsx`, `web/src/App.tsx` | the order page for `?order=<id>` |
| 18 | `tests/test_status.py` | allowed moves, a skipped status, two changes at once |
| 19 | `api/app/riders.py` | `nearest_free_riders`, `claim_rider`, `free_rider` |
| 19 | `api/app/orders.py`, `api/app/main.py` | the nearest free rider in `create_order`; `GET /riders/nearest`; free the rider on delivery |
| 19 | `tests/test_nearest.py` | the four distance tests |
| 20 | `api/app/geo.py`, `api/app/riders.py`, `api/app/orders.py` | `haversine_m`, `average_speed_kmh`, `eta_minutes`, `recent_points`, `arrival_estimate` |
| 20 | `api/app/main.py`, `web/src/OrderTracker.tsx` | `distance_m` and `eta_minutes` in `GET /orders/{order_id}`; poll every 15 s |
| 20 | `tests/test_geo.py` | the distance and arrival-time tests |

When you reach a test's task, delete its `@pytest.mark.skip(...)` line and write its body.
From task 19, placing an order needs a free rider nearby: add the `free_rider` fixture to the tests
in `test_orders.py` and `test_status.py`.

## What you still write yourself

- All the logic and tests above. The docstrings say what each function must do; the brief says how.
- `evidence.md`, `AI_LOG.md` and every other file a brief asks for, in the task folder.
- Task 21 (wrap-up) has no TODO: `tiffintrack/README.md` and `EXPLAIN.md` are your own words. This
  `STARTER.md` is not your README.
