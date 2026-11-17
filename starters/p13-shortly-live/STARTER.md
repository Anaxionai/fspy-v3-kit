# Shortly live add-on (P13, Guided level)

An add-on: new files for your own `shortly/` folder, with the same paths. It never replaces
a file you already have. `TODO(task NN)` markers name the task in module 15.

## What is included
- `toxiproxy.json`: the incident drill's contract, ready. Keep it exactly as it is: the
  mentor's drill kit needs the proxies `postgres` (15432) and `redis` (16379).
- `api/app/metrics.py`: the metrics module with stubs (task 7).
- `ops/prometheus.yml`: Prometheus set-up, ready: it scrapes `api:8080` and loads `alerts.yml`.
- `ops/alerts.yml`: the rules file, with no rules yet (tasks 7 and 8).
- `ops/grafana/provisioning/datasources/prometheus.yml`: Grafana starts with Prometheus added.
- `ops/grafana/shortly-starter.json`: a dashboard to import, with the four panels and no queries.
- `ops/user-data.sh` (LF line endings) and `ops/.gitattributes`, which keeps it LF on Windows.
- `ops/postmortem.md`, `ops/deploy.md`, `ops/cost.md`, `ops/runbook.md`: outlines to fill.
- `infra/live/main.tf`, `variables.tf`, `outputs.tf`: the real server's OpenTofu outline (task 10).
  The provider with `default_tags` and the Ubuntu image lookup are ready; the resources are yours.
- `ops/Caddyfile` and `compose.live.yaml`: outlines for HTTPS on the server (task 12).

## Add it (task 7)
In Git Bash, in task 7's folder, after you copy your `shortly/` folder in:
```bash
git -C ~/fspy-v3-kit pull
cp -r ~/fspy-v3-kit/starters/p13-shortly-live/{api,infra,ops,toxiproxy.json,compose.live.yaml} shortly/
```
`api/` only adds `api/app/metrics.py`, and `infra/` only adds `infra/live/`: your P11 files in
`infra/` stay as they are. Nothing of yours is replaced.

## Lines to add to your own files (task 7)
1. In `api/`, run `uv add prometheus-client`.
2. In `api/app/main.py`, add these imports next to your other `from app...` imports:
   ```python
   from app.metrics import metrics_middleware
   from app.metrics import router as metrics_router
   ```
   Then, right after `app = FastAPI(...)` and before any route:
   ```python
   app.middleware("http")(metrics_middleware)
   app.include_router(metrics_router)  # before GET /{code}, or /metrics is read as a short code
   ```
   Add them after you write `metrics.py`: the stubs fail every request until then.
3. In `compose.yaml`, add these three services under `services:`, and `grafana-data:` under
   the top-level `volumes:` (next to `pgdata:`). Image versions are in the kit's VERSIONS.md.
   ```yaml
     toxiproxy:
       image: ghcr.io/shopify/toxiproxy:2.13.0
       command: ["-host=0.0.0.0", "-config=/config/toxiproxy.json"]
       ports: ["8474:8474"]
       volumes: ["./toxiproxy.json:/config/toxiproxy.json:ro"]
       healthcheck:
         test: ["CMD", "/toxiproxy-cli", "list"]
         interval: 5s
         timeout: 3s
         retries: 10

     prometheus:
       image: prom/prometheus:v3.16.0
       ports: ["9090:9090"]
       volumes:
         - ./ops/prometheus.yml:/etc/prometheus/prometheus.yml:ro
         - ./ops/alerts.yml:/etc/prometheus/alerts.yml:ro

     grafana:
       image: grafana/grafana:13.3.0
       ports: ["3000:3000"]
       volumes:
         - ./ops/grafana/provisioning:/etc/grafana/provisioning:ro
         - grafana-data:/var/lib/grafana
   ```
   Keep `name: shortly` and the service names: the drill finds `shortly-api-1`,
   `shortly-worker-1`, `shortly-postgres-1` and `shortly-redis-1` by these names.
