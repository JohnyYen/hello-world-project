import {
  Configuration,
  LMSCredentialsApi,
  LMSIntegrationApi,
  LMSCredentialCreate,
  LMSCredentialResponse,
  SyncResultResponse,
} from "@workspace/api-client-ts";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthToken(): Promise<string> {
  if (typeof window !== "undefined") {
    // Cliente: obtener token de localStorage (guardado por auth-context)
    const token = localStorage.getItem("auth_token");
    return token || "";
  } else {
    // Servidor: importar cookies dinámicamente
    const { cookies } = await import("next/headers");
    const cookieStore = await cookies();
    const token = cookieStore.get("auth_token");
    return token?.value || "";
  }
}

function createLmsApiConfiguration(): Configuration {
  return new Configuration({
    basePath: API_BASE_URL,
    accessToken: async () => {
      const token = await getAuthToken();
      return token;
    },
  });
}

function getLmsCredentialsApi(): LMSCredentialsApi {
  return new LMSCredentialsApi(createLmsApiConfiguration());
}

function getLmsIntegrationApi(): LMSIntegrationApi {
  return new LMSIntegrationApi(createLmsApiConfiguration());
}

async function getLmsCredentials(userId: number): Promise<LMSCredentialResponse> {
  const api = getLmsCredentialsApi();
  const response = await api.getUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdGet({ userId });
  return response;
}

async function registerLmsCredentials(credentials: LMSCredentialCreate): Promise<LMSCredentialResponse> {
  const api = getLmsCredentialsApi();
  const response = await api.registerLmsCredentialsApiV1UsersLmsCredentialsPost({ lMSCredentialCreate: credentials });
  return response;
}

async function deleteLmsCredentials(userId: number): Promise<void> {
  const api = getLmsCredentialsApi();
  await api.deleteUserLmsCredentialsApiV1UsersLmsCredentialsUserUserIdDelete({ userId });
}

async function syncLmsData(userId: number): Promise<SyncResultResponse> {
  const api = getLmsIntegrationApi();
  const response = await api.syncLmsDataApiV1UsersLmsSyncUserIdPost({ userId });
  return response;
}

export const lmsService = {
  getLmsCredentials,
  registerLmsCredentials,
  deleteLmsCredentials,
  syncLmsData,
};
