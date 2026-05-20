export interface Course {
  id: string;
  name: string;
  description: string | null;
  schoolYear: string;
  periodLabel: string;
  startDate: string;
  endDate: string;
  isActive: boolean;
  studentCount: number;
  professorCount: number;
  createdAt: string | null;
  updatedAt: string | null;
}

export interface CourseDetail extends Course {
  students: StudentEnrollment[];
  professors: ProfessorAssignment[];
}

export interface StudentEnrollment {
  studentId: string;
  name: string;
  lastname: string | null;
  email: string;
  enrolledAt: string;
}

export interface ProfessorAssignment {
  professorId: string;
  name: string;
  email: string;
}

export interface CourseCreateRequest {
  name: string;
  description?: string;
  schoolYear: string;
  periodLabel: string;
  startDate: string;
  endDate: string;
  studentIds: string[];
  professorIds: string[];
}

export interface CourseUpdateRequest {
  name?: string;
  description?: string;
  schoolYear?: string;
  periodLabel?: string;
  startDate?: string;
  endDate?: string;
  studentIds?: string[];
  professorIds?: string[];
  isActive?: boolean;
}

export interface EnrollmentRequest {
  studentIds: string[];
}

export interface PaginatedCourseList {
  items: Course[];
  total: number;
  skip: number;
  limit: number;
}
