"""Test set-up that every test file shares.

It reads reelpipe/.env (if it exists) into the environment before any test runs, so
`uv run pytest -q` talks to the same emulators as the API. A variable already set in your
terminal wins over the value in .env.
"""

import os
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def load_env_file(path: Path) -> None:
    """Copy each NAME=value line of path into os.environ, unless NAME is already set."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip('"').strip("'"))


load_env_file(ENV_FILE)

# TODO(task 22): move the `backend` fixture here from test_backends.py, parametrised over
#   "s3", "azure" and "gcs". Skip a backend whose emulator port does not answer, with a clear reason.
