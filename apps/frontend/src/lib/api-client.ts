import type {
  ApiResponse,
  Student,
  CreateStudentRequest,
  UpdateStudentRequest,
  StudentMetrics,
  StudentProgress,
  PerformanceDistribution,
  ActivityPerformance,
  StudentFilters,
  CacheConfig,
  SignupRequest,
  SignupResponse,
  LoginRequest,
  LoginResponse,
  AuthUser,
} from '@/types/api';
import type {
  Course,
  CourseMetrics,
  CourseProgressOverTime,
  StudentActivitySummary,
  CourseReportKPIs,
} from '@/types/course-report.interface';

// Legacy ApiError compatible type
interface LegacyApiError {
  success: boolean;
  message: string;
  code?: string;
}

/**
 * 🚀 API Client Type-Safe para Next.js 15
 * 
 * Características:
 * - ✅ Type Safety completo
 * - ✅ Cache configuration
 * - ✅ Error handling typed
 * - ✅ Request/Response validation
 * - ✅ Automatic revalidation
 */
export class APIClient {
  private baseURL: string;
  private defaultHeaders: Record<string, string>;
  private getToken?: () => string | Promise<string>;

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  /**
   * 🔧 Set a token getter function for dynamic auth
   * Useful for client-side components that need to read tokens
   */
  setTokenGetter(getToken: () => string | Promise<string>): void {
    this.getToken = getToken;
  }

  /**
   * 🔐 Set authentication token
   */
  setAuthToken(token: string): void {
    this.defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  /**
   * 🗑️ Clear authentication token
   */
  clearAuthToken(): void {
    delete this.defaultHeaders['Authorization'];
  }

  /**
   * 🌐 Generic GET request with type safety
   */
  async get<T>(
    endpoint: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any -- Query params can be any serializable value
    config?: CacheConfig & { params?: Record<string, any> }
  ): Promise<ApiResponse<T>> {
    // Support relative URLs for client-side proxy routes
    const isRelativeUrl = endpoint.startsWith("/api/");
    const origin = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000";
    const url = new URL(isRelativeUrl ? endpoint : `${this.baseURL}${endpoint}`, origin);

    // Add query parameters
    if (config?.params) {
      Object.entries(config.params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          url.searchParams.append(key, String(value));
        }
      });
    }

