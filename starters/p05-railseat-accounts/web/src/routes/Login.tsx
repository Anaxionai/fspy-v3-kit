// Login page (P5 add-on, task 9). The form is ready; logging in is yours.
import { useState, type FormEvent } from "react";
import { Link } from "react-router";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    // TODO(task 9): call login(email, password) from useAuth(), then navigate("/bookings")
    // with useNavigate(). On an ApiError with status 401, setError("Wrong email or password").
    throw new Error("TODO(task 9): log in through useAuth().login()");
  }

  return (
    <main className="mx-auto max-w-sm p-4">
      <h1 className="text-2xl font-bold">Log in</h1>
      <form onSubmit={onSubmit} className="mt-4 flex flex-col gap-3">
        <label className="flex flex-col gap-1">
          Email
          <input
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="rounded border p-2"
          />
        </label>
        <label className="flex flex-col gap-1">
          Password
          <input
            type="password"
            autoComplete="current-password"
            required
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
          Log in
        </button>
      </form>
      {/* TODO(task 10): add a "Forgot password?" link to /reset here. */}
      {/* TODO(task 15): add a "Sign in with Google" link: a plain <a> to http://localhost:8000/auth/google/login, not fetch. */}
      <p className="mt-4">
        New to RailSeat? <Link to="/signup">Create an account</Link>
      </p>
    </main>
  );
}
