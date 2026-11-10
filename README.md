# FSPY-V3 course kit

This is the course kit for **FSPY-V3, Full-Stack Engineering (React, FastAPI & PostgreSQL) v3**.
It holds what your tasks need beyond your own code. That is the laptop setup guides, a cloud lab that runs on your laptop, practice data, small tools, the Guided starters and the capstone briefs.
Your task briefs link to files in this kit.

## Get the kit

Run this once, in Git Bash, in week 2:

```bash
cd ~ && git clone https://github.com/Anaxionai/fspy-v3-kit.git
```

This makes the folder `~/fspy-v3-kit`, which is `C:\Users\<your name>\fspy-v3-kit` on Windows.
Keep it next to your course repository, never inside it.

Check it: `ls ~/fspy-v3-kit` lists `README.md`, `VERSIONS.md`, `setup` and the other folders below.

## Update the kit

When a task says "Run `git pull` in your copy of the course kit", run:

```bash
cd ~/fspy-v3-kit
git pull
```

Do not change the kit's files. Copy a file into your own repository first, then change your copy.
If `git pull` says your local changes would be overwritten, run `git restore .` in the kit folder. It undoes your changes to the kit's files. Then run `git pull` again.

Every command in the kit's READMEs is written for **Git Bash**. [`setup/windows.md`](setup/windows.md) sets it up.

## What is in the kit

| Path | What it is | Used in |
|---|---|---|
| `README.md` | This file | the whole course |
| `VERSIONS.md` | The version of every tool, image and library the course uses | the whole course |
| `LICENSE` | The MIT licence for the kit's code | — |
| `setup/windows.md` | Windows laptop setup: Git Bash, VS Code, uv and Python, WSL 2, Docker Desktop, Node.js | Launchpad, weeks 1 and 2 |
| `setup/wslconfig.example` | A `.wslconfig` file that limits WSL 2's memory and swap | Launchpad, week 2 |
| `setup/coding-agent.md` | Setting up a coding agent, using it safely, and the `AGENT_LOG.md` format | Capstone, CP3 and CP4 |
| `try-it.md` | Free sites where you practise each new idea in the browser | learn cards |
| `cloudlab/` | The cloud lab: one Docker Compose file with profiles for PostgreSQL, Redis, Mailpit, MongoDB, AWS, Azure and Google Cloud emulators, and Toxiproxy. Its README has the ports, passwords and memory advice. | map weeks, P3 to P13 |
| `cloudlab/aws/`, `azure/`, `gcp/` | Using each cloud's emulator from the command line and from Python | map weeks, P8, P11 |
| `cloudlab/k3d/` | A Kubernetes cluster on your laptop with k3d | P12 |
| `cloudlab/budget/` | A $5 budget with alerts, on the AWS emulator and on a real account | map weeks, P11, P13 |
| `data/public-apis.md` | Free public APIs that need no key, with one example address each | map weeks |
| `data/sample-db/` | `stations.sql`: one table of 40 Indian railway stations, and how to load it | map weeks |
| `data/upi/` | `make_statement.py`: your own fake UPI bank statement, plus a sample and a starter rules file | P1 PaisaLens |
| `data/railseat/` | RailSeat's seed data (stations, trains, coaches, stops), its generator, its travel rules and the Gemini API guide | map weeks, P3 to P6, P10 |
| `tools/cricket-replay/` | `replay.py`: replays a real IPL match ball by ball as a live feed on port 8765 | P2 Match Centre |
| `mockpay/` | MockPay, the course's mock payment gateway, in Docker on port 9090 | P6 |
| `capstone/` | How the capstone works, the four product briefs, and the plan template | CP1 to CP4 |
| `starters/` | The Guided starters: a starting point for each project, for students on the Guided level | all projects |

## Running the kit's Python scripts

The scripts in `data/upi`, `data/railseat` and `tools/cricket-replay` use only Python's standard library. Start each one with `uv run`, for example:

```bash
cd ~/fspy-v3-kit/data/upi
uv run make_statement.py --student <your student id>
```

Each of those folders has its own tests. Run them in the folder with `uv run --with pytest pytest -q`.

## Line endings

The kit's `.gitattributes` file makes Git check out every text file with LF line endings, on Windows too.
Shell scripts and data files then work in Git Bash and inside Linux containers. Do not convert them to CRLF.

## Licence and attribution

- **The kit's code** is under the MIT licence: see [`LICENSE`](LICENSE). That covers the scripts, tests and configuration files written for the kit, unless a folder says otherwise.
- **Made-up data.** The UPI statements and RailSeat's trains, timetables and travel rules are made up by the kit, and you may use them freely. The people, small shops and employers in the statements are invented. Real company names, such as Swiggy or Netflix, appear only to make the data look real. RailSeat and MockPay are training products: they have no link with Indian Railways, IRCTC or any payment company.
- **Station facts.** Station codes, names, states and zones are public facts. The coordinates, platform counts and opening years come from English Wikipedia, read in November 2026. The kit uses those facts, not Wikipedia's text.
- **Cricket data.** `tools/cricket-replay` downloads ball-by-ball data from [Cricsheet](https://cricsheet.org). Cricsheet makes it available under the [Open Data Commons Attribution License 1.0](https://opendatacommons.org/licenses/by/1-0/). The kit itself holds no Cricsheet data: its test match is made up. Any public page that shows Cricsheet data must say so, for example: *Ball-by-ball data from Cricsheet (cricsheet.org), licensed under ODC-By 1.0.*
- **Public APIs** in `data/public-apis.md` each have their own terms; that file lists the ones that ask for credit.
- **Tools and images.** The tools and Docker images the course uses keep their own licences. Docker Desktop is free under the Personal plan for individual learning. It is also free for small businesses with fewer than 250 employees and less than $10 million in yearly revenue.
- Company and product names belong to their owners.
