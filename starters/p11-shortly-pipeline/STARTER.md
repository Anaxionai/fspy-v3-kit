# Shortly pipeline add-on (P11, Guided level)

An add-on: new files for your own `shortly/` folder, with the same paths. It never replaces
a file you already have. Every piece of the pipeline is yours to write: the files hold the
structure and `TODO(task NN)` markers, where NN is the task number in module 13.

## What is included
- `.github/workflows/ci.yml`: the workflow skeleton. Five jobs (`api`, `web`, `image`,
  `infra`, `deploy-staging`) with their triggers, names and TODOs, but no steps. Each job ends
  with a step that fails on purpose until you replace it. `image`, `infra` and
  `deploy-staging` start switched off (`if: false`).
- `scripts/smoke.sh`: the smoke test skeleton (task 14), saved with LF line endings, and
  `scripts/.gitattributes`, which keeps every `.sh` file LF when Git checks it out on Windows.
- `infra/main.tf`, `variables.tf`, `outputs.tf`: OpenTofu outlines (task 12).
- `infra/oidc-trust-policy.json`: the trust policy outline (task 13).

## Add it (task 9)
In Git Bash, in task 9's folder, after you copy your `shortly/` folder in:
```bash
git -C ~/fspy-v3-kit pull
cp -r ~/fspy-v3-kit/starters/p11-shortly-pipeline/{.github,scripts,infra} shortly/
ROOT="$(git rev-parse --show-toplevel)"
mkdir -p "$ROOT/.github/workflows"
cp shortly/.github/workflows/ci.yml "$ROOT/.github/workflows/shortly-ci.yml"
```
None of these files exists in `shortly/` before P11, so nothing of yours is replaced.
Keep the two workflow copies identical after every change (step 7 of task 9).

## Run it
```bash
act pull_request -W .github/workflows/shortly-ci.yml --rm # from the repository root
bash scripts/smoke.sh                                     # from shortly/, with the stack up
```
As shipped, `api` and `web` fail with "TODO(task 9) ..." and the other jobs are skipped.

## Lines to add to your own files
- Task 9, `api/pyproject.toml`: run `uv add --dev ruff mypy` in `api/`. If mypy says `celery`
  has no type hints, add:
  ```toml
  [tool.mypy]
  ignore_missing_imports = true
  ```
- Task 10, `api/pyproject.toml`: run `uv version 1.0.0` in `api/`.
- Task 12, `shortly/.gitignore`: add these four lines.
  ```
  .terraform/
  *.tfstate
  *.tfstate.*
  *.tfplan
  ```
- Task 14, `compose.yaml` (step 1): add the `image:` lines below. Build the image once, in
  `api`, and let `worker` reuse it. If both services have `build:` and the same `image:`,
  Docker Desktop can stop with `image "...shortly-api:dev": already exists`, because both
  builds write the same name at once.
  ```yaml
    api:
      build: .
      image: ${SHORTLY_IMAGE:-shortly-api:dev}
    worker:
      image: ${SHORTLY_IMAGE:-shortly-api:dev}
      pull_policy: never        # built by api; `docker compose pull` fetches it once, for api
  ```
  Keep the rest of each service as it is (`worker` loses only its `build:` line).

## Your TODOs
| Task | File | What you write |
|---|---|---|
| 9 | `.github/workflows/ci.yml` | `paths:`, `working-directory`, the `api` job (services, env, steps), the `web` job |
| 10 | `.github/workflows/ci.yml` | the `image` job: `needs`, permissions, version and name, login, build, push rules |
| 11 | `.github/workflows/ci.yml` | the Trivy step in `image`, before any push |
| 12 | `infra/main.tf`, `variables.tf`, `outputs.tf` | the provider, the four resources, the variables, the outputs |
| 13 | `infra/main.tf`, `.github/workflows/ci.yml` | keys out of the provider; the `infra` job |
| 13 | `infra/oidc-trust-policy.json` | your account id, and the `aud` and `sub` conditions |
| 14 | `.github/workflows/ci.yml`, `scripts/smoke.sh` | `workflow_dispatch`, `deploy-staging`, the smoke test |

No TODO for task 15: the wrap-up writes `shortly/README.md` and `EXPLAIN.md`.

## What you still write yourself
Every step of every job, the smoke test, all the OpenTofu code and the trust policy
conditions. Also `evidence.md` and `AI_LOG.md` in each task folder, and the two-copy upkeep.

## act notes (tested on Windows with act 0.2.97 and Docker Desktop, 10 Nov 2026)
- Service containers work: act waits until PostgreSQL, Redis and Floci are healthy, and the
  steps reach them on `localhost`.
- Add `--rm` to every act command. Without it, a failed job leaves its containers running,
  and its PostgreSQL and Redis keep ports 5432 and 6379, which the cloud lab needs.
- `act -j image` runs `api` and `web` first, because `image` needs them.
- The Trivy scan uses the base image in your laptop's Docker cache. An old copy can fail with
  CRITICAL findings that the current image has fixed: run `docker pull python:3.12-slim` first.
- act ignores `paths:` and `branches:` filters, so it runs every job for the event you give it.
- The deploy job runs on your own Docker, as Compose project `shortly`, so it replaces your
  local stack and keeps running afterwards. Before and after it, run `docker compose down`
  in your `shortly/` folder.
- In `smoke.sh`, `BASE_URL` changes the address for one run, such as
  `BASE_URL=http://localhost:8081 bash scripts/smoke.sh`.

## Windows notes
- `scripts/smoke.sh` must keep LF line endings. If bash says `$'\r': command not found`,
  open it in VS Code, click CRLF in the status bar, choose LF and save.
- The Trivy command names paths inside a container. In the workflow that is fine. To try it
  in Git Bash, put `MSYS_NO_PATHCONV=1` in front of `docker run`.
