// The Cancel and refund button for a paid booking (P6 add-on, task 13, ready).
// It shows the result, for example "Refunded ₹900.00 (fee ₹300.00)".
import { useState } from "react";
import { requestRefund, type RefundReply } from "./api";
import { formatPaise } from "./money";

export function RefundButton({ pnr, onDone }: { pnr: string; onDone?: () => void }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RefundReply | null>(null);

  async function onRefund() {
    if (!window.confirm("Cancel this booking? You get the fare back minus a 25% fee.")) return;
    setBusy(true);
    setError(null);
    try {
      setResult(await requestRefund(pnr));
      onDone?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "The refund failed. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  if (result) {
    return (
      <p role="status">
        Refunded {formatPaise(result.refund_paise)} (fee {formatPaise(result.fee_paise)})
      </p>
    );
  }

  return (
    <div>
      <button
        type="button"
        onClick={onRefund}
        disabled={busy}
        className="rounded border border-red-700 px-3 py-2 text-red-700 focus-visible:ring-2"
      >
        Cancel and refund
      </button>
      {error && (
        <p role="alert" className="mt-1 text-red-700">
          {error}
        </p>
      )}
    </div>
  );
}
