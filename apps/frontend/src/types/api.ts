// 📋 Definición de tipos base para la API
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  pagination?: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface ApiError {
  success: false;
  message: string;
  errors?: Record<string, string[]>;
  code?: string;
}

// 🎓 Tipos específicos de Student
export interface Student {
  id: string;
  name: string;
  email: string;
  maxLevel: number;
  status: 'active' | 'inactive' | 'unregistered';
  course: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateStudentRequest {
  name: string;
  email: string;
  course: string;
  maxLevel?: number;
  status?: 'active' | 'inactive' | 'unregistered';
}

export interface UpdateStudentRequest {
  name?: string;
  email?: string;
  maxLevel?: number;
  status?: 'active' | 'inactive' | 'unregistered';
  course?: string;
}

// 📊 Tipos de Métricas
export interface StudentMetrics {
  totalStudents: number;
  activeStudents: number;
  inactiveStudents: number;
  averageLevel: number;
  completionRate: number;
  recentActivity: number;
}

export interface CourseMetrics {
  courseId: string;
  courseName: string;
  totalStudents: number;
  averageProgress: number;
  averageGrade: number;
}

export interface EngagementMetrics {
  dailyActiveUsers: number;
  weeklyActiveUsers: number;
  monthlyActiveUsers: number;
  averageSessionTime: number;
  bounceRate: number;
}

// 📈 Tipos de Reportes
export interface StudentProgress {
  studentId: string;
  courseName: string;
  currentLevel: number;
  maxLevel: number;
  completionPercentage: number;
  averageGrade: number;
  lastActivity: string;
}

export interface PerformanceDistribution {
  gradeRange: string;
  count: number;
  percentage: number;
}

export interface ActivityPerformance {
  activityId: string;
  activityName: string;
  averageScore: number;
  completionRate: number;
  averageTime: number;
  difficulty: 'easy' | 'medium' | 'hard';
}

// 🎯 Parámetros de Query
export interface PaginationParams {
  page?: number;
  limit?: number;
  search?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface StudentFilters extends PaginationParams {
  course?: string;
  status?: Student['status'];
  minLevel?: number;
  maxLevel?: number;
}

export interface DateRangeFilters {
  startDate?: string;
  endDate?: string;
}

// 📡 Endpoints Types
export type ApiEndpoint = 
  | `/students`
  | `/students/${string}`
  | `/students/${string}/progress`
  | `/metrics/students`
  | `/metrics/engagement`
  | `/reports/performance`
  | `/reports/activity`;

// 🔄 Cache y Revalidation Types
export interface CacheConfig {
  next: {
    revalidate?: number | false;
    tags?: string[];
  };
}

export type CacheDuration = 
  | 60        // 1 minuto
  | 300       // 5 minutos  
  | 900       // 15 minutos
  | 1800      // 30 minutos
  | 3600      // 1 hora
  | 86400     // 1 día
  | false;    // sin caché

// 🔐 Tipos de Autenticación
// Legacy types (snake_case) - mantienen compatibilidad con el API actual
export interface AuthTokens {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
}

// Legacy types para backward compatibility con componentes existentes
// NOTA: LoginResponse/SignupResponse usan snake_case (access_token, token_type)
// mientras api-client-ts usa camelCase (accessToken, tokenType, expiresIn).
// Mantenemos estas definiciones para no romper código existente.
export interface LoginRequest {
  username?: string;
  email?: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

export interface SignupRequest {
  username: string;
  email: string;
  name: string;
  lastname?: string;
  password: string;
}

export interface SignupResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: AuthUser;
}

export interface AuthUser {
  id: number;
  email: string;
  name: string;
  lastname?: string;
  username: string;
  role?: {
    id: number;
    name: string;
  };
}

// =============================================================================
// Type aliases para migración gradual hacia api-client-ts
// =============================================================================
// Estos aliases permiten usar tipos del api-client-ts manteniendo backward
// compatibility con código existente que importa desde types/api.ts
//
// Uso recomendado:
//   import { LoginRequest, SignupRequest } from "@/types/api";  // Legacy
//   import { UserLogin, UserCreate } from "@workspace/api-client-ts";  // Nuevo
//
// ⚠️  ALGUNOS ALIASES NO SON DIRECTAMENTE COMPATIBLES:
//   - LoginResponse/SignupResponse: campos snake_case vs camelCase del API
//   - AuthUser: tiene 'role' que TeacherProfileResponse no tiene
//   Usar con precaución en migraciones.
// =============================================================================

import type {
  UserLogin,
  UserCreate,
  UserLoginResponse,
  TeacherProfileResponse,
} from "@workspace/api-client-ts";

export type LoginRequestLegacy = LoginRequest;
export type LoginRequestNew = UserLogin;

export type SignupRequestLegacy = SignupRequest;
export type SignupRequestNew = UserCreate;

export type LoginResponseLegacy = LoginResponse;
export type LoginResponseNew = UserLoginResponse;

export type SignupResponseLegacy = SignupResponse;
export type SignupResponseNew = UserLoginResponse;

export type AuthUserLegacy = AuthUser;
export type AuthUserNew = TeacherProfileResponse;

export type { UserLogin, UserCreate, UserLoginResponse, TeacherProfileResponse };

// 📝 Form State Types
export interface FormState<T> {
  data: T;
  errors: Partial<Record<keyof T, string[]>>;
  isSubmitting: boolean;
  isDirty: boolean;
}

// 📊 Tipos para Gráficos de Reportes de Estudiante
export interface StudentReportKPIs {
  totalLevelsCompleted: number;
  totalGamesPlayed: number;
  totalPlayTime: number;
  averageScore: number;
  currentStreak: number;
  lastActivity: string | null;
}

export interface ProgressOverTime {
  date: string;
  level: number;
  score: number;
  timeSpent: number;
}

export interface LevelPerformance {
  levelName: string;
  score: number;
  attempts: number;
  timeSpent: number;
  completed: boolean;
}

export interface ActivityDistribution {
  gameName: string;
  timeSpent: number;
  sessions: number;
}