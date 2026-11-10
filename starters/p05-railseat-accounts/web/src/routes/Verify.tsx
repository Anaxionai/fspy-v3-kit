// Email verification page, opened from the Mailpit link /verify?token=... (P5 add-on, task 7).
// It posts the token only when the button is clicked, never in useEffect: React runs
// effects twice in development, and the second post would find the token already used.
import { useState } from "react";
import { Link, useSearchParams } from "react-router";

async function verifyToken(token: string): Promise<void> {
  void token; // only quiets TypeScript until you use the name; delete this line
  throw new Error("TODO(task 7): POST { token } to /auth/verify with api()");
}

export default function Verify() {
  const [params] = useSearchParams();
  const token = params.get("token");
  const [status, setStatus] = useState<"ready" | "busy" | "done" | "failed">("ready");

  async function onVerify() {
    if (!token) return;
    setStatus("busy");
    try {
      await verifyToken(token);
      setStatus("done");
    } catch {
      setStatus("failed");
    }
  }

  if (!token) {
    return (
      <main className="mx-auto max-w-sm p-4">
        <h1 className="text-2xl font-bold">Verify your email</h1>
        <p className="mt-2">This link has no token. Open the link from your email again.</p>
      </main>
    );
  }

  if (status === "done") {
    return (
      <main className="mx-auto max-w-sm p-4">
        <h1 className="text-2xl font-bold">Email verified</h1>
        <p className="mt-2">
          You can now <Link to="/login">log in</Link>.
        </p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-sm p-4">
      <h1 className="text-2xl font-bold">Verify your email</h1>
      {status === "failed" && (
        <p role="alert" className="mt-2 text-red-700">
          This link is invalid or has expired.
        </p>
      )}
      <button
        type="button"
        onClick={onVerify}
        disabled={status === "busy"}
        className="mt-4 rounded bg-blue-700 p-2 text-white focus-visible:ring-2"
      >
        Verify my email
      </button>
    </main>
  );
}
