export interface Student {
  id: string;
  name: string;
  email: string;
  maxLevel: number;
  status: "active" | "inactive" | "unregistered";
  registrationDate: string;
  lastActivity: string;
  completedLessons: number;
  totalLessons: number;
  progress: number;
  achievements: string[];
  course?: string;
}

export interface CreateStudentDto {
  name: string;
  email: string;
  maxLevel: number;
  status?: "active" | "inactive" | "unregistered";
  course?: string;
}

export interface UpdateStudentDto {
  name?: string;
  email?: string;
  maxLevel?: number;
  status?: "active" | "inactive" | "unregistered";
  course?: string;
}