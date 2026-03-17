import { Configuration, AuthenticationApi, UserLogin, UserCreate, UserLoginResponse } from "@workspace/api-client-ts";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const authConfiguration = new Configuration({
  basePath: API_BASE_URL,
});

const authenticationApi = new AuthenticationApi(authConfiguration);

interface LoginParams {
  username?: string;
  email?: string;
  password: string;
}

interface RegisterParams {
  username: string;
  email: string;
  name: string;
  lastname?: string;
  password: string;
}

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

export const authService = {
  login,
  register,
};

export type { LoginParams, RegisterParams };
