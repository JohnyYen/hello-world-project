import type { StudentResponse, StudentListResponse } from '@/api/types';

/**
 * Adapter to convert API responses to domain models.
 */

export function studentResponseToStudent(response: StudentResponse) {
  return {
    id: response.id,
    username: response.username,
    email: response.email,
    name: response.name,
    lastname: response.lastname,
    isActive: response.is_active,
    createdAt: response.created_at,
    updatedAt: response.updated_at,
  };
}

export function studentListResponseToStudents(response: StudentListResponse) {
  return (response.data ?? []).map(studentResponseToStudent);
}

// Re-export types for convenience
export type { StudentResponse, StudentListResponse };
