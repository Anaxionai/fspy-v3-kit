"""Payments: orders, refunds and MockPay's webhook (P6 add-on).

Two routers, both included in app/main.py (see STARTER.md):
- `router` needs a signed-in user on every route, as P5's deny-by-default rule says.
- `webhook_router` has no user check: MockPay sends no token. The HMAC signature
  is its guard (task 10), and its route goes into PUBLIC_ROUTES.
Every amount comes from RailSeat's own data, never from the request.
"""

from fastapi import APIRouter, Depends, Header, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User
from app.payment_schemas import OrderIn, OrderOut, RefundOut
from app.security import current_user
from app.services.mockpay import MockPayClient, get_mockpay

router = APIRouter(tags=["payments"], dependencies=[Depends(current_user)])
webhook_router = APIRouter(tags=["webhooks"])

# MockPay sends the passenger back to My bookings after checkout.
RETURN_URL = "http://localhost:5173/bookings"


@router.post("/payments/orders", status_code=201, response_model=OrderOut)
async def create_payment_order(
    data: OrderIn,
    request: Request,
    response: Response,
    user: User = Depends(current_user),
    mockpay: MockPayClient = Depends(get_mockpay),
    session: AsyncSession = Depends(get_session),
    idempotency_key: str | None = Header(default=None),
):
    """Create a MockPay order for one of the user's bookings (task 9, steps 3-7).

    - Load the booking with your P5 ownership check (another passenger's PNR: 404).
      It must be `pending_payment`, else 409.
    - Add an `Order` (`created`) whose `amount_paise` is the booking's `fare_paise`.
    - Call `mockpay.create_order()`. A timeout (`httpx.TimeoutException`) gives 504,
      a MockPayError gives 502 with its message, and neither leaves an order behind.
    - Save MockPay's `id` as `gateway_order_id`; return `order_id` and `checkout_url`.
    """
    # TODO(task 11): require the Idempotency-Key header (else 400), claim it with
    # claim_key() before the work, replay or refuse a repeat, and save_reply() in the
    # same transaction. Mark a replayed reply with the header `Idempotent-Replayed: true`.
    raise NotImplementedError("TODO(task 9): create the order with the booking's fare")


@router.post("/bookings/{pnr}/refund", response_model=RefundOut)
async def refund_booking(
    pnr: str,
    request: Request,
    response: Response,
    user: User = Depends(current_user),
    mockpay: MockPayClient = Depends(get_mockpay),
    session: AsyncSession = Depends(get_session),
    idempotency_key: str | None = Header(default=None),
):
    """Cancel a paid booking and refund the fare minus the 25% fee (task 13, steps 2-7).

    - Your P5 ownership check, and your task 11 Idempotency-Key handling.
    - Only a `confirmed` booking with a `captured` payment: anything else gets 409.
    - `refund_split()` gives the amounts. Call `mockpay.refund()` with the key
      `refund-<PNR>`; an error gives 502 and a timeout 504, changing nothing.
    - Then, in one transaction: `refunded_paise`, `move()` for the payment and the
      order, the cancelled booking, and the two ledger transfers of step 7.
    """
    raise NotImplementedError(
        "TODO(task 13): refund the booking and post the transfers"
    )


@webhook_router.post("/payments/webhook")
async def mockpay_webhook(
    request: Request, session: AsyncSession = Depends(get_session)
):
    """Receive MockPay's events (task 10, steps 3-6).

    - Read the raw body with `await request.body()` before any JSON parsing, and check
      `X-MockPay-Signature` with `signature_ok()` and MOCKPAY_WEBHOOK_SECRET. A bad
      signature: 400, and nothing changes.
    - `payment.captured`: in one transaction, find the order by `data.order_id`, add a
      `captured` Payment, `move()` the order to `paid`, confirm the booking.
    - `payment.failed`: add a `failed` Payment and leave the order `created`.
    - Any other event type: 200 and change nothing.
    """
    # TODO(task 11): right after the signature check, record_event(); a repeat answers
    # 200 {"status": "duplicate"} and changes nothing.
    # TODO(task 12): on payment.captured, post "capture:<payment id>" (mockpay_clearing
    # against ticket_sales) in the same transaction as the status moves.
    # TODO(task 13): refund.processed answers 200 and changes nothing: the refund route
    # recorded it already.
    raise NotImplementedError(
        "TODO(task 10): check the signature, then handle the event"
    )
