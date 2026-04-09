function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  }
  return process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

const API_BASE_URL = getApiBaseUrl();

async function getAuthToken(): Promise<string> {
  if (typeof window !== "undefined") {
    // Client-side: token is in HTTP-only cookie, not accessible from JS
    // Return empty string; calls should use Next.js API routes as proxy
    return "";
  } else {
    // Servidor: importar cookies dinámicamente
    const { cookies } = await import("next/headers");
    const cookieStore = await cookies();
    const token = cookieStore.get("auth_token");
    return token?.value || "";
  }
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAuthToken();
  
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Error ${response.status}: ${response.statusText}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// =====================
// Tipos para Métricas
// =====================

interface MetricType {
  id: string;
  name: string;
  code: string;
  description: string | null;
  created_at: string;
  updated_at: string | null;
}

interface MetricTypeCreate {
  name: string;
  code: string;
  description?: string;
}

interface MetricTypeUpdate {
  name?: string;
  code?: string;
  description?: string;
}

// =====================
// Funciones de Métricas
// =====================

interface GetMetricTypesParams {
  skip?: number;
  limit?: number;
}

async function getMetricTypes(params: GetMetricTypesParams = {}): Promise<Array<MetricType>> {
  const queryParams = new URLSearchParams();
  if (params.skip !== undefined) queryParams.set("skip", String(params.skip));
  if (params.limit !== undefined) queryParams.set("limit", String(params.limit));
  
  const query = queryParams.toString();
  return fetchApi<Array<MetricType>>(`/api/v1/statistic/metric-types${query ? `?${query}` : ""}`);
}

async function getMetricType(metricTypeId: string): Promise<MetricType> {
  return fetchApi<MetricType>(`/api/v1/statistic/metric-types/${metricTypeId}`);
}

async function createMetricType(metricType: MetricTypeCreate): Promise<MetricType> {
  return fetchApi<MetricType>("/api/v1/statistic/metric-types", {
    method: "POST",
    body: JSON.stringify(metricType),
  });
}

async function updateMetricType(metricTypeId: string, metricType: MetricTypeUpdate): Promise<MetricType> {
  return fetchApi<MetricType>(`/api/v1/statistic/metric-types/${metricTypeId}`, {
    method: "PATCH",
    body: JSON.stringify(metricType),
  });
}

async function deleteMetricType(metricTypeId: string): Promise<void> {
  return fetchApi<void>(`/api/v1/statistic/metric-types/${metricTypeId}`, {
    method: "DELETE",
  });
}

// =====================
// Funciones existentes (XAPI y Feedback)
// =====================

interface GetStatementsParams {
  skip?: number;
  limit?: number;
  studentId?: number;
  verbId?: string;
  gameId?: number;
  levelId?: number;
}

interface GetStudentFeedbackHistoryParams {
  skip?: number;
  limit?: number;
}

async function getStatements(params: GetStatementsParams = {}): Promise<unknown> {
  const queryParams = new URLSearchParams();
  if (params.skip !== undefined) queryParams.set("skip", String(params.skip));
  if (params.limit !== undefined) queryParams.set("limit", String(params.limit));
  if (params.studentId !== undefined) queryParams.set("student_id", String(params.studentId));
  if (params.verbId) queryParams.set("verb_id", params.verbId);
  if (params.gameId !== undefined) queryParams.set("game_id", String(params.gameId));
  if (params.levelId !== undefined) queryParams.set("level_id", String(params.levelId));
  
  const query = queryParams.toString();
  return fetchApi<unknown>(`/api/v1/statistic/xapi/statements${query ? `?${query}` : ""}`);
}

async function getStatement(statementId: string): Promise<unknown> {
  return fetchApi<unknown>(`/api/v1/statistic/xapi/statements/${statementId}`);
}

async function sendStatements(batch: unknown): Promise<unknown> {
  return fetchApi<unknown>("/api/v1/statistic/xapi/statements", {
    method: "POST",
    body: JSON.stringify(batch),
  });
}

async function submitFeedback(feedback: unknown): Promise<unknown> {
  return fetchApi<unknown>("/api/v1/statistic/feedback", {
    method: "POST",
    body: JSON.stringify(feedback),
  });
}

async function getStudentFeedbackHistory(studentId: number, params: GetStudentFeedbackHistoryParams = {}): Promise<unknown> {
  const queryParams = new URLSearchParams();
  if (params.skip !== undefined) queryParams.set("skip", String(params.skip));
  if (params.limit !== undefined) queryParams.set("limit", String(params.limit));
  
  const query = queryParams.toString();
  return fetchApi<unknown>(`/api/v1/statistic/feedback/${studentId}${query ? `?${query}` : ""}`);
}

export const statisticsService = {
  // Métricas (usa fetch directo)
  getMetricTypes,
  getMetricType,
  createMetricType,
  updateMetricType,
  deleteMetricType,
  
  // XAPI y Feedback (mantiene compatibilidad)
  getStatements,
  getStatement,
  sendStatements,
  submitFeedback,
  getStudentFeedbackHistory,
};

export type {
  MetricType,
  MetricTypeCreate,
  MetricTypeUpdate,
  GetMetricTypesParams,
  GetStatementsParams,
  GetStudentFeedbackHistoryParams,
};