    // Build headers with dynamic token if getter is available
    const headers = { ...this.defaultHeaders };
    if (this.getToken) {
      const token = await this.getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    // For relative URLs, don't send Authorization header (cookie handles auth)
    if (isRelativeUrl) {
      delete headers['Authorization'];
    }

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers,
      ...config,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * 📤 Generic POST request with type safety
   */
  async post<T, R = T>(
    endpoint: string,
    data: T,
    config?: CacheConfig
  ): Promise<ApiResponse<R>> {
    const isRelativeUrl = endpoint.startsWith("/api/");
    const origin = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000";
    const url = new URL(isRelativeUrl ? endpoint : `${this.baseURL}${endpoint}`, origin);

    const headers = { ...this.defaultHeaders };
    if (this.getToken) {
      const token = await this.getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }
    if (isRelativeUrl) {
      delete headers['Authorization'];
    }

    const response = await fetch(url.toString(), {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
      ...config,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * ✏️ Generic PUT request with type safety
   */
  async put<T, R = T>(
    endpoint: string,
    data: T,
    config?: CacheConfig
  ): Promise<ApiResponse<R>> {
    const isRelativeUrl = endpoint.startsWith("/api/");
    const origin = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000";
    const url = new URL(isRelativeUrl ? endpoint : `${this.baseURL}${endpoint}`, origin);

    const headers = { ...this.defaultHeaders };
    if (this.getToken) {
      const token = await this.getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }
    if (isRelativeUrl) {
      delete headers['Authorization'];
    }

    const response = await fetch(url.toString(), {
      method: 'PUT',
      headers,
      body: JSON.stringify(data),
      ...config,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * 🗑️ Generic DELETE request
   */
  async delete(
    endpoint: string,
    config?: CacheConfig
  ): Promise<ApiResponse<void>> {
    const isRelativeUrl = endpoint.startsWith("/api/");
    const origin = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000";
    const url = new URL(isRelativeUrl ? endpoint : `${this.baseURL}${endpoint}`, origin);

    const headers = { ...this.defaultHeaders };
    if (this.getToken) {
      const token = await this.getToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }
    if (isRelativeUrl) {
      delete headers['Authorization'];
    }

    const response = await fetch(url.toString(), {
      method: 'DELETE',
      headers,
      ...config,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * 🚨 Handle API errors with type safety
   */
  private async handleError(response: Response): Promise<LegacyApiError> {
    let errorData: LegacyApiError;

    try {
      const body = await response.json();
      errorData = {
        success: false,
        message: body?.detail || body?.message || `HTTP ${response.status}: ${response.statusText}`,
        code: response.status.toString(),
      };
    } catch {
      errorData = {
        success: false,
        message: `HTTP ${response.status}: ${response.statusText}`,
        code: response.status.toString(),
      };
    }

    // eslint-disable-next-line no-console -- Log error for debugging API issues
    console.error('API Error:', {
      status: response.status,
      url: response.url,
      error: errorData,
    });

    return errorData;
  }
}

// 🎯 Singleton instance
export const apiClient = new APIClient();

/**
 * 📚 API Service functions with typed endpoints
 */
export class StudentService {
  // eslint-disable-next-line no-unused-vars
  constructor(private _client: APIClient) {}

  // 👥 Get all students with filters
  async getStudents(filters?: StudentFilters): Promise<ApiResponse<Student[]>> {
    return this._client.get('/students', { 
      params: filters,
      next: { revalidate: 300 }, // 5 minutes cache
    });
  }

  // 👤 Get single student
  async getStudent(id: string): Promise<ApiResponse<Student>> {
    return this._client.get(`/students/${id}`, {
      next: { revalidate: 60 }, // 1 minute cache
    });
  }

  // ➕ Create new student
  async createStudent(data: CreateStudentRequest): Promise<ApiResponse<Student>> {
    return this._client.post('/students', data, {
      next: { tags: ['students'] }, // Invalidate on revalidate
    });
  }

  // ✏️ Update student
  async updateStudent(id: string, data: UpdateStudentRequest): Promise<ApiResponse<Student>> {
    return this._client.put(`/students/${id}`, data, {
      next: { tags: ['students', `student-${id}`] },
    });
  }

  // 🗑️ Delete student
  async deleteStudent(id: string): Promise<ApiResponse<void>> {
    return this._client.delete(`/students/${id}`, {
      next: { tags: ['students'] },
    });
  }

  // 📊 Get student progress
  async getStudentProgress(id: string): Promise<ApiResponse<StudentProgress>> {
    return this._client.get(`/students/${id}/progress`, {
      next: { revalidate: 1800 }, // 30 minutes cache
    });
  }

  // 📈 Get student metrics
  async getStudentMetrics(): Promise<ApiResponse<StudentMetrics>> {
    return this._client.get('/metrics/students', {
      next: { revalidate: 900 }, // 15 minutes cache
    });
  }
}

export class ReportsService {
  // eslint-disable-next-line no-unused-vars
  constructor(private _client: APIClient) {}

  // 📊 Get performance distribution
  async getPerformanceDistribution(filters?: StudentFilters): Promise<ApiResponse<PerformanceDistribution[]>> {
    return this._client.get('/reports/performance', {
      params: filters,
      next: { revalidate: 3600 }, // 1 hour cache
    });
  }

  // 📈 Get activity performance
  async getActivityPerformance(filters?: StudentFilters): Promise<ApiResponse<ActivityPerformance[]>> {
    return this._client.get('/reports/activity', {
      params: filters,
      next: { revalidate: 3600 }, // 1 hour cache
    });
  }
}

export class CourseReportsService {
  constructor(private _client: APIClient) {}

  private getBaseUrl(): string {
    // On client side, use proxy route to forward auth cookie
    if (typeof window !== "undefined") {
      return "/api/courses";
    }
    // On server side, call backend directly
    return this._client["baseURL"] + "/api/v1/courses";
  }

  async getCourses(): Promise<ApiResponse<Course[]>> {
    const baseUrl = this.getBaseUrl();
    return this._client.get(baseUrl);
  }

  async getReportKPIs(): Promise<ApiResponse<CourseReportKPIs>> {
    const baseUrl = this.getBaseUrl();
    return this._client.get(`${baseUrl}/reports/kpis`);
  }

  async getCourseMetrics(
    courseIds: string[],
    options?: { signal?: AbortSignal },
  ): Promise<ApiResponse<CourseMetrics[]>> {
    const baseUrl = this.getBaseUrl();
    return this._client.get(`${baseUrl}/metrics`, {
      params: { course_ids: courseIds.join(",") },
      signal: options?.signal,
    });
  }

  async getProgressOverTime(
    courseId: string,
    options?: { signal?: AbortSignal },
  ): Promise<ApiResponse<CourseProgressOverTime[]>> {
    const baseUrl = this.getBaseUrl();
    return this._client.get(`${baseUrl}/${courseId}/progress-over-time`, {
      signal: options?.signal,
    });
  }

  async getActivitySummary(
    courseId: string,
    days = 30,
    options?: { signal?: AbortSignal },
  ): Promise<ApiResponse<StudentActivitySummary[]>> {
    const baseUrl = this.getBaseUrl();
    return this._client.get(`${baseUrl}/${courseId}/activity-summary`, {
      params: { days },
      signal: options?.signal,
    });
  }
}

/**
 * @deprecated desde 2026-03-19
 * 
 * ⚠️ **MIGRACIÓN REQUERIDA**
 * 
 * Esta clase ha sido reemplazada por el módulo `services/auth.ts`.
 * 
 * **Cambios necesarios:**
 * - `login()` → usar `login(params: LoginParams)` desde `@/services/auth`
 * - `getMe()` → usar `getMe(token: string)` desde `@/services/auth`
 * - `signup()` → usar `register(params: RegisterParams)` desde `@/services/auth`
 * 
 * **Ver también:** `lib/actions.ts` - acciones Server Actions refactorizadas
 * 
 * Esta clase se eliminará en la próxima versión mayor (v2.0).
 */
export class AuthService {
  // eslint-disable-next-line no-unused-vars
  constructor(private _client: APIClient) {}

  // 🔐 Login user
  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw error;
    }

    return response.json();
  }

  // 👤 Get current user profile
  async getMe(): Promise<ApiResponse<AuthUser>> {
    return this._client.get('/users/professors/me');
  }

  // 📝 Register new teacher
  async signup(data: SignupRequest): Promise<SignupResponse> {
    // Note: The backend returns the raw object, not wrapped in ApiResponse
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw error;
    }

    return response.json();
  }
}

// 🏭 Service instances
export const studentService = new StudentService(apiClient);
export const reportsService = new ReportsService(apiClient);
export const courseReportsService = new CourseReportsService(apiClient);

/**
 * @deprecated authService - usar funciones desde `@/services/auth` (login, register, getMe, logout, changePassword)
 */
export const authService = new AuthService(apiClient);