import {
  Configuration,
  UsersApi,
  UserListResponse,
  SingleUserResponse,
  UserCreate,
  StudentListResponse,
  StudentResponse,
  StudentCreate,
  StudentUpdate,
  StudentProgressResponse,
  StudentReportsResponse,
  TeacherProfileResponseSchema,
  TeacherProfileUpdate,
  TeacherUpdateResponseSchema,
  TeacherSettingsResponseSchema,
  TeacherSettingsUpdate,
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

function createUsersApiConfiguration(token?: string): Configuration {
  return new Configuration({
    basePath: API_BASE_URL,
    accessToken: token,
  });
}

async function getUsersApi(): Promise<UsersApi> {
  const token = await getAuthToken();
  return new UsersApi(createUsersApiConfiguration(token));
}

interface GetUsersParams {
  skip?: number;
  limit?: number;
  includeDeleted?: boolean;
}

export async function getUsers(params: GetUsersParams = {}): Promise<UserListResponse> {
  const api = await getUsersApi();
  const response = await api.getAllUsersApiV1UsersGet({
    skip: params.skip,
    limit: params.limit,
    includeDeleted: params.includeDeleted,
  });
  return response;
}

export async function getUser(userId: number): Promise<SingleUserResponse> {
  const api = await getUsersApi();
  const response = await api.getUserApiV1UsersUserIdGet({ userId });
  return response;
}

export async function createUser(userCreate: UserCreate): Promise<SingleUserResponse> {
  const api = await getUsersApi();
  const response = await api.createUserApiV1UsersPost({ userCreate });
  return response;
}

interface GetStudentsParams {
  skip?: number;
  limit?: number;
  search?: string;
}

export async function getStudents(params: GetStudentsParams = {}): Promise<StudentListResponse> {
  const api = await getUsersApi();
  const response = await api.listStudentsApiV1UsersStudentsGet({
    skip: params.skip,
    limit: params.limit,
    search: params.search,
  });
  return response;
}

export async function getStudent(id: number): Promise<StudentResponse> {
  const api = await getUsersApi();
  const response = await api.getStudentApiV1UsersStudentsIdGet({ id });
  return response;
}

export async function createStudent(studentCreate: StudentCreate): Promise<StudentResponse> {
  const api = await getUsersApi();
  const response = await api.createStudentApiV1UsersStudentsPost({ studentCreate });
  return response;
}

export async function updateStudent(id: number, studentUpdate: StudentUpdate): Promise<StudentResponse> {
  const api = await getUsersApi();
  const response = await api.updateStudentApiV1UsersStudentsIdPut({ id, studentUpdate });
  return response;
}

export async function deleteStudent(id: number): Promise<void> {
  const api = await getUsersApi();
  await api.deleteStudentApiV1UsersStudentsIdDelete({ id });
}

export async function getStudentProgress(id: number): Promise<StudentProgressResponse> {
  const api = await getUsersApi();
  const response = await api.getStudentProgressApiV1UsersStudentsIdProgressGet({ id });
  return response;
}

export async function getStudentReports(id: number): Promise<StudentReportsResponse> {
  const api = await getUsersApi();
  const response = await api.getStudentReportsApiV1UsersStudentsIdReportsGet({ id });
  return response;
}

export async function getTeacherProfile(): Promise<TeacherProfileResponseSchema["data"]> {
  const api = await getUsersApi();
  const response = await api.getTeacherProfileApiV1UsersProfessorsMeGet();
  return response.data;
}

export async function updateTeacherProfile(profile: TeacherProfileUpdate): Promise<TeacherUpdateResponseSchema> {
  const api = await getUsersApi();
  const response = await api.updateTeacherProfileApiV1UsersProfessorsMePut({ teacherProfileUpdate: profile });
  return response;
}

export async function getTeacherSettings(): Promise<TeacherSettingsResponseSchema["data"]> {
  const api = await getUsersApi();
  const response = await api.getTeacherSettingsApiV1UsersProfessorsSettingsGet();
  return response.data;
}

export async function updateTeacherSettings(settings: TeacherSettingsUpdate): Promise<TeacherSettingsResponseSchema> {
  const api = await getUsersApi();
  const response = await api.updateTeacherSettingsApiV1UsersProfessorsSettingsPut({ teacherSettingsUpdate: settings });
  return response;
}

export const usersService = {
  getUsers,
  getUser,
  createUser,
  getStudents,
  getStudent,
  createStudent,
  updateStudent,
  deleteStudent,
  getStudentProgress,
  getStudentReports,
  getTeacherProfile,
  updateTeacherProfile,
  getTeacherSettings,
  updateTeacherSettings,
};

export type {
  GetUsersParams,
  GetStudentsParams,
};
