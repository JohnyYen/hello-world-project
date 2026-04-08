import { syncApi } from "@/api/client";
import type {
  SyncSessionSchema,
  SyncEventSchema,
  SyncSessionCreate,
  SyncEventCreate,
} from "@/api/types";

export async function startSyncSession(
  params: SyncSessionCreate,
  token: string
): Promise<SyncSessionSchema> {
  const response = await syncApi.startSession(params, token);
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

export async function endSyncSession(
  sessionId: string,
  token: string
): Promise<SyncSessionSchema> {
  const response = await syncApi.endSession(sessionId, token);
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

export async function getSessionsByInstance(
  instanceId: string,
  token: string
): Promise<SyncSessionSchema[]> {
  const response = await syncApi.getSessionsByInstance(instanceId, token);
  return response.data ?? [];
}

export async function registerSyncEvent(
  event: SyncEventCreate,
  token: string
): Promise<SyncEventSchema> {
  const response = await syncApi.registerEvent(event, token);
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

export async function listSyncEvents(
  sessionId: string,
  token: string
): Promise<SyncEventSchema[]> {
  const response = await syncApi.listEvents(sessionId, token);
  return response.data ?? [];
}
