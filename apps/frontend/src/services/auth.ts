import { authApi } from "@/api/client";
import type {
  UserLoginResponse,
  TeacherProfileResponse,
  UserResponse,
  UserLoginRequest,
  UserCreateRequest,
  UserChangePasswordRequest,
} from "@/api/types";

export interface LoginParams {
  username?: string;
  email?: string;
  password: string;
}

export interface RegisterParams {
  username: string;
  email: string;
  name: string;
  lastname?: string;
  password: string;
}

export type UserProfileResponse = TeacherProfileResponse | UserResponse;

async function login(params: LoginParams): Promise<UserLoginResponse> {
  return authApi.login({
    username: params.username,
    email: params.email,
    password: params.password,
  });
}

async function register(params: RegisterParams): Promise<UserLoginResponse> {
  return authApi.register({
    username: params.username,
    email: params.email,
    name: params.name,
    lastname: params.lastname,
    password: params.password,
  });
}

async function getMe(token?: string): Promise<UserProfileResponse> {
  if (!token) {
    throw new Error("No token provided");
  }
  const response = await import("@/api/client").then((m) =>
    m.usersApi.getTeacherProfile(token)
  );
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

async function changePassword(
  userId: string,
  currentPassword: string,
  newPassword: string,
  token: string
): Promise<UserProfileResponse> {
  const response = await authApi.changePassword(
    userId,
    { currentPassword, newPassword },
    token
  );
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

async function logout(): Promise<void> {
  // Cookie is cleared server-side via logoutAction
  // This function is kept for API consistency
}

/**
 * Fetches user profile using cookie-based authentication.
 * Used by AuthProvider to check session on mount (client-side).
 * Calls Next.js API route which reads the HTTP-only cookie server-side.
 */
async function getMeFromCookie(): Promise<UserProfileResponse | null> {
  if (typeof window === "undefined") {
    // Server-side: use getServerUser
    const { getServerUser } = await import("@/lib/auth-server");
    const { user } = await getServerUser();
    return user as UserProfileResponse | null;
  }

  // Client-side: call Next.js API route (same-origin, cookies sent automatically)
  const response = await fetch("/api/auth/me", {
    cache: "no-store",
  });

  if (!response.ok) {
    return null;
  }

  const data = await response.json();
  return data.user || null;
}

export const authService = {
  login,
  register,
  getMe,
  getMeFromCookie,
  changePassword,
  logout,
};

export { login, register, getMe, getMeFromCookie, changePassword, logout };
