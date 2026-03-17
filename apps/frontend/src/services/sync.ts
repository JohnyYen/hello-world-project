import { cookies } from "next/headers";
import {
  Configuration,
  SyncApi,
  SyncSessionCreate,
  SyncSessionSchema,
  SyncEventCreate,
  SyncEventSchema,
} from "@workspace/api-client-ts";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthToken(): Promise<string> {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token");
  return token?.value || "";
}

function createSyncApiConfiguration(): Configuration {
  return new Configuration({
    basePath: API_BASE_URL,
    accessToken: async () => {
      const token = await getAuthToken();
      return token;
    },
  });
}

function getSyncApi(): SyncApi {
  return new SyncApi(createSyncApiConfiguration());
}

async function startSyncSession(params: SyncSessionCreate): Promise<SyncSessionSchema> {
  const api = getSyncApi();
  const response = await api.startSyncSessionApiV1SyncSyncSessionsPost({ syncSessionCreate: params });
  return response;
}

async function endSyncSession(sessionId: number): Promise<SyncSessionSchema> {
  const api = getSyncApi();
  const response = await api.endSyncSessionApiV1SyncSyncSessionsSessionIdEndPut({ sessionId });
  return response;
}

async function getSessionsByInstance(instanceId: number): Promise<Array<SyncSessionSchema>> {
  const api = getSyncApi();
  const response = await api.getSessionsByInstanceApiV1SyncSyncSessionsInstanceIdGet({ instanceId });
  return response;
}

async function registerSyncEvent(event: SyncEventCreate): Promise<SyncEventSchema> {
  const api = getSyncApi();
  const response = await api.registerSyncEventApiV1SyncSyncEventsPost({ syncEventCreate: event });
  return response;
}

async function listSyncEvents(sessionId: number): Promise<Array<SyncEventSchema>> {
  const api = getSyncApi();
  const response = await api.listSyncEventsApiV1SyncSyncEventsSessionIdGet({ sessionId });
  return response;
}

export const syncService = {
  startSyncSession,
  endSyncSession,
  getSessionsByInstance,
  registerSyncEvent,
  listSyncEvents,
};
