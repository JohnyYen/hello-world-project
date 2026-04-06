import { Configuration, AuthenticationApi, UsersApi, UserLogin, UserCreate, UserLoginResponse, TeacherProfileResponse, UserChangePassword, SingleUserResponse } from "@workspace/api-client-ts";

function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    // Client-side: use public URL (browser accessible)
    return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  }
  // Server-side: use internal Docker URL
  return process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

const API_BASE_URL = getApiBaseUrl();

const createConfig = (token?: string) =>
  new Configuration({
    basePath: API_BASE_URL,
    accessToken: token,
  });

const authenticationApi = new AuthenticationApi(createConfig());
const usersApi = new UsersApi(createConfig());

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

export type UserProfileResponse = TeacherProfileResponse;

async function login(params: LoginParams): Promise<UserLoginResponse> {
  const userLogin: UserLogin = {
    username: params.username,
    email: params.email,
    password: params.password,
  };

  const response = await authenticationApi.loginForAccessTokenApiV1AuthLoginPost({
    userLogin,
  });

  return response;
}

async function register(params: RegisterParams): Promise<UserLoginResponse> {
  const userCreate: UserCreate = {
    username: params.username,
    email: params.email,
    name: params.name,
    lastname: params.lastname,
    password: params.password,
  };

  const response = await authenticationApi.registerUserApiV1AuthRegisterPost({
    userCreate,
  });

  return response;
}

async function getMe(token?: string): Promise<TeacherProfileResponse> {
  const api = token ? new UsersApi(createConfig(token)) : usersApi;
  const response = await api.getTeacherProfileApiV1UsersProfessorsMeGet();
  return response.data;
}

async function changePassword(
  userId: number,
  currentPassword: string,
  newPassword: string,
  token: string
): Promise<SingleUserResponse> {
  const api = new AuthenticationApi(createConfig(token));
  const userChangePassword: UserChangePassword = {
    currentPassword,
    newPassword,
  };

  return api.changePasswordApiV1AuthChangePasswordPost({
    userId,
    userChangePassword,
  });
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
