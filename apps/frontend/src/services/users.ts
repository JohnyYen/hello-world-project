import { cookies } from "next/headers";
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
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token");
  return token?.value || "";
}

function createUsersApiConfiguration(): Configuration {
  return new Configuration({
    basePath: API_BASE_URL,
    accessToken: async () => {
      const token = await getAuthToken();
      return token;
    },
  });
}

function getUsersApi(): UsersApi {
  return new UsersApi(createUsersApiConfiguration());
}

interface GetUsersParams {
  skip?: number;
  limit?: number;
  includeDeleted?: boolean;
}

async function getUsers(params: GetUsersParams = {}): Promise<UserListResponse> {
  const api = getUsersApi();
  const response = await api.getAllUsersApiV1UsersGet({
    skip: params.skip,
    limit: params.limit,
    includeDeleted: params.includeDeleted,
  });
  return response;
}

async function getUser(userId: number): Promise<SingleUserResponse> {
  const api = getUsersApi();
  const response = await api.getUserApiV1UsersUserIdGet({ userId });
  return response;
}

async function createUser(userCreate: UserCreate): Promise<SingleUserResponse> {
  const api = getUsersApi();
  const response = await api.createUserApiV1UsersPost({ userCreate });
  return response;
}

interface GetStudentsParams {
  skip?: number;
  limit?: number;
  search?: string;
}

async function getStudents(params: GetStudentsParams = {}): Promise<StudentListResponse> {
  const api = getUsersApi();
  const response = await api.listStudentsApiV1UsersStudentsGet({
    skip: params.skip,
    limit: params.limit,
    search: params.search,
  });
  return response;
}

async function getStudent(id: number): Promise<StudentResponse> {
  const api = getUsersApi();
  const response = await api.getStudentApiV1UsersStudentsIdGet({ id });
  return response;
}

async function createStudent(studentCreate: StudentCreate): Promise<StudentResponse> {
  const api = getUsersApi();
  const response = await api.createStudentApiV1UsersStudentsPost({ studentCreate });
  return response;
}

async function updateStudent(id: number, studentUpdate: StudentUpdate): Promise<StudentResponse> {
  const api = getUsersApi();
  const response = await api.updateStudentApiV1UsersStudentsIdPut({ id, studentUpdate });
  return response;
}

async function deleteStudent(id: number): Promise<void> {
  const api = getUsersApi();
  await api.deleteStudentApiV1UsersStudentsIdDelete({ id });
}

async function getStudentProgress(id: number): Promise<StudentProgressResponse> {
  const api = getUsersApi();
  const response = await api.getStudentProgressApiV1UsersStudentsIdProgressGet({ id });
  return response;
}

async function getStudentReports(id: number): Promise<StudentReportsResponse> {
  const api = getUsersApi();
  const response = await api.getStudentReportsApiV1UsersStudentsIdReportsGet({ id });
  return response;
}

async function getTeacherProfile(): Promise<TeacherProfileResponseSchema> {
  const api = getUsersApi();
  const response = await api.getTeacherProfileApiV1UsersProfessorsMeGet();
  return response;
}

async function updateTeacherProfile(profile: TeacherProfileUpdate): Promise<TeacherUpdateResponseSchema> {
  const api = getUsersApi();
  const response = await api.updateTeacherProfileApiV1UsersProfessorsMePut({ teacherProfileUpdate: profile });
  return response;
}

async function getTeacherSettings(): Promise<TeacherSettingsResponseSchema> {
  const api = getUsersApi();
  const response = await api.getTeacherSettingsApiV1UsersProfessorsSettingsGet();
  return response;
}

async function updateTeacherSettings(settings: TeacherSettingsUpdate): Promise<TeacherSettingsResponseSchema> {
  const api = getUsersApi();
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
