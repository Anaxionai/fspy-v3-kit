# Cloud lab

The cloud lab runs the course's databases and cloud services on your laptop, in Docker Desktop. Nothing here costs money, and nothing leaves your laptop.

It is one Compose file, `docker-compose.yml`, with six profiles (named groups of services). You start only the profile your task needs. Four of the services are emulators (programs that imitate a cloud service on your laptop): Floci, Azurite, fake-gcs-server and the Pub/Sub emulator.

## Before you start

- Docker Desktop is running, with the WSL 2 backend. `setup/windows.md` in this kit shows how to install it.
- You use Git Bash in the VS Code terminal for every command.
- Go to this folder first. Every command in this file runs from here:

```bash
cd ~/fspy-v3-kit/cloudlab
docker compose version
```

The second command prints `Docker Compose version v2...`. If it prints an error, start Docker Desktop and wait until it says "Engine running".

## The six profiles

| Profile | What it starts | Used in |
|---|---|---|
| `core` | PostgreSQL 16 with pgvector, Redis 7, Mailpit | the map weeks, then most projects |
| `aws` | Floci, a local AWS (S3, SQS, Lambda, IAM, Budgets) | the map weeks, P8, P11, P13 |
| `azure` | Azurite, the Azure Storage emulator | P8 |
| `gcp` | fake-gcs-server (Cloud Storage) and the Pub/Sub emulator | P8 |
| `mongo` | MongoDB 7 | P9, P12 |
| `drill` | Toxiproxy, which puts faults between your app and the `core` databases | P13 |

Kubernetes is not a profile. It runs in k3d: see `k3d/README.md`.

## Start a profile

| Profile | Start command |
|---|---|
| `core` | `docker compose --profile core up -d` |
| `aws` | `docker compose --profile aws up -d` |
| `azure` | `docker compose --profile azure up -d` |
| `gcp` | `docker compose --profile gcp up -d` |
| `mongo` | `docker compose --profile mongo up -d` |
| `drill` | `docker compose --profile core --profile drill up -d` (Toxiproxy needs `core`) |

The first start of each profile downloads its images once. On a slow connection this can take 10 minutes.

Check that it runs:

```bash
docker compose --profile core ps
```

Every line should say `Up`. Most services also say `(healthy)` after a few seconds. The containers are named `cloudlab-<service>-1`, for example `cloudlab-postgres-1` and `cloudlab-redis-1`.

To start two profiles together, name both: `docker compose --profile core --profile mongo up -d`.

## Stop the lab

| To stop | Command |
|---|---|
| One profile, keeping its data | `docker compose --profile core down` |
| One emulator inside a profile | `docker compose --profile azure stop azurite` |
| The same emulator again | `docker compose --profile azure start azurite` |
| Everything in the lab | `docker compose --profile "*" down` |

Always name a profile. `docker compose down` on its own stops nothing here, because every service belongs to a profile.

The message `Network cloudlab_default  Resource is still in use` is normal. It means another profile is still running.

The service names for `stop` and `start` are `postgres`, `redis`, `mailpit`, `floci`, `azurite`, `gcs`, `pubsub`, `mongo` and `toxiproxy`.

## Reset a profile (delete its data)

```bash
docker compose --profile core down -v
```

The `-v` flag deletes the profile's volumes (storage that Docker keeps between runs). Other profiles keep their data.

| Service | Keeps data after `down`? |
|---|---|
| PostgreSQL, Redis, MongoDB | Yes, in a volume |
| Floci | Yes: buckets, queues, functions and budgets, in a volume |
| Azurite, fake-gcs-server | Yes, in a volume |
| Pub/Sub emulator | No. Create your topics and subscriptions again after each start |
| Toxiproxy | No. It reads `toxiproxy.json` again at each start |

## Ports and passwords

These passwords work only on your laptop. Never use them on a real server.

| Service | Profile | Address from your laptop | User and password |
|---|---|---|---|
| PostgreSQL 16 + pgvector | `core` | `postgresql://railseat:railseat@localhost:5432/railseat` | user `railseat`, password `railseat`, database `railseat` |
| Redis 7 | `core` | `redis://localhost:6379/0` | none |
| Mailpit SMTP | `core` | `localhost:1025` | any user name and password, or none; no TLS |
| Mailpit web page | `core` | http://localhost:8025 | none |
| Floci (AWS) | `aws` | http://localhost:4566 | keys `test` / `test`, region `ap-south-1`; see `aws/README.md` |
| Azurite Blob, Queue, Table | `azure` | http://127.0.0.1:10000, 10001, 10002 | the connection string in `azure/README.md` |
| fake-gcs-server | `gcp` | http://localhost:4443 | none; see `gcp/README.md` |
| Pub/Sub emulator | `gcp` | `localhost:8085` | none |
| MongoDB 7 | `mongo` | `mongodb://localhost:27017` | none (no password) |
| Toxiproxy API | `drill` | http://localhost:8474 | none |
| PostgreSQL through Toxiproxy | `drill` | `localhost:15432` | as PostgreSQL |
| Redis through Toxiproxy | `drill` | `localhost:16379` | none |

