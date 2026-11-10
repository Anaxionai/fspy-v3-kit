# P6 Guided add-on: RailSeat payments

New files for **your own** `railseat/` folder, the one you copy forward from P5. You get the
money helpers, the MockPay client, the payment and ledger routes, a fake MockPay for tests, one
test file per task and the Pay and refund buttons. Every piece of logic is a TODO for you.
Nothing here replaces a file you already have. MockPay's `README.md` in the kit is the reference.

## What is included
| Path in `railseat/` | What it is |
|---|---|
| `api/app/money.py` | `parse_rupees`, `format_paise`, `split_paise`: TODOs. |
| `api/app/payment_schemas.py` | Ready. Request and reply models; no request holds an amount. |
| `api/app/services/fares.py` | `FARES_PAISE` ready; `fare_for` and `refund_split`: TODOs. |
| `api/app/services/order_states.py` | Status lists and `InvalidMove` ready; the move dicts and `move()`: TODOs. |
| `api/app/services/mockpay.py` | `get_mockpay()` ready; `MockPayClient` methods, `sign()`, `signature_ok()`: TODOs. |
| `api/app/services/idempotency.py`, `ledger.py` | Repeat-proofing and the double-entry ledger: TODOs. |
| `api/app/routers/payments.py`, `ledger.py` | Every route's path, models and dependencies; the bodies are TODOs. |
| `api/tests/fakes.py` | `FakeMockPay` and `signed_event()`: TODOs. |
| `api/tests/fixtures/payment_captured.json` | README section 5's example body: one line, no newline at the end. |
| `api/tests/test_*.py` | One file per test module of the briefs. Each test says what to check, and is skipped. |
| `web/src/payments/` | `PayButton.tsx`, `RefundButton.tsx` ready; `formatPaise()`, `startCheckout()`, `requestRefund()`: TODOs. |
| `docs/payments.md` | Two empty Mermaid state diagrams for task 8. |

## Copy it in (task 8)
In Git Bash, in the task folder, after you copied `railseat/` from P5:
```bash
cp -rn ~/fspy-v3-kit/starters/p06-railseat-payments/{api,web,docs} railseat/
```
`-n` never overwrites a file you have. Never open and re-save `payment_captured.json` in an
editor that adds a newline at the end: the signature covers those exact bytes.
Then change your own files:
1. **`app/settings.py`:** add these lines (the values go in `api/.env` in tasks 9 and 10). No
   such file? You did P5 at Core level: copy the P5 add-on's `api/app/settings.py` first and
   run `uv add python-dotenv`.
```python
MOCKPAY_URL = os.environ.get("MOCKPAY_URL", "http://localhost:9090")
MOCKPAY_API_KEY = os.environ.get("MOCKPAY_API_KEY", "")
MOCKPAY_WEBHOOK_SECRET = os.environ.get("MOCKPAY_WEBHOOK_SECRET", "")
```
2. **`app/models.py`:** the models in the briefs: `fare_paise` on `Booking`, `Order` and
   `Payment` (task 8), `WebhookEvent` and `IdempotencyKey` (task 11), `LedgerEntry` (task 12).
   Autogenerate does not notice a changed `postgresql_where`, so widen P3's partial unique
   index (task 8, step 5) by hand in that migration: drop the index, then create it again.
3. **`app/main.py`:** `from app.routers import ledger, payments`, then
   `app.include_router(payments.router)` (task 9), `app.include_router(payments.webhook_router)`
   (task 10) and `app.include_router(ledger.router)` (task 12, once it is admin-only).
   Add `"Idempotency-Key"` to the CORS `allow_headers` in task 11.
4. **`tests/test_permissions.py` (P5):** add `("POST", "/payments/webhook")` to `PUBLIC_ROUTES` (task 10).
5. **`tests/conftest.py`:** empty `orders` and `payments` (task 8), `webhook_events` and
   `idempotency_keys` (task 11) and `ledger_entries` (task 12) with your other tables. In task 9,
   add this fixture, so no test calls the real MockPay:
