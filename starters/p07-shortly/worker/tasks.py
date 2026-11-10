"""Shortly's Celery worker: counts clicks off the request path (task 19).

The same image as the API runs it. Compose starts it with
    celery -A worker.tasks worker --loglevel=INFO
On Windows, a worker on your laptop (outside Docker) also needs --pool=solo.

It reads REDIS_URL and DATABASE_URL from the environment, like the API.
"""

import os

from celery import Celery
from sqlalchemy import create_engine

app = Celery("shortly", broker=os.environ["REDIS_URL"])

# A sync engine: a Celery task is a plain function, and psycopg 3 also works sync.
engine = create_engine(os.environ["DATABASE_URL"])

# TODO(task 21): create a sync Redis client on REDIS_URL here, with decode_responses=True.


# Keep the name "count_click": the API sends jobs by this name, and P11 and P13 rely on it.
# TODO(task 19): make Celery retry this task automatically, with back-off, when
#   sqlalchemy.exc.OperationalError is raised (the database is down or restarting).
@app.task(name="count_click")
def count_click(code: str, ts: float) -> None:
    """Add 1 to the clicks of the link `code`.

    Inputs: the code, and ts, the click time in seconds (time.time() at the redirect).
    Output: none. An unknown code changes no row, and that is not an error.
    """
    # TODO(task 19): add 1 to links.clicks for this code in PostgreSQL, in one UPDATE,
    #   so two workers can never lose a click.
    # TODO(task 21): also record the click in Redis: one hash field per India day in
    #   clicks:<code>, and one point for the code in the sorted set top:links.
    #   The India day of ts: datetime.fromtimestamp(ts, ZoneInfo("Asia/Kolkata")).date().isoformat()
    raise NotImplementedError("TODO(task 19): add 1 to clicks for this code")
