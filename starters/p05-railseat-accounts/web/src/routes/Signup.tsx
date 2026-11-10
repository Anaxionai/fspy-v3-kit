// Sign-up page (P5 add-on, task 7). The form and its checks are ready; the API call is yours.
import { useState, type FormEvent } from "react";
import { Link } from "react-router";
import { z } from "zod";

const signupSchema = z.object({
  email: z.string().trim().toLowerCase().email("Enter a valid email address"),
  password: z.string().min(10, "Use at least 10 characters"),
});

type SignupForm = z.infer<typeof signupSchema>;

async function signUp(form: SignupForm): Promise<void> {
  void form; // only quiets TypeScript until you use the name; delete this line
  // A taken email gets 409 from the API: throw an error with a clear message for it.
  throw new Error("TODO(task 7): POST the form to /auth/signup with api()");
}

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const result = signupSchema.safeParse({ email, password });
    if (!result.success) {
      setError(result.error.issues[0].message);
      return;
    }
    setError(null);
    setBusy(true);
    try {
      await signUp(result.data);
      setDone(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign-up failed. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  if (done) {
    return (
      <main className="mx-auto max-w-sm p-4">
        <h1 className="text-2xl font-bold">Check your email</h1>
        <p className="mt-2">We sent a link to {email}. Open it to verify your account.</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-sm p-4">
      <h1 className="text-2xl font-bold">Create an account</h1>
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
        <label className="flex flex-col gap-1">
          Password (10 or more characters)
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
        <button type="submit" disabled={busy} className="rounded bg-blue-700 p-2 text-white focus-visible:ring-2">
          Create account
        </button>
      </form>
      <p className="mt-4">
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </main>
  );
}
