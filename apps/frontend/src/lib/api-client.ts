import { 
  ApiResponse, 
  ApiError, 
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
  AuthUser
} from '@/types/api';

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

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
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
    const url = new URL(`${this.baseURL}${endpoint}`);
    
    // Add query parameters
    if (config?.params) {
      Object.entries(config.params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          url.searchParams.append(key, String(value));
        }
      });
    }

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: this.defaultHeaders,
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
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: this.defaultHeaders,
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
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PUT',
      headers: this.defaultHeaders,
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
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'DELETE',
      headers: this.defaultHeaders,
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
  private async handleError(response: Response): Promise<ApiError> {
    let errorData: ApiError;
    
    try {
      errorData = await response.json();
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
export const authService = new AuthService(apiClient);