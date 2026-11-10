"""HTML pages: the hosted checkout (for customers) and the dashboard (for you)."""

from datetime import datetime
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from mockpay import events, orders, payments
from mockpay.dashboard import dashboard_data
from mockpay.errors import ApiError
from mockpay.money import format_inr
from mockpay.payments import Outcome
from mockpay.routes.deps import Ctx

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")

GOOD = {"paid", "captured", "processed", "delivered"}
BAD = {"failed", "gave_up"}
WAITING = {"pending", "attempted", "waiting", "sending"}


def tone(status: Any) -> str:
    """The colour of a status label: good, bad, waiting or plain."""
    if isinstance(status, int):
        return "good" if 200 <= status < 300 else "bad"
    if status in GOOD:
        return "good"
    if status in BAD:
        return "bad"
    return "waiting" if status in WAITING else "plain"


def when(iso_text: str | None, ms: bool = False) -> str:
    """'2026-11-10T15:45:30.123+05:30' -> '10 Nov 15:45:30' (or '15:45:30.123' with ms)."""
    if not iso_text:
        return ""
    moment = datetime.fromisoformat(iso_text)
    if ms:
        return moment.strftime("%H:%M:%S.%f")[:-3]
    return moment.strftime("%d %b %H:%M:%S")


templates.env.filters["inr"] = format_inr
templates.env.filters["when"] = when
templates.env.globals["tone"] = tone


def message_page(request: Request, status_code: int, title: str, text: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request, "message.html", {"title": title, "text": text}, status_code=status_code
    )


def add_query(url: str, **params: str) -> str:
    """Add query parameters to a URL that may already have some."""
    parts = urlsplit(url)
    query = parse_qsl(parts.query, keep_blank_values=True) + list(params.items())
    return urlunsplit(parts._replace(query=urlencode(query)))


@router.get("/")
async def home() -> RedirectResponse:
    return RedirectResponse("/dashboard")


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/checkout/{order_id}", response_class=HTMLResponse)
async def checkout_page(request: Request, order_id: str, ctx: Ctx) -> Response:
    order = orders.find_order(ctx, order_id)
    if order is None:
        return message_page(request, 404, "Order not found", f"MockPay has no order {order_id}.")
    return templates.TemplateResponse(
        request,
        "checkout.html",
        {
            "order": orders.order_json(ctx, order),
            "payments": payments.payments_for_order(ctx, order_id),
            "timeout_seconds": ctx.settings.timeout_seconds,
        },
    )


@router.post("/checkout/{order_id}/pay")
async def pay(
    request: Request, order_id: str, outcome: Annotated[Outcome, Form()], ctx: Ctx
) -> Response:
    """A button on the checkout page was pressed. Make the payment, then send the customer back."""
    try:
        payment = payments.start_payment(ctx, order_id, outcome)
    except ApiError as exc:
        return message_page(request, exc.status_code, "Payment not possible", exc.message)

    order = orders.find_order(ctx, order_id)
    assert order is not None
    if order["return_url"]:
        # The redirect only says "the customer is back". It is not proof of
        # payment: the merchant must wait for the webhook (or ask the API).
        target = add_query(order["return_url"], order_id=order_id, payment_id=payment["id"])
    else:
        target = f"/checkout/{order_id}/result?" + urlencode({"payment_id": payment["id"]})
    # 303 See Other: the browser follows it with a GET, so a refresh cannot pay twice.
    return RedirectResponse(target, status_code=303)


@router.get("/checkout/{order_id}/result", response_class=HTMLResponse)
async def checkout_result(request: Request, order_id: str, payment_id: str, ctx: Ctx) -> Response:
    """Shown after paying when the order has no return_url."""
    payment = payments.find_payment(ctx, payment_id)
    if payment is None or payment["order_id"] != order_id:
        return message_page(request, 404, "Payment not found", f"No payment {payment_id}.")
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "payment": payment,
            "timeout_seconds": ctx.settings.timeout_seconds,
        },
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, ctx: Ctx, refresh: int = 5) -> Response:
    """refresh: reload the page every this many seconds; 0 turns it off."""
    context = dashboard_data(ctx)
    context["refresh"] = max(0, refresh)
    return templates.TemplateResponse(request, "dashboard.html", context)


@router.post("/dashboard/events/{event_id}/resend")
async def dashboard_resend(request: Request, event_id: str, ctx: Ctx) -> Response:
    """The "Send again" button: the same as POST /v1/simulate/webhook, without the API key."""
    try:
        events.resend_event(ctx, event_id)
    except ApiError as exc:
        return message_page(request, exc.status_code, "Event not found", exc.message)
    return RedirectResponse("/dashboard", status_code=303)
