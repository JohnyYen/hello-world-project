"use client";

import { createContext, use, useState, useEffect, type ReactNode } from "react";
import type { TeacherProfileResponse, UserResponse } from "@/api/types";
import { authService, type LoginParams, type RegisterParams } from "@/services/auth";

// Union type to support SimpleUser (from server), TeacherProfileResponse, and UserResponse (from API login)
type User = TeacherProfileResponse | UserResponse | null;

interface AuthContextValue {
  user: User;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (params: LoginParams) => Promise<void>;
  register: (params: RegisterParams) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  // Token is managed via HTTP-only cookies, no client-side storage needed
  const [user, setUser] = useState<User>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch user profile on mount and when auth state changes
  useEffect(() => {
    let cancelled = false;

    const fetchUser = async () => {
      try {
        const userData = await authService.getMeFromCookie();
        if (!cancelled) {
          setUser(userData);
          setIsAuthenticated(!!userData);
        }
      } catch {
        // No valid session or profile fetch failed
        if (!cancelled) {
          setUser(null);
          setIsAuthenticated(false);
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    };

    fetchUser();

    return () => { cancelled = true };
  }, []);

  const login = async (params: LoginParams) => {
    await authService.login(params);
    // After login, cookie is set by server, fetch user profile
    const userData = await authService.getMeFromCookie();
    setUser(userData);
    setIsAuthenticated(true);
  };

  const register = async (params: RegisterParams) => {
    await authService.register(params);
    // After register, cookie is set by server, fetch user profile
    const userData = await authService.getMeFromCookie();
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logout = async () => {
    // Call Next.js API route to clear cookie server-side
    await fetch("/api/auth/logout", { method: "POST" });
    setUser(null);
    setIsAuthenticated(false);
  };

  const value: AuthContextValue = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext value={value}>{children}</AuthContext>;
}

export function useAuth(): AuthContextValue {
  const context = use(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
