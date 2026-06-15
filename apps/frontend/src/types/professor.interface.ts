export interface Professor {
  id: string;
  name: string;
  email: string;
  department: string;
  status: "active" | "inactive" | "on-leave";
  joinDate: string;
  specialization: string;
  courses: string[];
  officeLocation?: string;
  contactNumber?: string;
  profilePicture?: string;
}

export interface CreateProfessorDto {
  name: string;
  email: string;
  department: string;
  specialization: string;
  status?: "active" | "inactive" | "on-leave";
  courses?: string[];
  officeLocation?: string;
  contactNumber?: string;
}

export interface UpdateProfessorDto {
  name?: string;
  email?: string;
  department?: string;
  specialization?: string;
  status?: "active" | "inactive" | "on-leave";
  courses?: string[];
  officeLocation?: string;
  contactNumber?: string;
}

/**
 * Teacher profile data used in the account page.
 * Built from the API UserResponse / TeacherProfileResponse.
 */
export interface TeacherProfileData {
  id: string;
  fullName: string;
  email: string;
  username: string;
  avatarUrl: string | null;
  department: string;
  contactPhone: string | null;
  createdAt: string;
}

export interface AccountStats {
  activeCourses: number;
  totalStudents: number;
}