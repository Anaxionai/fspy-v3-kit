"""OpenTelemetry traces for the API (task 25). The spans print to the pod's log.

First install the packages in tiffintrack/ (task 25, step 1):
    uv add opentelemetry-sdk opentelemetry-instrumentation-fastapi prometheus-client
Your code here will need: trace from opentelemetry, Resource from opentelemetry.sdk.resources,
TracerProvider from opentelemetry.sdk.trace, and BatchSpanProcessor and ConsoleSpanExporter
from opentelemetry.sdk.trace.export.
"""

SERVICE_NAME = "tiffintrack-api"


def setup_tracing() -> None:
    """Make SERVICE_NAME's tracer provider the global one, printing spans in batches to the log.

    main.py calls this once, before it instruments the app. STARTER.md shows the lines.
    TODO(task 25): write it.
    """
    raise NotImplementedError("TODO(task 25): set up the tracer provider")
