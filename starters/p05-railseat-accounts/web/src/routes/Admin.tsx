// Admin page at /admin: every user with their role (P5 add-on, task 13).
// Only admins see it in the browser, and the API refuses everyone else anyway.
import type { AuthUser } from "../api/client";

type AdminUsers = { data: AuthUser[] | undefined; isPending: boolean; error: Error | null };

// A TanStack Query result has these three fields, so you can return useQuery(...) here.
function useAdminUsers(): AdminUsers {
  throw new Error("TODO(task 13): load GET /admin/users with useQuery and api()");
}

export default function Admin() {
  const { data, isPending, error } = useAdminUsers();

  if (isPending) return <p className="p-4">Loading users</p>;
  if (error)
    return (
      <p role="alert" className="p-4 text-red-700">
        {error.message}
      </p>
    );

  return (
    <main className="mx-auto max-w-3xl p-4">
      <h1 className="text-2xl font-bold">Users</h1>
      <table className="mt-4 w-full text-left">
        <thead>
          <tr>
            <th className="p-2">Email</th>
            <th className="p-2">Role</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((u) => (
            <tr key={u.id} className="border-t">
              <td className="p-2">{u.email}</td>
              <td className="p-2">{u.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
