import { unstable_cache } from 'next/cache';
import { Student } from "@/types";
import { getStudents as apiGetStudents, getStudent as apiGetStudent } from "@/services/users";
import { studentListResponseToStudents, studentResponseToStudent } from "@/adapters/student.adapter";

const cacheOptions = { 
  revalidate: process.env.NODE_ENV === 'production' ? 300 : 60,
  tags: ['students'] 
};

const getStudentCached = unstable_cache(
  async (id: string) => {
    try {
      const response = await apiGetStudent(parseInt(id, 10));
      return studentResponseToStudent(response);
    } catch {
      return null;
    }
  },
  ['student-detail'],
  cacheOptions
);

const getAllStudentsCached = unstable_cache(
  async () => {
    try {
      const response = await apiGetStudents();
      return studentListResponseToStudents(response);
    } catch {
      return [];
    }
  },
  ['all-students'],
  cacheOptions
);

const getStudentsListCached = unstable_cache(
  async () => {
    try {
      const response = await apiGetStudents();
      return studentListResponseToStudents(response);
    } catch {
      return [];
    }
  },
  ['students-list'],
  cacheOptions
);

export async function getStudent(id: string): Promise<Student | null> {
  return getStudentCached(id);
}

export async function getAllStudents(): Promise<Student[]> {
  return getAllStudentsCached();
}

export async function getStudents(): Promise<Student[]> {
  return getStudentsListCached();
}

export async function getUniqueCourses(): Promise<string[]> {
  const students = await getStudents();
  return Array.from(new Set(students.map(s => s.course).filter((c): c is string => Boolean(c)))).sort().reverse();
}