4. Nothing in `compose.yaml` changes for the server: in task 12, `compose.live.yaml` adds Caddy
   and stops publishing the API's port there.

## Run it
```bash
docker compose up -d --build --wait     # from shortly/
MSYS_NO_PATHCONV=1 docker compose exec -T prometheus promtool check rules /etc/prometheus/alerts.yml
curl -s localhost:8474/proxies          # the two proxies
cd infra/live && tofu init && tofu validate && cd ../..   # task 10: the outline is valid as shipped
```
Grafana is on `localhost:3000` (first sign-in `admin` / `admin`, then choose a new password).
Import the dashboard: Dashboards, New, Import, upload `ops/grafana/shortly-starter.json`.
After you change `alerts.yml` or `prometheus.yml`, run `docker compose restart prometheus`.

Firing the alert (task 7, step 11): your rate limiter lets only 5 quick `POST /links` through,
and their body field is `target_url` (`{"url": ...}` gets 422, which is not a 5xx). With the
`postgres` proxy off, `GET /links/<code>/stats` fails with 500 every time, so send those too:
`for i in $(seq 100); do curl -s -o /dev/null localhost:8080/links/<code>/stats; done`

## Your TODOs
| Task | File | What you write |
|---|---|---|
| 7 | `api/app/metrics.py` | the three metrics, `metrics_middleware`, `GET /metrics` |
| 7 | `api/app/cache.py` (yours) | count every lookup as `hit`, `miss` or `error` |
| 7 | `.env`, `.env.example`, `compose.yaml` (yours) | the API and worker through `toxiproxy:15432` and `toxiproxy:16379`; both `depends_on` a healthy `toxiproxy` |
| 7 | `ops/alerts.yml` | `ShortlyHighErrorRate` |
| 7 | the imported dashboard | the four PromQL queries; export the result to `ops/dashboards/shortly.json` |
| 8 | `ops/postmortem.md`, `ops/alerts.yml` or the dashboard | the postmortem; one new rule or panel |
| 10 | `ops/user-data.sh` | the two Docker commands |
| 10 | `infra/live/*.tf` | the version pin, `my_ip_cidr`, the key pair, the security group and its rules, the instance, the `public_ip` output |
| 10, 12 | `ops/deploy.md` | your deploy recipe: the server in task 10, HTTPS and the stack in task 12 |
| 12 | `ops/Caddyfile`, `compose.live.yaml` | the site block; the `caddy` service, its volume and the API's port reset |
| 13 | `ops/cost.md` | prices, hours, sums, the 30-day figure, the actual spend |
| 14 | `ops/runbook.md` | all six sections and the Mermaid diagram |

Task 9 has no file: it secures your AWS account and records the evidence in `evidence.md`.
Task 11 is the HTTPS card: its answers go in `https-notes.md` in task 12's folder.
No TODO for task 15: the wrap-up writes `shortly/README.md` and `EXPLAIN.md`.

## What you still write yourself
All the metrics code, every PromQL query and alert rule, the Toxiproxy routing, the postmortem,
the OpenTofu resources, the Caddy and Compose lines for HTTPS, the runbook, the deploy recipe,
the cost sums, and the evidence in each task folder.

## Windows notes
- `ops/user-data.sh` must keep LF line endings, or cloud-init fails and Docker is never
  installed. If it shows CRLF in VS Code's status bar, click it, choose LF and save.
- `docker compose exec ... promtool` names paths inside a container, so it needs
  `MSYS_NO_PATHCONV=1` in front, as above.
- `ssh-keygen` in Git Bash writes `~/.ssh/shortly-key`, and OpenTofu finds the `.pub` file there
  through `pathexpand("~/.ssh/shortly-key.pub")`. No `chmod` is needed in Git Bash.
- On a `t3.small`, the image build can run out of memory (exit code 137). Build while nothing
  else runs. On the server, set `F="-f compose.yaml -f compose.live.yaml"`, then run
  `docker compose $F stop`, `docker compose $F build` and `docker compose $F up -d`.
