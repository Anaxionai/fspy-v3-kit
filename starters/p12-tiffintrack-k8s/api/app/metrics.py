"""Prometheus metrics for the API (task 25): traffic, errors and latency, served on GET /metrics.

main.py adds record_request as a middleware and metrics_endpoint as GET /metrics: STARTER.md
shows the lines. Your code here will need: time, and Counter, Histogram, generate_latest and
CONTENT_TYPE_LATEST from prometheus_client.
"""

from fastapi import Request, Response

# Requests to these paths are not counted: they come from Prometheus and the probes, not from users.
NOT_COUNTED = {"/metrics", "/healthz", "/readyz"}

# TODO(task 25): REQUESTS, a Counter named tiffintrack_http_requests_total with the labels
#   method, route and status.
# TODO(task 25): DURATION, a Histogram named tiffintrack_http_request_duration_seconds with the
#   labels method and route.


async def record_request(request: Request, call_next) -> Response:
    """HTTP middleware: time each request, then count it in REQUESTS and DURATION.

    The route label is the route's template, such as /orders/{order_id}, never the raw path,
    because every raw id would make a new time series. The template is known only after
    call_next has routed the request.
    Edge cases: an exception counts as status 500 and is raised again; NOT_COUNTED paths are skipped.
    TODO(task 25): write it.
    """
    raise NotImplementedError("TODO(task 25): record the request's metrics")


def metrics_endpoint() -> Response:
    """GET /metrics: every metric in Prometheus's text format, with Prometheus's content type.

    TODO(task 25): write it.
    """
    raise NotImplementedError("TODO(task 25): serve the metrics")
