import { cookies, headers } from 'next/headers';
import { Student } from "@/types";
import { getStudents as apiGetStudents, getStudent as apiGetStudent } from "@/services/users";

/**
 * Obtiene el token de autenticación desde múltiples fuentes:
 * 1. Cookies del servidor (httpOnly)
 * 2. Authorization header
 */
async function getAuthToken(): Promise<string | undefined> {
  // Intentar desde cookies del servidor
  const cookieStore = await cookies();
  const cookieToken = cookieStore.get("auth_token")?.value;
  if (cookieToken) return cookieToken;

  // Intentar desde Authorization header
  const headersList = await headers();
  const authHeader = headersList.get('authorization');
  if (authHeader?.startsWith('Bearer ')) {
    return authHeader.substring(7);
  }

  return undefined;
}

/**
 * Calcula el estado del estudiante basado en last_activity:
 * - Pendiente (unregistered): nunca ha tenido actividad (last_activity = null)
 * - Inactivo (inactive): última actividad hace más de 14 días
 * - Activo (active): última actividad en los últimos 14 días
 */
function calculateStudentStatus(lastActivity: string | null): "active" | "inactive" | "unregistered" {
  if (!lastActivity) {
    return "unregistered";  // Pendiente - nunca ha jugado
  }

  const activityDate = new Date(lastActivity);
  const now = new Date();
  const twoWeeksInMs = 14 * 24 * 60 * 60 * 1000; // 14 días en milisegundos

  if (now.getTime() - activityDate.getTime() > twoWeeksInMs) {
    return "inactive";  // Inactivo - más de 2 semanas sin actividad
  }

  return "active";  // Activo - actividad en las últimas 2 semanas
}

/**
 * Obtiene un estudiante por ID SIN cache.
 */
export async function getStudentById(id: string): Promise<Student | null> {
  try {
    const token = await getAuthToken();
    if (!token) return null;

    const response = await apiGetStudent(id, token);
    
    // El backend puede devolver directamente el objeto o envuelto en ApiResponse
    // Convertir a unknown primero para evitar ошибки de tipo
    const studentData = ((response as unknown) as { data?: Record<string, unknown> })?.data || ((response as unknown) as Record<string, unknown>);

    if (!studentData || !studentData.id) return null;

    const lastActivity = studentData.last_activity as string | null;

    return {
      id: String(studentData.id),
      name: `${studentData.name || ''} ${studentData.lastname || ''}`.trim(),
      email: String(studentData.email || ''),
      maxLevel: 0,
      status: calculateStudentStatus(lastActivity),
      registrationDate: String(studentData.created_at || ''),
      lastActivity: lastActivity || String(studentData.updated_at || ''),
      completedLessons: 0,
      totalLessons: 0,
      progress: 0,
      achievements: [],
    };
  } catch (error) {
    console.error('Error fetching student by ID:', error);
    return null;
  }
}

/**
 * Obtiene todos los estudiantes SIN cache.
 */
export async function getAllStudents(schoolYear?: string): Promise<Student[]> {
  try {
    const token = await getAuthToken();
    if (!token) return [];

    const response = await apiGetStudents(token, 0, 100, schoolYear);
    return (response.data ?? []).map((s) => ({
      id: s.id,
      name: `${s.name} ${s.lastname || ''}`.trim(),
      email: s.email,
      maxLevel: 0,
      status: calculateStudentStatus(s.last_activity),
      registrationDate: s.created_at ?? '',
      lastActivity: s.last_activity ?? s.updated_at ?? '',
      completedLessons: 0,
      totalLessons: 0,
      progress: 0,
      achievements: [],
    }));
  } catch {
    return [];
  }
}

/**
 * Alias para compatibilidad.
 */
export async function getStudents(): Promise<Student[]> {
  return getAllStudents();
}

/**
 * Obtiene cursos escolares (años académicos) únicos del backend.
 * Ejemplo: "2025 a 2026"
 */
export async function getUniqueCourses(): Promise<string[]> {
  try {
    const token = await getAuthToken();
    if (!token) return [];

    // Llamar al endpoint /api/v1/users/students/courses
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8010'}/api/v1/users/students/courses`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      console.error('Error fetching courses:', response.status);
      return [];
    }

    const courses = await response.json();
    return courses as string[];
  } catch (error) {
    console.error('Error fetching courses:', error);
    return [];
  }
}
