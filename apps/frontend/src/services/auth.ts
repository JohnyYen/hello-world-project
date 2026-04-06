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
  if (typeof window !== "undefined") {
    localStorage.removeItem("auth_token");
    document.cookie = "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
}

export const authService = {
  login,
  register,
  getMe,
  changePassword,
  logout,
};

export { login, register, getMe, changePassword, logout };
