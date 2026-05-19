/**
 * API client using native fetch.
 */

const API_BASE_URL =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_API_URL || "http://localhost:8010"
    : process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://hwp-backend:8000";

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
    public response: Response
  ) {
    super(detail);
    this.name = "ApiError";
  }
}

async function request<T>(
  path: string,
  options: RequestInit & { token?: string } = {}
): Promise<T> {
  const { token, headers: extraHeaders, ...fetchOptions } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(extraHeaders as Record<string, string>),
  };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    let detail = `HTTP ${response.status}`;
    try {
      const body = await response.json();
      detail = body?.detail || body?.message || detail;
    } catch {
      // ignore
    }
    throw new ApiError(response.status, detail, response);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

// ─── Authentication ────────────────────────────────────────────────────────

export const authApi = {
  login: (body: { username?: string; email?: string; password: string }) =>
    request<import("./types").UserLoginResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  register: (body: { username: string; email: string; name: string; lastname?: string; password: string }) =>
    request<import("./types").UserLoginResponse>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  changePassword: (userId: string, body: { currentPassword: string; newPassword: string }, token: string) =>
    request<import("./types").SingleUserResponse>(
      `/api/v1/auth/change-password?user_id=${userId}`,
      { method: "POST", body: JSON.stringify(body), token }
    ),
};

// ─── Users / Professors ────────────────────────────────────────────────────

