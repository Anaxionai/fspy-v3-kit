"""Sends click jobs to the Celery worker through Redis (task 19).

A redirect then never writes to PostgreSQL: the worker in worker/tasks.py does.
"""

# TODO(task 19): create a Celery client on settings.redis_url here.
#   It only sends jobs, so it needs the broker and no task code.


def send_click(code: str) -> None:
    """Queue one count_click job for `code`.

    Input: the code that was just followed. The job's arguments are the code and
    ts, the click time from time.time().
    Must do: send the job by name, "count_click", exactly as the worker registers it.
    Edge case: do not let the send retry, so a redirect never waits for a broker
    that is down. GET /{code} catches the error, logs it and still redirects.
    """
    raise NotImplementedError("TODO(task 19): send the count_click job by name")