```python
from app.main import app
from app.services.mockpay import get_mockpay
from tests.fakes import FakeMockPay


@pytest.fixture
def fake_mockpay():
    fake = FakeMockPay()
    app.dependency_overrides[get_mockpay] = lambda: fake
    yield fake
    app.dependency_overrides.pop(get_mockpay, None)
```
6. **`web/src/api/client.ts` and My bookings (task 9):** add `fare_paise: number` to your
   `Booking` type (and `fare_paise: int` to `BookingOut` in `schemas.py`). On each booking card,
   show `<PayButton pnr={b.pnr} farePaise={b.fare_paise} />` while it is `pending_payment`, and
   in task 13 `<RefundButton pnr={b.pnr} />` once it is `confirmed`. Both are named exports.

## Run it
- MockPay: `docker compose up --build -d` in `~/fspy-v3-kit/mockpay`; its dashboard is
  http://localhost:9090/dashboard.
- From `railseat/api`: `uv run fastapi dev app/main.py` and `uv run pytest -q`. The new tests
  show as skipped until you write them and delete the skip line.
- From `railseat/web`: `npm run dev`, `npm run build` and `npm test`.

## TODO map
| Task | File | What you write |
|---|---|---|
| 8 | `app/money.py`, `app/services/fares.py` | `parse_rupees`, `format_paise`, `split_paise`; `fare_for` |
| 8 | `app/services/order_states.py`, `docs/payments.md` | `ORDER_MOVES`, `PAYMENT_MOVES`, `move()`; both diagrams |
| 8 | `tests/test_money.py`, `tests/test_states.py` | 4 and 2 tests |
| 9 | `app/services/mockpay.py` | `MockPayClient.__init__`, `create_order` |
| 9 | `app/routers/payments.py`, `tests/fakes.py`, `tests/test_orders.py` | `create_payment_order`; `FakeMockPay.create_order`; 3 tests |
| 9 | `web/src/payments/money.ts`, `api.ts` | `formatPaise()`, `startCheckout()`; polling on My bookings (yours) |
| 10 | `app/services/mockpay.py`, `app/routers/payments.py` | `sign`, `signature_ok`; `mockpay_webhook` |
| 10 | `tests/test_webhook.py` | 3 tests |
| 11 | `app/services/idempotency.py` | `record_event`, `body_hash`, `claim_key`, `save_reply` |
| 11 | `app/routers/payments.py`, `web/src/payments/api.ts`, `tests/test_idempotency.py` | the key in the orders route and the webhook; one key per checkout; 3 tests |
| 12 | `app/services/ledger.py`, `app/routers/ledger.py` | `post`, `balances`, `import_settlement`; admin-only, `ledger`, `import_settlements` |
| 12 | `app/services/mockpay.py`, `app/routers/payments.py`, `tests/fakes.py`, `tests/test_ledger.py` | `settlement_report`; the capture posting; the fake report; 4 tests |
| 13 | `app/services/fares.py`, `app/services/mockpay.py`, `app/routers/payments.py` | `refund_split`; `refund`; `refund_booking`, and `refund.processed` in the webhook |
| 13 | `tests/fakes.py`, `tests/test_refund.py`, `web/src/payments/api.ts` | `FakeMockPay.refund`; 3 tests; `requestRefund()` |
| 14 | `tests/fakes.py` | `fail_next` in `FakeMockPay.create_order`, `signed_event()` |
| 14 | `tests/test_duplicates.py`, `test_late_events.py`, `test_timeouts.py`, `test_partial_refunds.py` | 2, 2, 1 and 2 tests |
| 15 | none | The wrap-up writes `railseat/README.md` and `EXPLAIN.md` only, so it has no TODO. |

## What you still write yourself
- Every TODO above, the models and migrations with their CHECK constraints, the new booking
  status `pending_payment` and `fare_paise` in `book_seat` (task 8).
- The polling with `refetchInterval` and "Payment pending" on My bookings (task 9).
- `evidence.md`, `AI_LOG.md`, `railseat/README.md` and `EXPLAIN.md`.