export const usersApi = {
  getTeacherProfile: (token: string) =>
    request<import("./types").ApiResponse<import("./types").TeacherProfileResponse>>(
      "/api/v1/users/professors/me",
      { token }
    ),

  updateTeacherProfile: (token: string, body: import("./types").TeacherProfileUpdate) =>
    request<import("./types").TeacherUpdateResponseSchema>(
      "/api/v1/users/professors/me",
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  getTeacherSettings: (token: string) =>
    request<import("./types").TeacherSettingsResponseSchema>(
      "/api/v1/users/professors/settings",
      { token }
    ),

  updateTeacherSettings: (token: string, body: import("./types").TeacherSettingsUpdate) =>
    request<import("./types").TeacherSettingsResponseSchema>(
      "/api/v1/users/professors/settings",
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  getUsers: (token: string, skip = 0, limit = 100) =>
    request<import("./types").UserListResponse>(
      `/api/v1/users?skip=${skip}&limit=${limit}`,
      { token }
    ),

  getUser: (userId: string, token: string) =>
    request<import("./types").SingleUserResponse>(
      `/api/v1/users/${userId}`,
      { token }
    ),

  createUser: (body: import("./types").UserCreateRequest, token: string) =>
    request<import("./types").SingleUserResponse>(
      "/api/v1/users",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  // Students
  getStudents: (token: string, skip = 0, limit = 100, schoolYear?: string) => {
    let url = `/api/v1/users/students?skip=${skip}&limit=${limit}`;
    if (schoolYear && schoolYear !== 'all') {
      url += `&school_year=${encodeURIComponent(schoolYear)}`;
    }
    return request<import("./types").StudentListResponse>(url, { token });
  },

  getStudent: (studentId: string, token: string) =>
    request<import("./types").ApiResponse<import("./types").StudentResponse>>(
      `/api/v1/users/students/${studentId}`,
      { token }
    ),

  createStudent: (body: import("./types").StudentCreate, token: string) =>
    request<import("./types").ApiResponse<import("./types").StudentResponse>>(
      "/api/v1/users/students",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  updateStudent: (studentId: string, body: import("./types").StudentUpdate, token: string) =>
    request<import("./types").ApiResponse<import("./types").StudentResponse>>(
      `/api/v1/users/students/${studentId}`,
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  getStudentProgress: (studentId: string, token: string) =>
    request<import("./types").StudentProgressResponse>(
      `/api/v1/users/students/${studentId}/progress`,
      { token }
    ),

  getStudentReports: (studentId: string, token: string) =>
    request<import("./types").StudentReportsResponse>(
      `/api/v1/users/students/${studentId}/reports`,
      { token }
    ),
};

// ─── Games & Levels ────────────────────────────────────────────────────────

export const gamesApi = {
  // Games
  getGames: (token: string) =>
    request<import("./types").GameListResponse>(
      "/api/v1/games",
      { token }
    ),

  getGame: (gameId: string, token: string) =>
    request<import("./types").SingleGameResponse>(
      `/api/v1/games/${gameId}`,
      { token }
    ),

  createGame: (body: import("./types").GameCreate, token: string) =>
    request<import("./types").GameCreateResponse>(
      "/api/v1/games",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  updateGame: (gameId: string, body: import("./types").GameUpdate, token: string) =>
    request<import("./types").GameUpdateResponse>(
      `/api/v1/games/${gameId}`,
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  deleteGame: (gameId: string, token: string) =>
    request<import("./types").GameDeleteResponse>(
      `/api/v1/games/${gameId}`,
      { method: "DELETE", token }
    ),

  // Levels
  getLevels: (token: string) =>
    request<import("./types").LevelListResponse>(
      "/api/v1/levels",
      { token }
    ),

  getLevel: (levelId: string, token: string) =>
    request<import("./types").SingleLevelResponse>(
      `/api/v1/levels/${levelId}`,
      { token }
    ),

  createLevel: (body: import("./types").LevelCreate, token: string) =>
    request<import("./types").LevelCreateResponse>(
      "/api/v1/levels",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  updateLevel: (levelId: string, body: import("./types").LevelUpdate, token: string) =>
    request<import("./types").LevelUpdateResponse>(
      `/api/v1/levels/${levelId}`,
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  deleteLevel: (levelId: string, token: string) =>
    request<import("./types").LevelDeleteResponse>(
      `/api/v1/levels/${levelId}`,
      { method: "DELETE", token }
    ),

  // Game Instances
  getGameInstances: (token: string) =>
    request<import("./types").GameInstanceListResponse>(
      "/api/v1/game-instances",
      { token }
    ),

  createGameInstance: (body: import("./types").GameInstanceCreate, token: string) =>
    request<import("./types").GameInstanceCreateResponse>(
      "/api/v1/game-instances",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  endGameInstance: (instanceId: string, body: import("./types").GameInstanceEnd, token: string) =>
    request<import("./types").GameInstanceEndResponse>(
      `/api/v1/game-instances/${instanceId}/end`,
      { method: "POST", body: JSON.stringify(body), token }
    ),

  // Segment Levels
  getSegmentLevels: (token: string) =>
    request<import("./types").SegmentLevelListResponse>(
      "/api/v1/segment-levels",
      { token }
    ),

  createSegmentLevel: (body: import("./types").SegmentLevelCreate, token: string) =>
    request<import("./types").SegmentLevelCreateResponse>(
      "/api/v1/segment-levels",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  updateSegmentLevel: (segmentLevelId: string, body: import("./types").SegmentLevelUpdate, token: string) =>
    request<import("./types").SegmentLevelUpdateResponse>(
      `/api/v1/segment-levels/${segmentLevelId}`,
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  deleteSegmentLevel: (segmentLevelId: string, token: string) =>
    request<import("./types").SegmentLevelDeleteResponse>(
      `/api/v1/segment-levels/${segmentLevelId}`,
      { method: "DELETE", token }
    ),
};

// ─── Course Management ─────────────────────────────────────────────────────

export const coursesApi = {
  list: (token: string, skip = 0, limit = 100) =>
    request<import("@/types/course.interface").PaginatedCourseList>(
      `/api/v1/courses/management?skip=${skip}&limit=${limit}`,
      { token }
    ),

  getById: (courseId: string, token: string) =>
    request<import("@/types/course.interface").CourseDetail>(
      `/api/v1/courses/${courseId}`,
      { token }
    ),

  create: (body: import("@/types/course.interface").CourseCreateRequest, token: string) =>
    request<import("@/types/course.interface").CourseDetail>(
      "/api/v1/courses/management",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  update: (courseId: string, body: import("@/types/course.interface").CourseUpdateRequest, token: string) =>
    request<import("@/types/course.interface").CourseDetail>(
      `/api/v1/courses/${courseId}`,
      { method: "PUT", body: JSON.stringify(body), token }
    ),

  delete: (courseId: string, token: string) =>
    request<{ success: boolean }>(
      `/api/v1/courses/${courseId}`,
      { method: "DELETE", token }
    ),

  getStudents: (courseId: string, token: string) =>
    request<import("@/types/course.interface").StudentEnrollment[]>(
      `/api/v1/courses/${courseId}/students`,
      { token }
    ),

  enrollStudents: (courseId: string, body: import("@/types/course.interface").EnrollmentRequest, token: string) =>
    request<import("@/types/course.interface").StudentEnrollment[]>(
      `/api/v1/courses/${courseId}/students`,
      { method: "POST", body: JSON.stringify(body), token }
    ),

  unenrollStudent: (courseId: string, studentId: string, token: string) =>
    request<{ success: boolean }>(
      `/api/v1/courses/${courseId}/students/${studentId}`,
      { method: "DELETE", token }
    ),

  listByRole: (role: "student" | "professor", token: string) =>
    request<import("./types").UserListResponse>(
      `/api/v1/users/by-role?role=${role}`,
      { token }
    ).then(res => res.data ?? []),
};

// ─── LMS ───────────────────────────────────────────────────────────────────

export const lmsApi = {
  getCredentials: (token: string) =>
    request<import("./types").LMSCredentialListResponse>(
      "/api/v1/lms/credentials",
      { token }
    ),

  registerCredential: (body: import("./types").LMSCredentialCreate, token: string) =>
    request<import("./types").LMSCredentialResponse>(
      "/api/v1/lms/credentials",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  syncLmsData: (token: string) =>
    request<import("./types").SyncResultResponse>(
      "/api/v1/lms/sync",
      { method: "POST", token }
    ),
};

// ─── Sync ──────────────────────────────────────────────────────────────────

export const syncApi = {
  startSession: (body: import("./types").SyncSessionCreate, token: string) =>
    request<import("./types").ApiResponse<import("./types").SyncSessionSchema>>(
      "/api/v1/sync/sessions",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  endSession: (sessionId: string, token: string) =>
    request<import("./types").ApiResponse<import("./types").SyncSessionSchema>>(
      `/api/v1/sync/sessions/${sessionId}`,
      { method: "DELETE", token }
    ),

  getSessionsByInstance: (instanceId: string, token: string) =>
    request<import("./types").SyncSessionListResponse>(
      `/api/v1/sync/sessions?instance_id=${instanceId}`,
      { token }
    ),

  registerEvent: (body: import("./types").SyncEventCreate, token: string) =>
    request<import("./types").ApiResponse<import("./types").SyncEventSchema>>(
      "/api/v1/sync/events",
      { method: "POST", body: JSON.stringify(body), token }
    ),

  listEvents: (sessionId: string, token: string) =>
    request<import("./types").SyncEventListResponse>(
      `/api/v1/sync/events?sync_session_id=${sessionId}`,
      { token }
    ),
};
