"""Prometheus metrics for Shortly (task 7), in the same pattern as metrics.py in P12.

Install the client once, in api/:  uv add prometheus-client
Then wire this file into app/main.py: STARTER.md shows the three lines.
"""

from fastapi import APIRouter, Request, Response
from starlette.middleware.base import RequestResponseEndpoint

router = APIRouter()

# TODO(task 7): define the metrics with prometheus_client, with exactly these names and labels.
#   The dashboard, the alert and the mentor's drill notes use them.
#     Counter    shortly_http_requests_total             labels method, route, status
#     Histogram  shortly_http_request_duration_seconds   labels method, route
#     Counter    shortly_cache_lookups_total             label  result: hit, miss or error
#   app/cache.py imports the cache counter and counts every lookup in get_target().


async def metrics_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Time and count every request, then return the response unchanged.

    Edge cases:
    - Label `route` with the route template, such as /links/{code}/stats, never the raw path:
      every new code would make a new time series. After call_next, the template is in
      request.scope["route"].path. A request that matched no route has none: use a fixed
      label such as "unmatched".
    - An exception counts as status 500; record it, then raise the exception again.
    - Skip /metrics and /healthz, so scrapes and health checks do not count as traffic.
    """
    raise NotImplementedError("TODO(task 7): record the request counter and the latency histogram")


@router.get("/metrics")
def metrics() -> Response:
    """GET /metrics: the text that Prometheus scrapes.

    Return generate_latest() with the media type CONTENT_TYPE_LATEST (both from prometheus_client).
    """
    raise NotImplementedError("TODO(task 7): return generate_latest() as CONTENT_TYPE_LATEST")
