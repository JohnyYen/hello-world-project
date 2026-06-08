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
  averageGrade?: string;
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

export interface FeedbackHistoryItem {
  id: string;
  student_id: string;
  professor_id: string;
  comments: string;
  rating: number | null;
  feedback_type: "advice" | "hint" | "tip" | "message";
  display_in_game: boolean;
  acknowledged_at: string | null;
  created_at: string;
  updated_at: string | null;
}