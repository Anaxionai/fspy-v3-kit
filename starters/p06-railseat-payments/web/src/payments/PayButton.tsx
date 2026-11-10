// The Pay button for a pending booking (P6 add-on, task 9, ready).
// It asks RailSeat for a MockPay order and opens MockPay's checkout page.
// Coming back to the site is not proof of payment: My bookings shows
// "Payment pending" until the webhook confirms the booking.
import { useState } from "react";
import { startCheckout } from "./api";
import { formatPaise } from "./money";

export function PayButton({ pnr, farePaise }: { pnr: string; farePaise: number }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onPay() {
    setBusy(true);
    setError(null);
    try {
      const reply = await startCheckout(pnr);
      window.location.assign(reply.checkout_url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "The payment could not start. Please try again.");
      setBusy(false);
    }
  }

  return (
    <div>
      <button
        type="button"
        onClick={onPay}
        disabled={busy}
        className="rounded bg-green-700 px-3 py-2 text-white focus-visible:ring-2"
      >
        Pay {formatPaise(farePaise)}
      </button>
      {error && (
        <p role="alert" className="mt-1 text-red-700">
          {error}
        </p>
      )}
    </div>
  );
}
