"""The merchant's JSON API under /v1. Every endpoint needs the API key."""

from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Header, Query
from fastapi.responses import JSONResponse

from mockpay import events, orders, payments, refunds
from mockpay.errors import ApiError
from mockpay.idempotency import run_idempotent
from mockpay.routes.deps import Ctx
from mockpay.schemas import OrderCreate, RefundCreate, WebhookResend
from mockpay.security import require_api_key
from mockpay.settlements import settlement_report

IdempotencyKey = Annotated[
    str | None,
    Header(alias="Idempotency-Key", description="Any unique text, for example a UUID"),
]

router = APIRouter(prefix="/v1", dependencies=[Depends(require_api_key)])

# Bodies that work as they stand when "Try it out" in /docs pre-fills them. Without these,
# Swagger fills optional fields with placeholders such as "return_url": "string", which fail.
NewOrder = Annotated[
    OrderCreate,
    Body(
        openapi_examples={
            "booking": {
                "summary": "A RailSeat booking",
                "value": {
                    "amount_paise": 125000,
                    "currency": "INR",
                    "receipt": "PNR0000001",
                    "return_url": "http://localhost:5173/bookings",
                },
            }
        }
    ),
]
NewRefund = Annotated[
    RefundCreate,
    Body(
        openapi_examples={
            "partial": {
                "summary": "A partial refund: put your payment's id in payment_id",
                "value": {"payment_id": "pay_your_payment_id", "amount_paise": 50000},
            }
        }
    ),
]
Resend = Annotated[
    WebhookResend,
    Body(
        openapi_examples={
            "three_copies": {
                "summary": "Three copies at once: put an id from GET /v1/events in event_id",
                "value": {"event_id": "evt_your_event_id", "copies": 3},
            }
        }
    ),
]


def created(body: dict[str, Any], replayed: bool) -> JSONResponse:
    """201 Created. A replayed answer says so in a header, as Stripe does."""
    headers = {"Idempotent-Replayed": "true"} if replayed else None
    return JSONResponse(body, status_code=201, headers=headers)


@router.post("/orders", status_code=201, tags=["Orders"], summary="Create an order")
async def create_order(
    body: NewOrder, ctx: Ctx, idempotency_key: IdempotencyKey = None
) -> JSONResponse:
    answer, replayed = run_idempotent(
        ctx,
        scope="orders",
        key=idempotency_key,
        request_data=body.model_dump(mode="json"),
        action=lambda: orders.create_order(ctx, body),
    )
    return created(answer, replayed)


@router.get("/orders/{order_id}", tags=["Orders"], summary="Get an order")
async def get_order(order_id: str, ctx: Ctx) -> dict[str, Any]:
    order = orders.find_order(ctx, order_id)
    if order is None:
        raise ApiError(404, "order_not_found", f"No order with id {order_id}.")
    return orders.order_json(ctx, order)


@router.get("/payments/{payment_id}", tags=["Payments"], summary="Get a payment")
async def get_payment(payment_id: str, ctx: Ctx) -> dict[str, Any]:
    payment = payments.find_payment(ctx, payment_id)
    if payment is None:
        raise ApiError(404, "payment_not_found", f"No payment with id {payment_id}.")
    return payments.payment_json(ctx, payment)


@router.post("/refunds", status_code=201, tags=["Refunds"], summary="Refund a payment")
async def create_refund(
    body: NewRefund, ctx: Ctx, idempotency_key: IdempotencyKey = None
) -> JSONResponse:
    answer, replayed = run_idempotent(
        ctx,
        scope="refunds",
        key=idempotency_key,
        request_data=body.model_dump(mode="json"),
        action=lambda: refunds.create_refund(ctx, body),
    )
    return created(answer, replayed)


@router.get("/settlements", tags=["Settlements"], summary="The settlement report for one day")
async def get_settlement(
    ctx: Ctx,
    day: Annotated[date, Query(alias="date", description="The day, YYYY-MM-DD (IST)")],
) -> dict[str, Any]:
    return settlement_report(ctx, day)


@router.post(
    "/simulate/webhook", status_code=202, tags=["Webhooks"], summary="Send a past event again"
)
async def simulate_webhook(body: Resend, ctx: Ctx) -> dict[str, Any]:
    delivery_ids = events.resend_event(ctx, body.event_id, body.copies)
    return {"event_id": body.event_id, "deliveries": delivery_ids, "status": "scheduled"}


@router.get("/events", tags=["Webhooks"], summary="Recent events, newest first")
async def list_events(
    ctx: Ctx,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    event_type: Annotated[str | None, Query(alias="type")] = None,
    order_id: str | None = None,
) -> dict[str, Any]:
    rows = events.list_events(ctx, limit=limit, event_type=event_type, order_id=order_id)
    items = [events.event_json(ctx, row) for row in rows]
    return {"count": len(items), "items": items}


@router.get("/events/{event_id}", tags=["Webhooks"], summary="One event and its deliveries")
async def get_event(event_id: str, ctx: Ctx) -> dict[str, Any]:
    event = events.find_event(ctx, event_id)
    if event is None:
        raise ApiError(404, "event_not_found", f"No event with id {event_id}.")
    return events.event_json(ctx, event)
