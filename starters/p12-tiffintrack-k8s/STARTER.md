# TiffinTrack on Kubernetes add-on (P12, Guided level)

These files go into your own `tiffintrack/` folder from P9. They are templates with TODOs: each
Kubernetes object has its structure and names, and you fill in the values and blocks that a task
asks for. Nothing in your folder is replaced. Every TODO names its task: `TODO(task N)`.

## What is included

- `k8s/`: `api.yaml`, `ws.yaml`, `sim.yaml`, `redis.yaml` and `mongo.yaml` (task 8); `web.yaml`, `ingress.yaml`
  and `README.md` (task 9); `config.yaml` and `secret.yaml.example` (task 10); `ws-hpa.yaml` (task 22).
- Ready to build, as in P7: `api/Dockerfile`, `ws/Dockerfile`, `simulator/Dockerfile`, `web/Dockerfile`
  (`node:24-alpine`, then nginx serves the page at `/`), `.dockerignore` and `web/.dockerignore`.
- Stubs: `api/app/health.py` (task 21), `api/app/telemetry.py` and `api/app/metrics.py` (task 25).
- `scripts/ws_load.py` (task 22) and `scripts/order_loop.py` (task 23), with their options ready.
- `helm/tiffintrack/Chart.yaml` (ready) and `helm/tiffintrack/values.yaml` (TODO) for task 24.
- `observability/setup.md` (task 26).

## Copy it in (task 8)

In Git Bash, in this task's folder, after you copy your `tiffintrack/` folder forward:

```bash
git -C ~/fspy-v3-kit pull
cp -rnv ~/fspy-v3-kit/starters/p12-tiffintrack-k8s/. tiffintrack/
```

`-n` never replaces a file you already have, and `-v` lists every file it copies. A file missing
from the list means you already had one with that name: compare the two and merge them by hand.

## How the templates work

- The task 8 files (`api`, `ws`, `sim`, `redis`, `mongo`) are real objects with empty values.
  Fill in every `TODO(task 8)` before your first `kubectl apply -f k8s/`.
- `web.yaml`, `ingress.yaml`, `config.yaml` and `ws-hpa.yaml` hold only comments until their task,
  so `kubectl apply -f k8s/` skips them. In that task, select from `# apiVersion` to the end and press Ctrl+/.
- A later TODO sits where its change goes, for example `TODO(task 21)` for the probes in `api.yaml`.
- `kubectl apply -f k8s/` skips `secret.yaml.example`, because its name does not end in `.yaml`.
- In task 24, Helm reads comments too: never write a double curly brace in a comment.

## Build and run (task 8)

From `tiffintrack/`, with the cluster `fspy` running and the task 8 TODOs filled in:

```bash
docker build -f api/Dockerfile -t tiffintrack-api:0.1.0 .
docker build -f ws/Dockerfile -t tiffintrack-ws:0.1.0 .
docker build -f simulator/Dockerfile -t tiffintrack-sim:0.1.0 .
k3d image import tiffintrack-api:0.1.0 tiffintrack-ws:0.1.0 tiffintrack-sim:0.1.0 -c fspy
kubectl apply -f k8s/
kubectl get pods -w
```

The API image runs `fastapi run api/app/main.py --port 8000`, the WebSocket image runs `ws/server.py`
with `uvicorn` on port 8001 (it starts faster), and the simulator image runs `simulator/sim.py` with
the Deployment's `args`. The images compile Python's bytecode when they are built, so pods start
quickly even with the small CPU limits of task 22. If your files are in other places, change the
`COPY` and `CMD` lines.

On the first `kubectl apply`, an API pod may restart once: it makes its MongoDB indexes at start-up
and gives up if MongoDB is still starting. `kubectl logs deployment/sim` shows the P9 starter's
`progress:` lines every 10 seconds. If your `sim.py` prints only at the end, add a progress line.

## Lines to change in your own files

- Task 8, step 1: remove the defaults of `MONGO_URL`, `REDIS_URL` and `API_URL`. With the P9 starter they
  are in `api/app/settings.py`, `ws/server.py` and `simulator/sim.py`, and `tests/conftest.py` still sets
  them for the tests. To run a program on your laptop after this, copy `.env.example` to `.env` and
  start it with `uv run --env-file .env ...`.
- Task 9, step 1: with the P9 starter, both addresses of the web app are in `web/src/config.ts`.
- Task 21: add the health endpoints. In `api/app/main.py`, put the import with the others and the
  second line after `app = FastAPI(...)`:
  ```python
  from app.health import router as health_router

  app.include_router(health_router)
  ```
- Task 25: after step 1's `uv add`, wire up tracing and metrics in `api/app/main.py` the same way:
  ```python
  from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
  from app.metrics import metrics_endpoint, record_request
  from app.telemetry import setup_tracing

  setup_tracing()
  app.middleware("http")(record_request)
  app.add_api_route("/metrics", metrics_endpoint, methods=["GET"], include_in_schema=False)
  FastAPIInstrumentor.instrument_app(app, excluded_urls="healthz,readyz,metrics")
  ```

## Your TODOs

| Task | Files | What you write |
|---|---|---|
| 8 | `k8s/api.yaml`, `ws.yaml`, `sim.yaml`, `redis.yaml`, `mongo.yaml` | labels and selectors, images and tags, ports, env with Service names, `sim`'s args |
| 9 | `k8s/web.yaml`, `k8s/ingress.yaml`, `k8s/README.md` | the web Deployment and Service, the four Ingress paths, the routes flowchart |
| 10 | `k8s/config.yaml`, `k8s/secret.yaml.example` | the four settings; fake Secret values |
| 10 | `k8s/api.yaml`, `ws.yaml`, `sim.yaml`, `mongo.yaml` | `envFrom`, `secretKeyRef`, MongoDB's root user |
| 20 | `k8s/redis.yaml`, `k8s/mongo.yaml` | StatefulSets, volume claims, headless Services |
| 21 | `api/app/health.py`, `k8s/api.yaml`, `k8s/ws.yaml` | `/healthz` and `/readyz`; three API probes; two TCP probes |
| 22 | every container in `k8s/`, `k8s/ws-hpa.yaml`, `k8s/ws.yaml` | requests and limits; the autoscaler; no `replicas` for `ws` |
| 22 | `scripts/ws_load.py` | `viewer` and `main` |
| 23 | `k8s/api.yaml`, `scripts/order_loop.py` | strategy, `preStop`, change-cause; `one_order` and `main` |
| 24 | `helm/tiffintrack/values.yaml` | every value the templates read |
| 25 | `api/app/telemetry.py`, `api/app/metrics.py`, the chart's API template | tracing, the two metrics, the middleware, `/metrics`, scrape annotations |
| 26 | `observability/setup.md` | the install commands; your exported dashboard JSON beside it |

## What you still write yourself

- Every value marked TODO. The comments say what each one is for; the brief gives the numbers.
- Task 23: the `X-App-Version` middleware in `api/app/main.py`. Task 24: the `templates/` folder,
  copied from `k8s/`. Task 25: your own span in `POST /orders`. Task 26: the dashboard.
- Tasks 11 and 27 have no TODO: they ask you to read the cluster's output and explain it in your own words.
- `evidence.md`, `AI_LOG.md`, `EXPLAIN.md` and the README update, as each brief asks.
