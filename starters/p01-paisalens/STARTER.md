# PaisaLens Guided starter (P1, module 3)

This folder is a ready-made `paisalens/` project for the Guided level of P1.
It does the set-up for you: the uv project, the package layout, pytest, and
the name and signature of every function the briefs ask for.
It gives you no answers. Each function body raises
`NotImplementedError("TODO(task NN): ...")`, and you write it in task NN.

## What is included

- `pyproject.toml`: the uv project `paisalens` for Python 3.12. The
  `paisalens` command runs `main()` until task 22. Typer and Rich are
  installed, and pytest is a development dependency. `uv.lock` pins every
  version, so your install matches everyone else's.
- `.python-version` (3.12) and `.gitignore`, which keeps `.venv/` and
  caches out of Git.
- `src/paisalens/`: `__init__.py`, `load.py`, `models.py`, `clean.py`,
  `categorise.py`, `report.py`, `recurring.py`, `errors.py` and `cli.py`.
  Each stub has a docstring that says what it must do.
- `tests/`: one file per module, holding only a plan of the tests you write,
  and `test_starter_checks.py`, four ready-made checks (see below).

Not included, because they are yours: `data/statement.csv` (task 6),
`rules.json` (task 8), `tests/data/mini_statement.csv` (task 23) and
`README.md` (task 25).

## Copy it in (task 6, step 1)

First run `git pull` in your kit folder, as task 6 says. Then, in Git Bash,
in task 6's folder:

```bash
cp -r ~/fspy-v3-kit/starters/p01-paisalens paisalens
cd paisalens
```

Copy the starter only once, in task 6. From task 7 on, you copy your own
`paisalens/` folder forward, as each brief says.

## Run it

```bash
uv run paisalens     # Hello from paisalens!
uv run pytest -q     # 4 skipped
```

Then go on with step 3 of task 6. Step 2 also lists a `README.md`: you have
this `STARTER.md` instead, and you write `README.md` in task 25.

`uv add --dev pytest` (task 10) and `uv add typer rich` (task 22) are done
already. If you run them, nothing changes.

## The starter checks

`tests/test_starter_checks.py` checks the results of `rupees` (task 9),
`month_of` with a date (task 18), `is_monthly` (task 20) and `bar` (task 24).
Each check is skipped until its task. When you finish that task, delete the
`@pytest.mark.skip(...)` line above the check and run `uv run pytest -q`.
They do not count as your tests: the tests each task asks for are yours.

## Your TODOs

| Task | Files | What you write |
|---|---|---|
| 6 | `load.py`, `__init__.py` | `to_paise`, `is_broken`, `read_statement`; `main()` prints the summary |
| 7 | `report.py`, `clean.py` | `month_of`, `monthly_totals`, `by_merchant`; a first `clean_merchant` |
| 7 | `load.py`, `__init__.py` | the merchant on each row, repeats skipped; months and top 10 printed |
| 8 | `categorise.py`, `report.py`, `__init__.py` | `load_rules`, `categorise`, `by_category`; the category totals |
| 9 | `report.py`, `__init__.py` | `rupees`, `render_report`; `data/report.txt` |
| 10 | `tests/test_load.py`, `test_clean.py`, `test_categorise.py` | your first tests, 6 or more |
| 18 | `models.py`, `load.py` | the `Transaction` fields; `parse_row`; a bad date in `is_broken` |
| 18 | `report.py`, `categorise.py`, `__init__.py`, `tests/test_categorise.py` | attributes in place of dict keys |
| 19 | `clean.py`, `tests/test_clean.py` | `clean_merchant` with regular expressions, `ALIASES`; a parametrised test |
| 20 | `models.py`, `recurring.py`, `__init__.py`, `tests/test_recurring.py` | `Subscription`, `is_monthly`, `find_recurring`; three tests |
| 21 | `errors.py`, `load.py`, `__init__.py`, `tests/test_load.py` | `BadRow`, `ErrorReport`; `read_statement(path, report)`; `pytest.raises` tests |
| 22 | `cli.py`, `pyproject.toml`, `__init__.py` | `load_all`, the three commands, the script line; delete `main()` |
| 23 | `tests/conftest.py`, `test_load.py`, `test_categorise.py`, `test_recurring.py`, `test_cli.py` | the fixtures and the pipeline tests |
| 24 | `report.py`, `cli.py`, `tests/test_cli.py` | `bar`, `month_table`, `category_table`; the tables and `--plain` |

Task 25, the wrap-up, has no TODO: you write `README.md` and `EXPLAIN.md`,
not code.

To see what is left, search the folder for `TODO` with Ctrl+Shift+F in
VS Code. Delete each TODO comment when you have done it.

## What you still write yourself

Everything a task asks for:

- every function body, and the code in `main()`;
- the fields of `Transaction` and `Subscription`, and the `BadRow` class;
- the Typer commands and their options;
- every test and fixture, and the small test statement;
- your rules, `NOTES.md`, `AI_LOG.md`, `evidence.md` and the wrap-up files.

The starter checks test only four results. They never replace your tests.
