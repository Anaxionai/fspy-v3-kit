// Calls to RailSeat's payment routes (P6 add-on). Use api() from ../api/client,
// and check that your api() keeps the headers you pass in `init`.
// No amount is ever sent: the API takes it from the booking's fare.

export type OrderReply = { order_id: number; checkout_url: string };
export type RefundReply = { pnr: string; refund_paise: number; fee_paise: number; payment_status: string };

// POST /payments/orders with { pnr }.
// TODO(task 11): send an `Idempotency-Key` header: one key per checkout, made with
// crypto.randomUUID() and reused when Pay is clicked again for the same PNR
// (keep the keys in a Map). Add "Idempotency-Key" to the API's CORS allow_headers.
export async function startCheckout(pnr: string): Promise<OrderReply> {
  void pnr; // only quiets TypeScript until you use the name; delete this line
  throw new Error("TODO(task 9): POST { pnr } to /payments/orders with api()");
}

// POST /bookings/{pnr}/refund with an `Idempotency-Key` header, reused on a retry.
export async function requestRefund(pnr: string): Promise<RefundReply> {
  void pnr; // only quiets TypeScript until you use the name; delete this line
  throw new Error("TODO(task 13): POST to /bookings/{pnr}/refund with api() and an Idempotency-Key");
}
