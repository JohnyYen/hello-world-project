/**
 * API type aliases for backward compatibility.
 * Re-exports types from the new manual type definitions.
 */

import type {
  UserLoginRequest,
  UserCreateRequest,
  UserLoginResponse,
  TeacherProfileResponse,
  StudentResponse,
  ApiResponse,
} from "@/api/types";

// Migration aliases
export type UserLogin = UserLoginRequest;
export type UserCreate = UserCreateRequest;
export type LoginRequestNew = UserLoginRequest;
export type SignupRequestNew = UserCreateRequest;
export type LoginResponseNew = UserLoginResponse;
export type SignupResponseNew = UserLoginResponse;
export type AuthUserNew = TeacherProfileResponse;

// Legacy aliases for lib/api-client.ts
export type LoginRequest = UserLoginRequest;
export type SignupRequest = UserCreateRequest;
export type LoginResponse = UserLoginResponse;
export type SignupResponse = UserLoginResponse;
export type AuthUser = TeacherProfileResponse;
export type { ApiResponse } from "@/api/types";
export type { ApiError } from "@/api/client";

// Student domain type (matches what the UI expects)
export interface Student {
  id: string;
  name: string;
  email: string;
  maxLevel: number;
  status: "active" | "inactive";
  registrationDate: string;
  lastActivity: string;
  completedLessons: number;
  totalLessons: number;
  progress: number;
  achievements: string[];
  course?: string;
}

export type CreateStudentRequest = {
  username: string;
  email: string;
  name: string;
  lastname: string;
  password: string;
  is_active?: boolean;
};

export type UpdateStudentRequest = Partial<CreateStudentRequest>;

export interface StudentMetrics {
  total: number;
  active: number;
  inactive: number;
  newThisWeek: number;
  newThisMonth: number;
}

export interface StudentProgress {
  studentId: string;
  levelsCompleted: number;
  totalPlayTime: number;
  averageScore: number;
  lastActivity: string;
}

export interface PerformanceDistribution {
  range: string;
  count: number;
}

export interface ActivityPerformance {
  activity: string;
  averageScore: number;
  participation: number;
}

export interface StudentFilters {
  search?: string;
  status?: "active" | "inactive";
  course?: string;
}

export interface CacheConfig {
  next?: {
    revalidate?: number;
    tags?: string[];
  };
}

// Re-export for direct access
export type {
  UserLoginRequest,
  UserCreateRequest,
  UserLoginResponse,
  TeacherProfileResponse,
};

// Re-export dashboard/report types
export type {
  OverviewKPIs,
  ActivityOverTimeItem,
  LevelPerformanceItem,
  OverviewTrends,
  StudentReportKPIs,
  ProgressOverTimeItem as ProgressOverTime,
  LevelPerformance,
  ActivityDistributionItem as ActivityDistribution,
} from "@/api/types";
