"use client";

import { createContext, use, useState, useEffect, type ReactNode } from "react";
import type { TeacherProfileResponse, UserResponse } from "@/api/types";
import { authService, type LoginParams, type RegisterParams } from "@/services/auth";
import { SimpleUser } from "@/lib/auth-server";

// Union type to support SimpleUser (from server), TeacherProfileResponse, and UserResponse (from API login)
type User = SimpleUser | TeacherProfileResponse | UserResponse;

interface AuthContextValue {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (params: LoginParams) => Promise<void>;
  register: (params: RegisterParams) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

const TOKEN_KEY = "auth_token";

interface AuthProviderProps {
  children: ReactNode;
  initialUser?: User | null;
  initialToken?: string | null;
}

export function AuthProvider({ children, initialUser, initialToken }: AuthProviderProps) {
  // Si tenemos datos iniciales del servidor, confiar en ellos
  const hasServerData = initialUser !== null && initialToken !== null;

  const [user, setUser] = useState<User | null>(initialUser ?? null);
  const [token, setToken] = useState<string | null>(initialToken ?? null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Solo leer de localStorage si NO tenemos datos del servidor
    if (!hasServerData) {
      const storedToken = localStorage.getItem(TOKEN_KEY);
      // Verificar que el token sea válido (no null, undefined string, etc.)
      if (storedToken && storedToken !== "undefined" && storedToken !== "null") {
        setToken(storedToken);
      }
    }
  }, [hasServerData]);

  const login = async (_params: LoginParams) => {
    const response = await authService.login(_params);
    const { access_token: accessToken, user: userData } = response;

    localStorage.setItem(TOKEN_KEY, accessToken);
    setToken(accessToken);
    setUser(userData);
  };

  const register = async (_params: RegisterParams) => {
    const response = await authService.register(_params);
    const { access_token: accessToken, user: userData } = response;

    localStorage.setItem(TOKEN_KEY, accessToken);
    setToken(accessToken);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  };

  const value: AuthContextValue = {
    user,
    token,
    isAuthenticated: !!token && !!user,
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
