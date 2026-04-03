import type {
  StudentResponse,
  StudentListResponse,
} from '@workspace/api-client-ts';
import type { Student } from '@/types/student.interface';

function studentResponseToStudent(response: StudentResponse): Student {
  const fullName = [response.name, response.lastname]
    .filter(Boolean)
    .join(' ')
    .trim();

  const registrationDate = response.created_at
    ? new Date(response.created_at).toISOString()
    : new Date().toISOString();

  return {
    id: String(response.id),
    name: fullName || response.username,
    email: response.email,
    maxLevel: 0,
    status: response.is_active ? 'active' : 'inactive',
    registrationDate,
    lastActivity: response.updated_at
      ? new Date(response.updated_at).toISOString()
      : registrationDate,
    completedLessons: 0,
    totalLessons: 0,
    progress: 0,
    achievements: [],
    course: 'General',
  };
}

function studentListResponseToStudents(
  list: StudentListResponse
): Student[] {
  return list.data.map(studentResponseToStudent);
}

export {
  studentResponseToStudent,
  studentListResponseToStudents,
};

export type { StudentResponse, StudentListResponse };
