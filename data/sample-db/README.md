# Sample database: 40 Indian railway stations

`stations.sql` makes one small table, `stations`, with 40 real Indian railway stations.
You use it in the map weeks for your first `SELECT` queries.

## The table

| Column | Type | Meaning | Example |
|---|---|---|---|
| `code` | `VARCHAR(5)`, primary key | The Indian Railways station code | `NDLS` |
| `name` | `TEXT` | The station's name | `New Delhi` |
| `state` | `TEXT` | The state or union territory | `Delhi` |
| `zone` | `VARCHAR(5)` | The railway zone, as a short code | `NR` |
| `platforms` | `INTEGER` | The number of platforms | `16` |
| `opened_year` | `INTEGER` | The year the station opened | `1926` |

The zone codes:

| Code | Zone | Code | Zone | Code | Zone |
|---|---|---|---|---|---|
| `NR` | Northern | `NER` | North Eastern | `NFR` | Northeast Frontier |
| `ER` | Eastern | `SER` | South Eastern | `ECR` | East Central |
| `ECoR` | East Coast | `NCR` | North Central | `NWR` | North Western |
| `WCR` | West Central | `WR` | Western | `CR` | Central |
| `SECR` | South East Central | `SR` | Southern | `SWR` | South Western |
| `SCR` | South Central | `SCoR` | South Coast | | |

The codes, names, states and zones are real.
The platform counts and opening years come from each station's English Wikipedia page, read in November 2026.
Stations change over time, so treat the numbers as practice data, not as travel information.

## Load it into the cloud lab's PostgreSQL

Run every command in Git Bash. The cloud lab's PostgreSQL has the user `railseat`, the password `railseat` and the database `railseat`.

**1. Start the cloud lab's `core` profile** (PostgreSQL, Redis and Mailpit):

```bash
cd ~/fspy-v3-kit/cloudlab
docker compose --profile core up -d
docker compose --profile core ps
```

Wait until the PostgreSQL line says `(healthy)`. The container is named `cloudlab-postgres-1`.

**2. Load the file.** Use one of these two ways.

The way the map-week task uses: copy the file into the container, then run it there. Stay in the `cloudlab` folder:

```bash
MSYS_NO_PATHCONV=1 docker cp ../data/sample-db/stations.sql cloudlab-postgres-1:/tmp/stations.sql
MSYS_NO_PATHCONV=1 docker exec cloudlab-postgres-1 psql -U railseat -d railseat -f /tmp/stations.sql
```

`MSYS_NO_PATHCONV=1` stops Git Bash from rewriting `/tmp/stations.sql` into a Windows path, such as `C:/Users/you/AppData/Local/Temp/stations.sql`.
Without it, `psql` says `No such file or directory`.

Or in one command: `docker exec -i` passes the file to `psql` through its input, so no path goes into the container:

```bash
cd ~/fspy-v3-kit
docker exec -i cloudlab-postgres-1 psql -U railseat -d railseat < data/sample-db/stations.sql
```

Both ways print:

```text
CREATE TABLE
INSERT 0 40
```

You can run the file again. It then prints a `NOTICE` that the table already exists, `CREATE TABLE` and `INSERT 0 0`, and changes nothing.

**3. Check it:**

```bash
docker exec cloudlab-postgres-1 psql -U railseat -d railseat -c "SELECT count(*) FROM stations;"
```

The count is 40.

**4. Open `psql` to type your own queries:**

```bash
docker exec -it cloudlab-postgres-1 psql -U railseat -d railseat
```

The prompt becomes `railseat=#`. Leave with `\q`.
Run this in VS Code's terminal. In the separate Git Bash window, `-it` can fail with `the input device is not a TTY`; then put `winpty` at the front: `winpty docker exec -it cloudlab-postgres-1 psql -U railseat -d railseat`.

## Start again with an empty table

```bash
docker exec cloudlab-postgres-1 psql -U railseat -d railseat -c "DROP TABLE IF EXISTS stations;"
```

Then load the file again as in step 2.

## Before P3: remove this table

In P3 you design RailSeat's own `stations` table, in the same `railseat` database.
Remove this practice table first, with the `DROP TABLE` command above. Otherwise your first migration finds a `stations` table that it did not make.
