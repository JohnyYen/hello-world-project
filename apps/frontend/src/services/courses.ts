import { coursesApi } from "@/api/client";
import type {
  PaginatedCourseList,
  CourseDetail,
  CourseCreateRequest,
  CourseUpdateRequest,
  StudentEnrollment,
} from "@/types/course.interface";
import type { UserResponse } from "@/api/types";

export async function getCourses(
  token: string,
  skip = 0,
  limit = 100
): Promise<PaginatedCourseList> {
  return coursesApi.list(token, skip, limit);
}

export async function getCourse(
  courseId: string,
  token: string
): Promise<CourseDetail> {
  return coursesApi.getById(courseId, token);
}

export async function createCourse(
  body: CourseCreateRequest,
  token: string
): Promise<CourseDetail> {
  return coursesApi.create(body, token);
}

export async function updateCourse(
  courseId: string,
  body: CourseUpdateRequest,
  token: string
): Promise<CourseDetail> {
  return coursesApi.update(courseId, body, token);
}

export async function deleteCourse(
  courseId: string,
  token: string
): Promise<{ success: boolean }> {
  return coursesApi.delete(courseId, token);
}

export async function getCourseStudents(
  courseId: string,
  token: string
): Promise<StudentEnrollment[]> {
  return coursesApi.getStudents(courseId, token);
}

export async function enrollStudents(
  courseId: string,
  studentIds: string[],
  token: string
): Promise<StudentEnrollment[]> {
  return coursesApi.enrollStudents(courseId, { studentIds }, token);
}

export async function unenrollStudent(
  courseId: string,
  studentId: string,
  token: string
): Promise<{ success: boolean }> {
  return coursesApi.unenrollStudent(courseId, studentId, token);
}

export async function getUsersByRole(
  role: "student" | "professor",
  token: string
): Promise<UserResponse[]> {
  return coursesApi.listByRole(role, token);
}
