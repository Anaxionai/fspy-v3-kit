// Password reset at /reset (P5 add-on, task 10). Two states:
// - /reset with no token: the email form, which asks for a link.
// - /reset?token=...: the new-password form, opened from the Mailpit link.
// Both forms are ready below; choosing between them and the API calls are yours.
import { useState, type FormEvent, type ReactNode } from "react";
import { Link, useSearchParams } from "react-router";
import { z } from "zod";

const emailSchema = z.string().trim().toLowerCase().email("Enter a valid email address");
const passwordSchema = z.string().min(10, "Use at least 10 characters");

export default function ResetPassword(): ReactNode {
  const [params] = useSearchParams();
  const token = params.get("token");
  void token; // only quiets TypeScript until you use the name; delete this line
  throw new Error("TODO(task 10): without a token show <EmailForm />, with one show <NewPasswordForm token={token} />");
}

async function sendResetLink(email: string): Promise<void> {
  void email; // only quiets TypeScript until you use the name; delete this line
  throw new Error("TODO(task 10): POST { email } to /auth/forgot with api()");
}

async function saveNewPassword(token: string, password: string): Promise<void> {
  void token; // these two lines only quiet TypeScript until you use the names; delete them
  void password;
  throw new Error("TODO(task 10): POST { token, password } to /auth/reset with api()");
}

export function EmailForm() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const result = emailSchema.safeParse(email);
    if (!result.success) {
      setError(result.error.issues[0].message);
      return;
    }
    setError(null);
    try {
      await sendResetLink(result.data);
      setSent(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Please try again.");
    }
  }

  if (sent) {
    return (
      <main className="mx-auto max-w-sm p-4">
        <h1 className="text-2xl font-bold">Check your email</h1>
        <p className="mt-2">If an account exists, we have emailed a reset link.</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-sm p-4">
      <h1 className="text-2xl font-bold">Forgot your password?</h1>
      <form onSubmit={onSubmit} noValidate className="mt-4 flex flex-col gap-3">
        <label className="flex flex-col gap-1">
          Email
          <input
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="rounded border p-2"
          />
        </label>
        {error && (
          <p role="alert" className="text-red-700">
            {error}
          </p>
        )}
        <button type="submit" className="rounded bg-blue-700 p-2 text-white focus-visible:ring-2">
          Email me a reset link
        </button>
      </form>
    </main>
  );
}

export function NewPasswordForm({ token }: { token: string }) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const result = passwordSchema.safeParse(password);
    if (!result.success) {
      setError(result.error.issues[0].message);
      return;
    }
    setError(null);
    try {
      await saveNewPassword(token, result.data);
      setDone(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "This link is invalid or has expired.");
    }
  }

  if (done) {
    return (
      <main className="mx-auto max-w-sm p-4">
        <h1 className="text-2xl font-bold">Password changed</h1>
        <p className="mt-2">
          <Link to="/login">Log in</Link> with your new password.
        </p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-sm p-4">
      <h1 className="text-2xl font-bold">Choose a new password</h1>
      <form onSubmit={onSubmit} noValidate className="mt-4 flex flex-col gap-3">
        <label className="flex flex-col gap-1">
          New password (10 or more characters)
          <input
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="rounded border p-2"
          />
        </label>
        {error && (
          <p role="alert" className="text-red-700">
            {error}
          </p>
        )}
        <button type="submit" className="rounded bg-blue-700 p-2 text-white focus-visible:ring-2">
          Save the new password
        </button>
      </form>
    </main>
  );
}
