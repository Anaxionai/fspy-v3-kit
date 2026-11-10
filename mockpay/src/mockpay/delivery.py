"""The webhook sender: delivers events to the merchant's server, with retries.

It runs in the background for as long as MockPay runs. A few times a second
it looks for delivery rows whose time has come, sends each one, and writes
down every attempt.

- A 2xx answer means "delivered". MockPay stops.
- Anything else (another status code, a refused connection, no answer in
  time) means "try again later", after 1 s, then 5 s, then 25 s
  (MOCKPAY_RETRY_DELAYS). After the last retry MockPay gives up. You can
  still send the event again with POST /v1/simulate/webhook.

Because the plan lives in the database, stopping and starting MockPay does
not lose a webhook: unfinished deliveries carry on after a restart.
"""

import asyncio
import logging
import sqlite3
import time

import httpx

from mockpay import __version__, clock
from mockpay.context import Context
from mockpay.events import DELIVERED, GAVE_UP, SENDING, WAITING
from mockpay.payments import fail_timed_out_payments
from mockpay.signing import sign

log = logging.getLogger("mockpay.webhooks")


class DeliveryWorker:
    def __init__(self, ctx: Context, client: httpx.AsyncClient) -> None:
        self.ctx = ctx
        self.client = client
        self._main_task: asyncio.Task[None] | None = None
        self._sends: set[asyncio.Task[None]] = set()  # attempts in flight

    def start(self) -> None:
        resume_interrupted_deliveries(self.ctx)
        self._main_task = asyncio.create_task(self._run_forever(), name="mockpay-webhooks")

    async def stop(self) -> None:
        tasks = [*self._sends, *([self._main_task] if self._main_task else [])]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _run_forever(self) -> None:
        while True:
            try:
                self.start_due_work()
            except Exception:
                log.exception("The webhook sender hit an error. It will try again.")
            await asyncio.sleep(self.ctx.settings.poll_seconds)

    def start_due_work(self) -> None:
        fail_timed_out_payments(self.ctx)  # the "Pay (times out)" button, 30 s later
        for delivery in claim_due_deliveries(self.ctx):
            # One task per attempt, so a slow merchant server does not hold up the others.
            task = asyncio.create_task(self.send(delivery))
            self._sends.add(task)
            task.add_done_callback(self._sends.discard)

    async def send(self, delivery: sqlite3.Row) -> None:
        """Make one HTTP attempt for one delivery, and write down what happened."""
        settings = self.ctx.settings
        body = delivery["body"].encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"MockPay/{__version__}",
            "X-MockPay-Event-Id": delivery["event_id"],
            "X-MockPay-Signature": sign(body, settings.webhook_secret),
        }
        started = time.perf_counter()
        status_code: int | None = None
        error: str | None = None
        try:
            response = await self.client.post(settings.webhook_url, content=body, headers=headers)
            status_code = response.status_code
        except Exception as exc:  # any failure to get an answer counts as a failed try
            error = describe_error(exc, settings.answer_timeout_seconds)
        duration_ms = round((time.perf_counter() - started) * 1000)
        record_attempt(self.ctx, delivery, settings.webhook_url, status_code, error, duration_ms)


def resume_interrupted_deliveries(ctx: Context) -> None:
    """Rows left "sending" by a stop or a crash go back in the queue."""
    with ctx.db.transaction() as conn:
        conn.execute("UPDATE deliveries SET status = ? WHERE status = ?", (WAITING, SENDING))


def claim_due_deliveries(ctx: Context) -> list[sqlite3.Row]:
    """Pick every delivery whose time has come, and mark it "sending" so it is picked once."""
    with ctx.db.transaction() as conn:
        due = conn.execute(
            "SELECT d.id, d.event_id, d.kind, d.attempts, e.type, e.body"
            " FROM deliveries d JOIN events e ON e.id = d.event_id"
            " WHERE d.status = ? AND d.next_attempt_at <= ?"
            " ORDER BY d.next_attempt_at, d.id",
            (WAITING, time.time()),
        ).fetchall()
        conn.executemany(
            "UPDATE deliveries SET status = ? WHERE id = ?", [(SENDING, row["id"]) for row in due]
        )
    return due


def record_attempt(
    ctx: Context,
    delivery: sqlite3.Row,
    url: str,
    status_code: int | None,
    error: str | None,
    duration_ms: int,
) -> None:
    """Log one attempt, then decide: delivered, try again later, or give up."""
    attempt_no = delivery["attempts"] + 1
    retry_delays = ctx.settings.retry_delays
    next_attempt_at: float | None = None
    if status_code is not None and 200 <= status_code < 300:
        status = DELIVERED
    elif attempt_no <= len(retry_delays):
        status = WAITING
        next_attempt_at = time.time() + retry_delays[attempt_no - 1]
    else:
        status = GAVE_UP

    with ctx.db.transaction() as conn:
        conn.execute(
            "INSERT INTO delivery_attempts"
            " (delivery_id, attempt_no, url, status_code, error, duration_ms, attempted_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                delivery["id"],
                attempt_no,
                url,
                status_code,
                error,
                duration_ms,
                clock.iso_ms(clock.now()),
            ),
        )
        conn.execute(
            "UPDATE deliveries SET status = ?, attempts = ?, next_attempt_at = ? WHERE id = ?",
            (status, attempt_no, next_attempt_at, delivery["id"]),
        )

    # For example: "evt_x payment.captured (first), try 1: HTTP 500 after 12 ms. Next try in 1 s."
    answer = f"HTTP {status_code}" if status_code is not None else error
    if status == WAITING:
        then = f"Next try in {retry_delays[attempt_no - 1]:g} s."
    elif status == GAVE_UP:
        then = "Gave up: send it again with POST /v1/simulate/webhook."
    else:
        then = "Delivered."
    log.info(
        "%s %s (%s), try %d: %s after %d ms. %s",
        delivery["event_id"],
        delivery["type"],
        delivery["kind"],
        attempt_no,
        answer,
        duration_ms,
        then,
    )


def describe_error(exc: Exception, answer_timeout_seconds: float) -> str:
    """A short, plain explanation of why there was no HTTP answer."""
    if isinstance(exc, httpx.ConnectError):
        return "could not connect: is your server running, and is MOCKPAY_WEBHOOK_URL right?"
    if isinstance(exc, httpx.TimeoutException):
        return f"no answer within {answer_timeout_seconds:g} s"
    return f"{type(exc).__name__}: {exc}"
