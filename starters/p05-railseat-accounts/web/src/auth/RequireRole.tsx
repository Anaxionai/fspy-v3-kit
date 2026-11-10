// Shows a page only to the roles that may use it (P5 add-on, task 13).
// The API is still the real guard: this only decides what the browser shows.
import type { ReactNode } from "react";
import type { Role } from "../api/client";

type Props = { roles: Role[]; children: ReactNode };

// - No user (signed out): <Navigate to="/login" replace /> (from react-router).
// - A user whose role is not in `roles`: <Forbidden /> (src/routes/Forbidden.tsx).
// - Otherwise: the children.
// Get the user with useAuth() from ./AuthContext.
export function RequireRole({ roles, children }: Props): ReactNode {
  void roles; // these two lines only quiet TypeScript until you use the names; delete them
  void children;
  throw new Error("TODO(task 13): send signed-out users to /login, show <Forbidden /> for a wrong role, else the children");
}
