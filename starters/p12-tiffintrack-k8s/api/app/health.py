"""Health endpoints for the Kubernetes probes (task 21).

Add them to the API in main.py: STARTER.md shows the two lines.
Your code here will need: asyncio (wait_for), os.path.exists, JSONResponse from fastapi.responses,
and your MongoDB client (with the P9 starter, get_db() from app.db).
"""

from fastapi import APIRouter

router = APIRouter()

# A lab switch for task 21, never for production: while this file exists, /healthz fails,
# so the liveness probe fails and Kubernetes restarts the container.
UNHEALTHY_FILE = "/tmp/unhealthy"


@router.get("/healthz")
async def healthz():
    """Liveness: can this process still answer? 200, without touching any database.

    Edge case: while UNHEALTHY_FILE exists, answer 500 instead (the lab switch).
    TODO(task 21): write it.
    """
    raise NotImplementedError("TODO(task 21): the liveness endpoint")


@router.get("/readyz")
async def readyz():
    """Readiness: can this pod serve orders now? Ping MongoDB and wait at most 1 second.

    200 when MongoDB answers. 503 when it fails or takes longer, so that Kubernetes takes the
    pod out of the Service until MongoDB is back, without restarting it.
    TODO(task 21): write it.
    """
    raise NotImplementedError("TODO(task 21): the readiness endpoint")
