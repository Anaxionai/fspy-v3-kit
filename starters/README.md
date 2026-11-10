# Guided starters

Every project in the course has three levels. Your mentor tells you yours after the week-2 placement check and may change it as you go.

- **Core**: you start from an empty folder and follow the task brief.
- **Guided**: you start from the starter in this folder. It does the set-up for you: project files, folder layout, configuration, test set-up, types and function signatures. Every piece of logic the tasks ask for is still yours to write. It is marked `TODO(task NN)`, with NN the task's number in that module.
- **Stretch**: Core, plus the module's Stretch goals.

A starter never contains a solution. AxReview grades Guided and Core work against the same Source of Truth.

## Two kinds

- **Starters** hold a whole product folder. You copy one in once, in the project's first build task, and then keep growing your copy.
- **Add-ons** hold only new files for a product you already have. Copying one never replaces your files (`cp -n`). Where one of your existing files must change, the add-on's `STARTER.md` shows the lines to add and the task that adds them.

| Folder | Project | Module | Kind | Copy into |
|---|---|---|---|---|
| `p01-paisalens/` | P1 PaisaLens | 3 | starter | `paisalens/` |
| `p02-matchcentre/` | P2 Match Centre | 4 | starter | `matchcentre/` |
| `p03-railseat-api/` | P3 RailSeat API | 5 | starter | `railseat/` (the whole product folder) |
| `p04-railseat-web/` | P4 RailSeat web | 6 | starter | `railseat/web/` |
| `p05-railseat-accounts/` | P5 accounts and roles | 7 | add-on | your `railseat/` |
| `p06-railseat-payments/` | P6 payments | 8 | add-on | your `railseat/` |
| `p07-shortly/` | P7 Shortly | 9 | starter | `shortly/` |
| `p08-reelpipe/` | P8 ReelPipe | 10 | starter | `reelpipe/` |
| `p09-tiffintrack/` | P9 TiffinTrack | 11 | starter | `tiffintrack/` |
| `p10-railseat-scale/` | P10 RailSeat at scale | 12 | add-on | your `railseat/` |
| `p11-shortly-pipeline/` | P11 Shortly ships | 13 | add-on | your `shortly/` |
| `p12-tiffintrack-k8s/` | P12 TiffinTrack on Kubernetes | 14 | add-on | your `tiffintrack/` |
| `p13-shortly-live/` | P13 Shortly live | 15 | add-on | your `shortly/` |

## How to use one

1. Pull the kit first, so you have the latest version: `cd ~/fspy-v3-kit && git pull`.
2. Open the folder's `STARTER.md`. It gives the exact copy command, how to run the project, and a table of every TODO with its task number.
3. In Git Bash, `cd` to the task folder the brief names, then run the copy command from `STARTER.md`, for example:
   ```bash
   cp -r ~/fspy-v3-kit/starters/p01-paisalens paisalens
   ```
4. Install and check it as `STARTER.md` says (`uv sync` and `uv run pytest`, or `npm install` and `npm test`). Everything passes as shipped.
5. Work through the tasks. When a task's TODOs are done, remove the `skip` or `todo` marks from that task's tests so they run.

## Good to know

- **Skipped tests are normal.** Before you write a task's code, its tests show as "skipped" or "todo" in the output. They are not failures. Paste the output as the brief asks.
- **`STARTER.md` is not your README.** You write the product's `README.md` yourself in the project's wrap-up.
- **Line endings:** the kit's `.gitattributes` keeps every text file in LF. If you create a shell script, check that VS Code's status bar says `LF`.
- **Versions:** the starters use the versions in the kit's `VERSIONS.md`. Commit the lock files (`uv.lock`, `package-lock.json`) with your code.
- **Stuck on a TODO?** Read the task's Learn links, ask AxTutor to explain the idea (not to write the code), then ask your mentor.
