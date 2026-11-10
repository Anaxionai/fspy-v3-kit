// The signed-in user for the whole app (P5 add-on, task 9).
// The access token itself stays in src/api/client.ts, in memory only:
// nothing about the session goes into localStorage or sessionStorage.
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { AuthUser } from "../api/client";

type AuthState = {
  user: AuthUser | null;
  login: (email: string, password: string) => Promise<AuthUser>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO(task 9): restore the session after a reload: call refreshSession() once and
    // setUser() with the user it returns. If it fails, stay signed out. Then setLoading(false).
    // Until you write it, these two lines start signed out, so the app still loads:
    setUser(null);
    setLoading(false);
  }, []);

  async function login(email: string, password: string): Promise<AuthUser> {
    void email; // these two lines only quiet TypeScript until you use the names; delete them
    void password;
    throw new Error("TODO(task 9): POST /auth/login with api(), setAccessToken(), setUser(), return the user");
  }

  async function logout(): Promise<void> {
    throw new Error(
      "TODO(task 9): POST /auth/logout, setAccessToken(null), setUser(null) and queryClient.clear() (useQueryClient)",
    );
  }

  if (loading) return <p className="p-4">Loading</p>;

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const value = useContext(AuthContext);
  if (value === null) throw new Error("useAuth() must be used inside <AuthProvider>");
  return value;
}
