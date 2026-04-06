import { revalidateTag } from 'next/cache';
import { Student } from "@/types";
import { getStudents as apiGetStudents, getStudent as apiGetStudent } from "@/services/users";
import { studentListResponseToStudents, studentResponseToStudent } from "@/adapters/student.adapter";

/**
 * Obtiene los estudiantes SIN cache.
 * Los datos de estudiantes dependen del token de autenticación del usuario,
 * por lo que cachear resultados sin considerar el contexto de auth会导致
 * que usuarios no autenticados pollute el cache con datos vacíos.
 */
export async function getStudent(id: string): Promise<Student | null> {
  try {
    const response = await apiGetStudent(parseInt(id, 10));
    return studentResponseToStudent(response);
  } catch {
    return null;
  }
}

export async function getAllStudents(): Promise<Student[]> {
  try {
    const response = await apiGetStudents();
    return studentListResponseToStudents(response);
  } catch {
    return [];
  }
}

export async function getStudents(): Promise<Student[]> {
  try {
    const response = await apiGetStudents();
    return studentListResponseToStudents(response);
  } catch (error) {
    console.error('Error fetching students:', error);
    return [];
  }
}

export async function getUniqueCourses(): Promise<string[]> {
  const students = await getStudents();
  return Array.from(new Set(students.map(s => s.course).filter((c): c is string => Boolean(c)))).sort().reverse();
}
