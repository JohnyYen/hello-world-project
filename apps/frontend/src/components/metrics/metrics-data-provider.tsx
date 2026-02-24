// Metrics data provider with mock data

// Define types for our metrics data
export type MetricSummary = {
  totalStudents: number;
  activeStudents: number;
  avgCompletionRate: number;
  avgScore: number;
  totalCourses: number;
  activeCourses: number;
};

export type StudentProgress = {
  id: string;
  name: string;
  progress: number;
  score: number;
  lastActivity: string;
};

export type CourseCompletion = {
  courseId: string;
  courseName: string;
  completionRate: number;
  enrolled: number;
  completed: number;
};

export type DailyActivity = {
  date: string;
  activityCount: number;
  avgTimeSpent: number;
};

export type ActivityPerformance = {
  activityId: string;
  name: string;
  avgScore: number;
  completionRate: number;
  difficulty: number;
};

// Mock data for metrics
const mockMetricSummary: MetricSummary = {
  totalStudents: 1250,
  activeStudents: 980,
  avgCompletionRate: 75,
  avgScore: 82,
  totalCourses: 24,
  activeCourses: 18
};

const mockStudentProgress: StudentProgress[] = [
  { id: "1", name: "Juan Pérez", progress: 85, score: 88, lastActivity: "2024-10-28" },
  { id: "2", name: "María González", progress: 92, score: 94, lastActivity: "2024-10-30" },
  { id: "3", name: "Carlos Rodríguez", progress: 65, score: 70, lastActivity: "2024-10-25" },
  { id: "4", name: "Ana López", progress: 78, score: 82, lastActivity: "2024-10-29" },
  { id: "5", name: "Luis Fernández", progress: 45, score: 52, lastActivity: "2024-10-20" },
];

const mockCourseCompletion: CourseCompletion[] = [
  { courseId: "c1", courseName: "Introducción a la Programación", completionRate: 85, enrolled: 120, completed: 102 },
  { courseId: "c2", courseName: "Fundamentos de JavaScript", completionRate: 78, enrolled: 95, completed: 74 },
  { courseId: "c3", courseName: "Estructuras de Datos", completionRate: 65, enrolled: 80, completed: 52 },
  { courseId: "c4", courseName: "Algoritmos", completionRate: 58, enrolled: 75, completed: 44 },
  { courseId: "c5", courseName: "Programación Orientada a Objetos", completionRate: 72, enrolled: 88, completed: 63 },
];

const mockDailyActivity: DailyActivity[] = [
  { date: "2024-10-20", activityCount: 120, avgTimeSpent: 45 },
  { date: "2024-10-21", activityCount: 145, avgTimeSpent: 52 },
  { date: "2024-10-22", activityCount: 168, avgTimeSpent: 48 },
  { date: "2024-10-23", activityCount: 132, avgTimeSpent: 50 },
  { date: "2024-10-24", activityCount: 156, avgTimeSpent: 54 },
  { date: "2024-10-25", activityCount: 110, avgTimeSpent: 42 },
  { date: "2024-10-26", activityCount: 98, avgTimeSpent: 38 },
  { date: "2024-10-27", activityCount: 175, avgTimeSpent: 58 },
  { date: "2024-10-28", activityCount: 182, avgTimeSpent: 60 },
  { date: "2024-10-29", activityCount: 201, avgTimeSpent: 62 },
  { date: "2024-10-30", activityCount: 195, avgTimeSpent: 59 },
];

const mockActivityPerformance: ActivityPerformance[] = [
  { activityId: "a1", name: "Variables y Tipos", avgScore: 92, completionRate: 88, difficulty: 2 },
  { activityId: "a2", name: "Condicionales", avgScore: 85, completionRate: 82, difficulty: 3 },
  { activityId: "a3", name: "Bucles", avgScore: 78, completionRate: 75, difficulty: 4 },
  { activityId: "a4", name: "Funciones", avgScore: 72, completionRate: 68, difficulty: 6 },
  { activityId: "a5", name: "Arrays", avgScore: 68, completionRate: 65, difficulty: 5 },
  { activityId: "a6", name: "Objetos", avgScore: 65, completionRate: 62, difficulty: 6 },
  { activityId: "a7", name: "Clases", avgScore: 58, completionRate: 55, difficulty: 7 },
  { activityId: "a8", name: "Herencia", avgScore: 52, completionRate: 48, difficulty: 8 },
];

export async function getMetricSummary(): Promise<MetricSummary> {
  // In a real application, this would be an API call to fetch data from a database
  // Simulating an async operation
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockMetricSummary;
}

export async function getStudentProgress(limit: number = 5): Promise<StudentProgress[]> {
  await new Promise(resolve => setTimeout(resolve, 100));
  // Sort by progress in descending order and take the top N
  return [...mockStudentProgress].sort((a, b) => b.progress - a.progress).slice(0, limit);
}

export async function getCourseCompletion(): Promise<CourseCompletion[]> {
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockCourseCompletion;
}

export async function getDailyActivity(): Promise<DailyActivity[]> {
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockDailyActivity;
}

export async function getActivityPerformance(): Promise<ActivityPerformance[]> {
  await new Promise(resolve => setTimeout(resolve, 100));
  return mockActivityPerformance;
}