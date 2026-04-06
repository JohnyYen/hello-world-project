import { cookies } from 'next/headers';
import { Student } from "@/types";
import { getStudents as apiGetStudents, getStudent as apiGetStudent } from "@/services/users";

/**
 * Obtiene el token de autenticación desde las cookies del servidor.
 */
async function getAuthToken(): Promise<string | undefined> {
  const cookieStore = await cookies();
  return cookieStore.get("auth_token")?.value;
}

/**
 * Obtiene un estudiante por ID SIN cache.
 */
export async function getStudentById(id: string): Promise<Student | null> {
  try {
    const token = await getAuthToken();
    if (!token) return null;

    const response = await apiGetStudent(id, token);
    if (!response.data) return null;

    return {
      id: response.data.id,
      name: `${response.data.name} ${response.data.lastname || ''}`.trim(),
      email: response.data.email,
      maxLevel: 0,
      status: response.data.is_active ? 'active' : 'inactive',
      registrationDate: response.data.created_at ?? '',
      lastActivity: response.data.updated_at ?? '',
      completedLessons: 0,
      totalLessons: 0,
      progress: 0,
      achievements: [],
    };
  } catch {
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
