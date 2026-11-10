# P10 Guided add-on: RailSeat at scale

New files for **your own** `railseat/` folder, the one you copy forward from P6. You get the
bookings generator and the k6 script, a `perf.md` with every section the briefs ask for, keyset
pagination, station search and the Ask RailSeat skeleton. Every piece of logic is a TODO for
you, and so is every index choice. Nothing here replaces a file you already have.

## What is included
| Path in `railseat/` | What it is |
|---|---|
| `perf/make_bookings.py` | Loading with COPY in batches of 100,000 is ready; `COLUMNS`, `prepare`, `load_context`, `build_row` and `ANALYZE`: TODOs. |
| `perf/endpoint.js` | The k6 settings are ready; the request: TODO. |
| `perf/perf.md` | Every section of tasks 7 to 13, each with a TODO. |
| `api/app/pagination.py` | `BookingPage` ready; `encode_cursor` and `decode_cursor`: TODOs. |
| `api/app/routers/admin_bookings.py` | `GET /admin/bookings`, only if you have no admin list of all bookings: admin-only and the body are TODOs. |
| `api/app/routers/stations.py` | `GET /stations/search`; `to_prefix_query` and the body: TODOs. |
| `api/app/rag/` | `chunk.py` (`split_rules`), `gemini.py` (`GeminiClient`), `index.py` (`upsert_rules`; the run is ready) and `retrieve.py` (`top_rules`): TODOs. |
| `api/app/routers/ask.py` | `POST /ask` and its models; the threshold, the prompt, the citations and the body: TODOs. |
| `api/tests/test_*.py` | Pagination, station search, chunking and `/ask`. Each test says what to check, and is skipped. |

## Copy it in (task 7)
In Git Bash, in the task folder, after you copied `railseat/` from P6:
```bash
cp -rn ~/fspy-v3-kit/starters/p10-railseat-scale/{api,perf} railseat/
```
`-n` never overwrites a file you have. Then change your own files when the task comes:
1. **`api/seed/load_seed.py` (task 7):** load with `COPY` or batches of 5,000 rows (step 2).
2. **`app/models.py`:** the `name_search` column and its GIN index on `Station` (task 11), and
   `RuleChunk` for `rule_chunks` with `Vector(768)` from `pgvector.sqlalchemy` (task 12). In the
   task 12 migration, run `CREATE EXTENSION IF NOT EXISTS vector` before the table.
3. **`app/settings.py` (task 12):** add these lines; the values go in `api/.env`, never in Git.
   No such file? Copy the P5 add-on's `api/app/settings.py` and run `uv add python-dotenv`.
```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "")
GEMINI_EMBED_MODEL = os.environ.get("GEMINI_EMBED_MODEL", "")
```
4. **`app/main.py`:** `from app.routers import admin_bookings, ask, stations`, then
   `app.include_router(admin_bookings.router)` (task 10, once it is admin-only),
   `app.include_router(stations.router)` (task 11) and `app.include_router(ask.router)` (task 12).
5. **`tests/test_permissions.py` (P5):** add `("GET", "/stations/search")` to `PUBLIC_ROUTES`
   (task 11). `/ask` and `/admin/bookings` stay private.
6. **`tests/conftest.py` (task 12):** empty `rule_chunks` with your other tables.

## Run it
- Data (task 7): in the kit's `data/railseat/`, `uv run make_seed.py --scale` (its README says
  where it writes); load it with your seed loader; then, from `railseat/api`:
  `uv run python ../perf/make_bookings.py --bookings 1000000`.
- k6 (task 8), from `railseat/`: `k6 run -e URL="http://localhost:8000/..." -e TOKEN="<token>" perf/endpoint.js`.
- Ask RailSeat (task 12), from `railseat/api`: `uv add google-genai pgvector`, then index the
  rules once with `uv run --env-file .env python -m app.rag.index`.
- Tests, from `railseat/api`: `uv run pytest -q`. The new tests show as skipped until you write
  them and delete the skip line.

## TODO map
| Task | File | What you write |
|---|---|---|
| 7 | `perf/make_bookings.py` | `COLUMNS`, `prepare`, `load_context`, `build_row`, the `ANALYZE` |
| 7 | `perf/perf.md` | `## Data` |
| 8 | `perf/endpoint.js`, `perf/perf.md` | the request with the optional token and its check; `## Baseline`, `## How measured` |
| 9 | `perf/perf.md` | `## Fix 1` (and more), `## Index sizes`. Your indexes go in your own migrations: no add-on file, because choosing them is the task. |
| 10 | `app/pagination.py`, `app/routers/admin_bookings.py` | `encode_cursor`, `decode_cursor`; admin-only, `all_bookings` |
| 10 | `tests/test_pagination.py`, `perf/perf.md` | 2 tests; `## Pagination`, `## N+1` |
| 11 | `app/routers/stations.py`, `tests/test_station_search.py` | `to_prefix_query`, `search_stations`; 3 tests |
| 11 | `perf/perf.md` | `## Search` |
| 12 | `app/rag/chunk.py`, `app/rag/gemini.py` | `split_rules`; `GeminiClient`: `__init__`, `embed_rules`, `embed_question`, `answer` |
| 12 | `app/rag/index.py`, `app/rag/retrieve.py` | `upsert_rules`; `top_rules` |
| 12 | `app/routers/ask.py` | `REFUSE_ABOVE`, `build_prompt`, `cited_rules`, `ask` |
| 12 | `tests/test_chunk.py`, `tests/test_ask.py` | 3 and 3 tests |
| 13 | `perf/perf.md`, `app/routers/ask.py` | `## Summary`, `## Ask RailSeat`, `## What it cost`, `## Not fixed`; timing the three steps of `/ask` |
| 14 | none | The wrap-up writes `railseat/README.md` and `EXPLAIN.md` only, so it has no TODO. |

## What you still write yourself
- Every TODO above, and the migrations: your indexes (task 9), `name_search` (task 11) and
  `rule_chunks` (task 12).
- The web parts, in your own pages: a Load more button with `next_cursor` (task 10), and station
  suggestions in a `<datalist>` 300 ms after the last key press (task 11).
- `evidence.md`, `AI_LOG.md`, `railseat/README.md` and `EXPLAIN.md`.
