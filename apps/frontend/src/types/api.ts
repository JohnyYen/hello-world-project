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
export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'teacher' | 'student';
  permissions: string[];
}

// 📝 Form State Types
export interface FormState<T> {
  data: T;
  errors: Partial<Record<keyof T, string[]>>;
  isSubmitting: boolean;
  isDirty: boolean;
}