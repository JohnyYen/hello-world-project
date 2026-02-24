// Reports data provider with mock data
import { notFound } from "next/navigation";

// Define types for our reports data
export type Student = {
  id: string;
  name: string;
  course: string;
  averageGrade: number;
  performanceLevel: "alta" | "media" | "baja";
  completedLessons: number;
  totalLessons: number;
  progress: number;
  achievements: string[];
};

export type Activity = {
  id: string;
  name: string;
  difficulty: number; // 1-10 scale
  averageScore: number; // 0-100 percentage
  topic: string;
};

export type Topic = {
  id: string;
  name: string;
  averageScore: number; // 0-100 percentage
};

export type PerformanceIssue = {
  topic: string;
  percentage: number; // Percentage of students struggling (0-100)
};

// Mock data for students
const mockStudents: Student[] = [
  {
    id: "1",
    name: "Juan Pérez",
    course: "2024-2027",
    averageGrade: 85,
    performanceLevel: "alta",
    completedLessons: 35,
    totalLessons: 40,
    progress: 88,
    achievements: ["Racha de Oro", "Maestra de Condicionales", "Experta en Funciones"]
  },
  {
    id: "2",
    name: "María González",
    course: "2024-2027",
    averageGrade: 92,
    performanceLevel: "alta",
    completedLessons: 38,
    totalLessons: 40,
    progress: 95,
    achievements: ["Completado", "Racha de Plata", "Maestra de Programación"]
  },
  {
    id: "3",
    name: "Carlos Rodríguez",
    course: "2024-2027",
    averageGrade: 65,
    performanceLevel: "media",
    completedLessons: 25,
    totalLessons: 40,
    progress: 63,
    achievements: ["Primer Nivel"]
  },
  {
    id: "4",
    name: "Ana López",
    course: "2024-2027",
    averageGrade: 78,
    performanceLevel: "media",
    completedLessons: 32,
    totalLessons: 40,
    progress: 80,
    achievements: ["Lógica Básica"]
  },
  {
    id: "5",
    name: "Luis Fernández",
    course: "2024-2027",
    averageGrade: 45,
    performanceLevel: "baja",
    completedLessons: 15,
    totalLessons: 40,
    progress: 38,
    achievements: []
  },
  {
    id: "6",
    name: "Sofía Martínez",
    course: "2023-2026",
    averageGrade: 88,
    performanceLevel: "alta",
    completedLessons: 36,
    totalLessons: 40,
    progress: 90,
    achievements: ["Completado", "Racha de Plata"]
  },
  {
    id: "7",
    name: "Pedro Sánchez",
    course: "2023-2026",
    averageGrade: 55,
    performanceLevel: "baja",
    completedLessons: 18,
    totalLessons: 40,
    progress: 45,
    achievements: ["Primeros Pasos"]
  },
  {
    id: "8",
    name: "Laura Ramírez",
    course: "2023-2026",
    averageGrade: 72,
    performanceLevel: "media",
    completedLessons: 28,
    totalLessons: 40,
    progress: 70,
    achievements: ["Lógica Básica", "Bucles Aprendidos"]
  },
];

// Mock data for activities
const mockActivities: Activity[] = [
  {
    id: "act1",
    name: "Introducción a la Programación",
    difficulty: 2,
    averageScore: 92,
    topic: "Fundamentos"
  },
  {
    id: "act2",
    name: "Variables y Tipos de Datos",
    difficulty: 3,
    averageScore: 88,
    topic: "Fundamentos"
  },
  {
    id: "act3",
    name: "Condicionales",
    difficulty: 4,
    averageScore: 75,
    topic: "Estructuras de Control"
  },
  {
    id: "act4",
    name: "Bucles",
    difficulty: 5,
    averageScore: 68,
    topic: "Estructuras de Control"
  },
  {
    id: "act5",
    name: "Funciones",
    difficulty: 7,
    averageScore: 60,
    topic: "Funciones"
  },
  {
    id: "act6",
    name: "Manejo de Errores",
    difficulty: 8,
    averageScore: 55,
    topic: "Avanzado"
  },
  {
    id: "act7",
    name: "Algoritmos Recursivos",
    difficulty: 9,
    averageScore: 48,
    topic: "Avanzado"
  },
];

// Mock data for topics
const mockTopics: Topic[] = [
  { id: "t1", name: "Fundamentos", averageScore: 90 },
  { id: "t2", name: "Estructuras de Control", averageScore: 72 },
  { id: "t3", name: "Funciones", averageScore: 65 },
  { id: "t4", name: "POO", averageScore: 58 },
  { id: "t5", name: "Algoritmos", averageScore: 52 },
  { id: "t6", name: "Avanzado", averageScore: 51 },
];

// Mock data for performance issues
const mockPerformanceIssues: PerformanceIssue[] = [
  { topic: "Estructuras de Control", percentage: 35 },
  { topic: "Funciones", percentage: 42 },
  { topic: "POO", percentage: 58 },
  { topic: "Algoritmos", percentage: 65 },
  { topic: "Avanzado", percentage: 72 },
];

// All available courses
const allCourses = ["2024-2027", "2023-2026", "2022-2025", "2021-2024"];

export async function getStudentsForCourse(course: string): Promise<Student[]> {
  // In a real application, this would be an API call to fetch data from a database
  // Simulating an async operation
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockStudents.filter(student => student.course === course);
}

export async function getAverageGradeForCourse(course: string): Promise<number> {
  const students = await getStudentsForCourse(course);
  if (students.length === 0) return 0;
  
  const total = students.reduce((sum, student) => sum + student.averageGrade, 0);
  return Math.round(total / students.length);
}

export async function getPerformanceDistributionForCourse(course: string): Promise<{ alta: number; media: number; baja: number }> {
  const students = await getStudentsForCourse(course);
  
  const alta = students.filter(s => s.performanceLevel === "alta").length;
  const media = students.filter(s => s.performanceLevel === "media").length;
  const baja = students.filter(s => s.performanceLevel === "baja").length;
  
  return { alta, media, baja };
}

export async function getTopStudentsForCourse(course: string, limit: number = 5): Promise<Student[]> {
  const students = await getStudentsForCourse(course);
  return students
    .sort((a, b) => b.averageGrade - a.averageGrade)
    .slice(0, limit);
}

export async function getActivitiesForCourse(course: string): Promise<Activity[]> {
  // In a real application, this would return activities specific to the course
  // For now, we return the same activities for all courses
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockActivities;
}

export async function getHardestActivities(course: string): Promise<Activity[]> {
  const activities = await getActivitiesForCourse(course);
  return activities
    .sort((a, b) => b.difficulty - a.difficulty)
    .slice(0, 5); // Top 5 hardest activities
}

export async function getTopicsForCourse(course: string): Promise<Topic[]> {
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockTopics;
}

export async function getPerformanceIssuesForCourse(course: string): Promise<PerformanceIssue[]> {
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockPerformanceIssues;
}

export async function getAllCourses(): Promise<string[]> {
  await new Promise(resolve => setTimeout(resolve, 100));
  return allCourses.sort().reverse(); // Sort in descending order to get most recent first
}

export async function getMostRecentCourse(): Promise<string> {
  const courses = await getAllCourses();
  return courses[0] || "2024-2027"; // Default to 2024-2027 if no courses exist
}