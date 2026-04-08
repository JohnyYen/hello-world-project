import { lmsApi } from "@/api/client";
import type {
  LMSCredentialCreate,
  LMSCredentialResponse,
  SyncResultResponse,
} from "@/api/types";

export async function getLmsCredentials(token: string): Promise<LMSCredentialResponse[]> {
  const response = await lmsApi.getCredentials(token);
  return response.data ?? [];
}

export async function registerLmsCredentials(
  credentials: LMSCredentialCreate,
  token: string
): Promise<LMSCredentialResponse> {
  return lmsApi.registerCredential(credentials, token);
}

export async function syncLmsData(token: string): Promise<SyncResultResponse> {
  return lmsApi.syncLmsData(token);
}
