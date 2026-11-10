// Shown when a signed-in user opens a page their role may not use (P5 add-on, task 13, ready).
import { Link } from "react-router";

export default function Forbidden() {
  return (
    <main className="mx-auto max-w-3xl p-4">
      <h1 className="text-2xl font-bold">You do not have access to this page</h1>
      <p className="mt-2">Your account cannot open this page. If you think it should, ask an admin.</p>
      <p className="mt-4">
        <Link to="/">Back to search</Link>
      </p>
    </main>
  );
}
