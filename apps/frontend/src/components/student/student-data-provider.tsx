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

    return {
      id: String(studentData.id),
      name: `${studentData.name || ''} ${studentData.lastname || ''}`.trim(),
      email: String(studentData.email || ''),
      maxLevel: 0,
      status: studentData.is_active ? 'active' : 'inactive',
      registrationDate: String(studentData.created_at || ''),
      lastActivity: String(studentData.updated_at || ''),
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
export async function getAllStudents(): Promise<Student[]> {
  try {
    const token = await getAuthToken();
    if (!token) return [];

    const response = await apiGetStudents(token);
    return (response.data ?? []).map((s) => ({
      id: s.id,
      name: `${s.name} ${s.lastname || ''}`.trim(),
      email: s.email,
      maxLevel: 0,
      status: s.is_active ? 'active' : 'inactive',
      registrationDate: s.created_at ?? '',
      lastActivity: s.updated_at ?? '',
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
 * Obtiene cursos únicos (placeholder - depende del modelo Student).
 */
export async function getUniqueCourses(): Promise<string[]> {
  const students = await getStudents();
  return Array.from(
    new Set(students.map(s => (s as any).course).filter((c): c is string => Boolean(c)))
  ).sort().reverse();
}
