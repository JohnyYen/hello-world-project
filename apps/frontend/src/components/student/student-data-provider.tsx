// Server component to fetch student data
import { notFound } from "next/navigation";
import { Student } from "@/types";

// Define the student type

// Mock data for students - in a real application, this would come from an API
const mockStudents: Record<string, Student> = {
  "1": {
    id: "1",
    name: "Juan Pérez",
    email: "juan.perez@email.com",
    maxLevel: 5,
    status: "active",
    registrationDate: "2024-01-15",
    lastActivity: "2024-10-28",
    completedLessons: 24,
    totalLessons: 40,
    progress: 60,
    achievements: ["Primeros Pasos", "Lógica Básica", "Bucles Aprendidos"]
  },
  "2": {
    id: "2",
    name: "María González",
    email: "maria.gonzalez@email.com",
    maxLevel: 8,
    status: "active",
    registrationDate: "2024-02-01",
    lastActivity: "2024-10-30",
    completedLessons: 35,
    totalLessons: 40,
    progress: 88,
    achievements: ["Racha de Oro", "Maestra de Condicionales", "Experta en Funciones"]
  },
  "3": {
    id: "3",
    name: "Carlos Rodríguez",
    email: "carlos.rodriguez@email.com",
    maxLevel: 3,
    status: "inactive",
    registrationDate: "2024-03-10",
    lastActivity: "2024-07-12",
    completedLessons: 12,
    totalLessons: 40,
    progress: 30,
    achievements: ["Primer Nivel"]
  },
  "4": {
    id: "4",
    name: "Ana López",
    email: "ana.lopez@email.com",
    maxLevel: 10,
    status: "active",
    registrationDate: "2024-01-22",
    lastActivity: "2024-10-29",
    completedLessons: 40,
    totalLessons: 40,
    progress: 100,
    achievements: ["Completado", "Racha de Plata", "Maestra de Programación"]
  },
  "5": {
    id: "5",
    name: "Luis Fernández",
    email: "luis.fernandez@email.com",
    maxLevel: 6,
    status: "unregistered",
    registrationDate: "2024-04-05",
    lastActivity: "2024-04-05",
    completedLessons: 0,
    totalLessons: 40,
    progress: 0,
    achievements: []
  }
};

// Mock data for the student list page (with course property)
export const mockStudentsList = [
  {
    id: "1",
    name: "Juan Pérez",
    email: "juan.perez@email.com",
    maxLevel: 5,
    status: "active",
    course: "2022-2025",
  },
  {
    id: "2",
    name: "María González",
    email: "maria.gonzalez@email.com",
    maxLevel: 8,
    status: "active",
    course: "2023-2026",
  },
  {
    id: "3",
    name: "Carlos Rodríguez",
    email: "carlos.rodriguez@email.com",
    maxLevel: 3,
    status: "inactive",
    course: "2021-2024",
  },
  {
    id: "4",
    name: "Ana López",
    email: "ana.lopez@email.com",
    maxLevel: 10,
    status: "active",
    course: "2023-2026",
  },
  {
    id: "5",
    name: "Luis Fernández",
    email: "luis.fernandez@email.com",
    maxLevel: 6,
    status: "unregistered",
    course: "2022-2025",
  },
  {
    id: "6",
    name: "Sofía Martínez",
    email: "sofia.martinez@email.com",
    maxLevel: 7,
    status: "active",
    course: "2023-2026",
  },
  {
    id: "7",
    name: "Pedro Sánchez",
    email: "pedro.sanchez@email.com",
    maxLevel: 4,
    status: "inactive",
    course: "2021-2024",
  },
  {
    id: "8",
    name: "Laura Ramírez",
    email: "laura.ramirez@email.com",
    maxLevel: 9,
    status: "active",
    course: "2023-2026",
  },
  {
    id: "9",
    name: "Miguel Torres",
    email: "miguel.torres@email.com",
    maxLevel: 2,
    status: "unregistered",
    course: "2022-2025",
  },
  {
    id: "10",
    name: "Elena Vásquez",
    email: "elena.vasquez@email.com",
    maxLevel: 11,
    status: "active",
    course: "2024-2027",
  },
  {
    id: "11",
    name: "Roberto Herrera",
    email: "roberto.herrera@email.com",
    maxLevel: 6,
    status: "active",
    course: "2023-2026",
  },
  {
    id: "12",
    name: "Carmen Castillo",
    email: "carmen.castillo@email.com",
    maxLevel: 8,
    status: "inactive",
    course: "2022-2025",
  },
];

export async function getStudent(id: string): Promise<Student | null> {
  // In a real application, this would be an API call to fetch data from a database
  // Simulating an async operation
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockStudents[id] as any || null;
}

export async function getAllStudents(): Promise<Student[]> {
  // In a real application, this would be an API call to fetch data from a database
  // Simulating an async operation
  await new Promise(resolve => setTimeout(resolve, 100));
  return Object.values(mockStudents) as any;
}

export async function getStudents(): Promise<(Student & { course: string })[]> {
  // In a real application, this would be an API call to fetch data from a database
  // Simulating an async operation
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockStudentsList as any;
}

export async function getUniqueCourses(): Promise<string[]> {
  const students = await getStudents();
  return Array.from(new Set(students.map(student => student.course))).sort().reverse();
}