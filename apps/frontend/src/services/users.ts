import { usersApi } from "@/api/client";
import type {
  UserListResponse,
  SingleUserResponse,
  StudentListResponse,
  StudentResponse,
  StudentCreate,
  StudentUpdate,
  StudentProgressResponse,
  StudentReportsResponse,
  TeacherProfileResponse,
  TeacherProfileUpdate,
  TeacherSettingsResponse,
  TeacherSettingsUpdate,
} from "@/api/types";

export async function getUsers(token: string, skip = 0, limit = 100): Promise<UserListResponse> {
  return usersApi.getUsers(token, skip, limit);
}

export async function getUser(userId: string, token: string): Promise<SingleUserResponse> {
  return usersApi.getUser(userId, token);
}

export async function createUser(
  body: { username: string; email: string; name: string; lastname?: string; password: string },
  token: string
): Promise<SingleUserResponse> {
  return usersApi.createUser(body, token);
}

export async function getStudents(
  token: string,
  skip = 0,
  limit = 100,
  schoolYear?: string
): Promise<StudentListResponse> {
  return usersApi.getStudents(token, skip, limit, schoolYear);
}

export async function getStudent(
  studentId: string,
  token: string
): Promise<import("@/api/types").ApiResponse<StudentResponse>> {
  return usersApi.getStudent(studentId, token);
}

export async function createStudent(
  body: StudentCreate,
  token: string
): Promise<import("@/api/types").ApiResponse<StudentResponse>> {
  return usersApi.createStudent(body, token);
}

export async function updateStudent(
  studentId: string,
  body: StudentUpdate,
  token: string
): Promise<import("@/api/types").ApiResponse<StudentResponse>> {
  return usersApi.updateStudent(studentId, body, token);
}

export async function getStudentProgress(
  studentId: string,
  token: string
): Promise<StudentProgressResponse> {
  return usersApi.getStudentProgress(studentId, token);
}

export async function getStudentReports(
  studentId: string,
  token: string
): Promise<StudentReportsResponse> {
  return usersApi.getStudentReports(studentId, token);
}

export async function getTeacherProfile(token: string): Promise<TeacherProfileResponse> {
  const response = await usersApi.getTeacherProfile(token);
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

export async function updateTeacherProfile(
  token: string,
  body: TeacherProfileUpdate
): Promise<TeacherProfileResponse> {
  const response = await usersApi.updateTeacherProfile(token, body);
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

export async function getTeacherSettings(token: string): Promise<TeacherSettingsResponse> {
  const response = await usersApi.getTeacherSettings(token);
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}

export async function updateTeacherSettings(
  token: string,
  body: TeacherSettingsUpdate
): Promise<TeacherSettingsResponse> {
  const response = await usersApi.updateTeacherSettings(token, body);
  if (!response.data) {
    throw new Error("No data in response");
  }
  return response.data;
}