pgvector is installed but not switched on. Switch it on once in each database: `CREATE EXTENSION IF NOT EXISTS vector;`.

## RAM advice for 8 GB laptops

Run at most two profiles at once, and stop each profile when its task is done. Your editor, browser and own app need memory too.

Memory use measured on the course versions, with the services idle:

| What runs | About |
|---|---|
| `core` | 50 MB (PostgreSQL 35 MB, Redis 5 MB, Mailpit 10 MB) |
| `aws` | 160 MB, plus up to 128 MB for each Lambda function while it runs |
| `azure` | 130 MB |
| `gcp` | 250 MB (Pub/Sub emulator 195 MB, fake-gcs-server 60 MB) |
| `mongo` | 75 MB; its cache can grow to 256 MB under load |
| `drill` | 10 MB |
| A k3d cluster (see `k3d/README.md`) | 1 GB or more |

One exception to the two-profile rule: in P8 you run one test suite on `aws`, `azure` and `gcp` together. Those three need about 0.6 GB, so they fit when `core` and `mongo` are stopped.

Before you start k3d, stop the whole lab with `docker compose --profile "*" down`.

Check live use with `docker stats --no-stream`. Docker Desktop's total memory is capped in `.wslconfig` (see `setup/windows.md`).

## Reaching the lab from your own containers

Inside a container, `localhost` is the container itself, not your laptop. Use `host.docker.internal` instead, and add this to the service in your own `compose.yaml`:

```yaml
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

For example, a worker container reaches Floci at `http://host.docker.internal:4566` and PostgreSQL at `host.docker.internal:5432`.

## Git Bash and paths inside containers

Git Bash changes any argument that starts with `/` into a Windows path. That breaks a Docker command that names a path inside a container. Put `MSYS_NO_PATHCONV=1` in front of that one command:

```bash
MSYS_NO_PATHCONV=1 docker exec cloudlab-postgres-1 ls /var/lib/postgresql/data
```

Commands with no such path need nothing extra, for example `docker compose --profile core ps`. Never `export` the variable for the whole terminal: it breaks other commands, such as `python ~/script.py`.

## Try the drill profile

Toxiproxy (a proxy that can add faults) sits between a client and a database. `toxiproxy.json` defines two proxies, with the same names as in Shortly (P13): `postgres` (port 15432) and `redis` (port 16379).

```bash
docker compose --profile core --profile drill up -d
curl -s http://localhost:8474/proxies
```

Add a 500 ms delay to every PostgreSQL reply that goes through the proxy:

```bash
curl -s -X POST http://localhost:8474/proxies/postgres/toxics -H "Content-Type: application/json" -d '{"name":"slow_db","type":"latency","stream":"downstream","attributes":{"latency":500}}'
```

A query through `localhost:15432` is now slow, and a query to `localhost:5432` is not. Remove the delay, or reset every proxy:

```bash
curl -s -X DELETE http://localhost:8474/proxies/postgres/toxics/slow_db
curl -s -X POST http://localhost:8474/reset
```

In P13, Shortly runs its own Toxiproxy on port 8474. Stop the lab's copy first: `docker compose --profile drill down`.

## Troubleshooting

- **`port is already allocated`** or **`address already in use`**: another program uses that port. Find it with `docker ps --format "table {{.Names}}\t{{.Ports}}"`. A PostgreSQL installed on Windows also takes port 5432: stop it in the Windows Services app. Shortly (P7, P13) and k3d use port 8080 and 8474.
- **A service is not `Up`** or says `unhealthy`: read its last log lines, for example `docker compose --profile core logs --tail 30 postgres`.
- **PostgreSQL rejects the password `railseat`**: the password is set only when the volume is first made. Reset it with `docker compose --profile core down -v`. This deletes the data.
- **`type "vector" does not exist`**: run `CREATE EXTENSION IF NOT EXISTS vector;` in your database.
- **`docker compose down` did nothing**: name the profile, or use `--profile "*"`.
- **The laptop is slow**: run `docker stats --no-stream` and stop the profiles you are not using.
- **`Cannot connect to the Docker daemon`**: start Docker Desktop and wait until it says "Engine running".

## Image versions

The images are pinned in `docker-compose.yml`:

| Service | Image |
|---|---|
| PostgreSQL | `pgvector/pgvector:0.8.7-pg16` |
| Redis | `redis:7.4.12-alpine` |
| Mailpit | `axllent/mailpit:v1.33.1` |
| Floci | `floci/floci:2.4.0` |
| Azurite | `mcr.microsoft.com/azure-storage/azurite:3.37.0` |
| fake-gcs-server | `fsouza/fake-gcs-server:1.56.1` |
| Pub/Sub emulator | `gcr.io/google.com/cloudsdktool/google-cloud-cli:592.0.0-emulators` |
| MongoDB | `mongo:7.0.45` |
| Toxiproxy | `ghcr.io/shopify/toxiproxy:2.13.0` |
