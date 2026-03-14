/**
 * 📊 Servicio de Datos para Reportes de Curso
 * Proporciona datos mock para el dashboard de reportes
 */

import type {
  Course,
  CourseMetrics,
  CourseProgressOverTime,
  StudentActivitySummary,
  CourseReportKPIs,
  ReportFilters,
} from '@/types/course-report.interface';

// Cursos disponibles
const courses: Course[] = [
  {
    id: 'course-1',
    name: 'Matemáticas I',
    period: '2026 - Primer Semestre',
    startDate: '2026-01-15',
    endDate: '2026-06-15',
    totalStudents: 45,
  },
  {
    id: 'course-2',
    name: 'Física Fundamental',
    period: '2026 - Primer Semestre',
    startDate: '2026-01-15',
    endDate: '2026-06-15',
    totalStudents: 32,
  },
  {
    id: 'course-3',
    name: 'Química General',
    period: '2026 - Primer Semestre',
    startDate: '2026-01-15',
    endDate: '2026-06-15',
    totalStudents: 28,
  },
  {
    id: 'course-4',
    name: 'Biología Celular',
    period: '2025 - Segundo Semestre',
    startDate: '2025-08-15',
    endDate: '2025-12-15',
    totalStudents: 38,
  },
  {
    id: 'course-5',
    name: 'Introducción a la Programación',
    period: '2025 - Segundo Semestre',
    startDate: '2025-08-15',
    endDate: '2025-12-15',
    totalStudents: 52,
  },
];

// Métricas de cada curso
const courseMetricsData: CourseMetrics[] = [
  {
    courseId: 'course-1',
    courseName: 'Matemáticas I',
    period: '2026 - Primer Semestre',
    averageProgress: 72,
    averageGrade: 78,
    completionRate: 65,
    studentsCompleted: 29,
    averageActiveTime: 145,
    dailyActiveUsers: 38,
    weeklyActiveUsers: 42,
    averageSessionsPerStudent: 12,
    highPerformers: 18,
    mediumPerformers: 20,
    lowPerformers: 7,
    progressTrend: 5.2,
    gradeTrend: 3.1,
    engagementTrend: -2.4,
  },
  {
    courseId: 'course-2',
    courseName: 'Física Fundamental',
    period: '2026 - Primer Semestre',
    averageProgress: 58,
    averageGrade: 71,
    completionRate: 50,
    studentsCompleted: 16,
    averageActiveTime: 98,
    dailyActiveUsers: 24,
    weeklyActiveUsers: 28,
    averageSessionsPerStudent: 8,
    highPerformers: 10,
    mediumPerformers: 14,
    lowPerformers: 8,
    progressTrend: -1.8,
    gradeTrend: 1.2,
    engagementTrend: -5.6,
  },
  {
    courseId: 'course-3',
    courseName: 'Química General',
    period: '2026 - Primer Semestre',
    averageProgress: 81,
    averageGrade: 84,
    completionRate: 75,
    studentsCompleted: 21,
    averageActiveTime: 167,
    dailyActiveUsers: 25,
    weeklyActiveUsers: 27,
    averageSessionsPerStudent: 15,
    highPerformers: 15,
    mediumPerformers: 10,
    lowPerformers: 3,
    progressTrend: 8.4,
    gradeTrend: 6.2,
    engagementTrend: 12.3,
  },
  {
    courseId: 'course-4',
    courseName: 'Biología Celular',
    period: '2025 - Segundo Semestre',
    averageProgress: 89,
    averageGrade: 82,
    completionRate: 82,
    studentsCompleted: 31,
    averageActiveTime: 156,
    dailyActiveUsers: 34,
    weeklyActiveUsers: 36,
    averageSessionsPerStudent: 14,
    highPerformers: 20,
    mediumPerformers: 12,
    lowPerformers: 6,
    progressTrend: 4.1,
    gradeTrend: 2.8,
    engagementTrend: 1.2,
  },
  {
    courseId: 'course-5',
    courseName: 'Introducción a la Programación',
    period: '2025 - Segundo Semestre',
    averageProgress: 45,
    averageGrade: 62,
    completionRate: 38,
    studentsCompleted: 20,
    averageActiveTime: 78,
    dailyActiveUsers: 35,
    weeklyActiveUsers: 45,
    averageSessionsPerStudent: 6,
    highPerformers: 8,
    mediumPerformers: 22,
    lowPerformers: 22,
    progressTrend: -12.3,
    gradeTrend: -8.5,
    engagementTrend: -15.2,
  },
];

// Generar datos de progreso en el tiempo
function generateProgressOverTime(courseId: string): CourseProgressOverTime[] {
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
  const baseProgress = Math.random() * 30 + 40;
  const baseGrade = Math.random() * 20 + 60;
  
  return months.map((month, index) => ({
    date: month,
    averageProgress: Math.min(100, Math.round(baseProgress + index * 12 + Math.random() * 5)),
    averageGrade: Math.min(100, Math.round(baseGrade + index * 8 + Math.random() * 5)),
  }));
}

// Generar datos de actividad diaria
function generateActivityData(courseId: string): StudentActivitySummary[] {
  const days = 14;
  const baseActive = Math.floor(Math.random() * 20) + 10;
  
  return Array.from({ length: days }, (_, i) => ({
    date: new Date(Date.now() - (days - 1 - i) * 24 * 60 * 60 * 1000)
      .toLocaleDateString('es-AR', { day: 'numeric', month: 'short' }),
    activeStudents: baseActive + Math.floor(Math.random() * 15),
    totalTimeSpent: (baseActive + Math.floor(Math.random() * 15)) * 45,
    averageSessionTime: 35 + Math.floor(Math.random() * 25),
  }));
}

// API simulada
export async function getCourses(): Promise<Course[]> {
  await new Promise(resolve => setTimeout(resolve, 300));
  return courses;
}

export async function getCourseMetrics(courseId: string): Promise<CourseMetrics | null> {
  await new Promise(resolve => setTimeout(resolve, 200));
  return courseMetricsData.find(c => c.courseId === courseId) || null;
}

export async function getAllCourseMetrics(): Promise<CourseMetrics[]> {
  await new Promise(resolve => setTimeout(resolve, 400));
  return courseMetricsData;
}

export async function getSelectedCourseMetrics(courseIds: string[]): Promise<CourseMetrics[]> {
  await new Promise(resolve => setTimeout(resolve, 300));
  return courseMetricsData.filter(c => courseIds.includes(c.courseId));
}

export async function getCourseProgressOverTime(courseId: string): Promise<CourseProgressOverTime[]> {
  await new Promise(resolve => setTimeout(resolve, 250));
  return generateProgressOverTime(courseId);
}

export async function getActivitySummary(courseId: string): Promise<StudentActivitySummary[]> {
  await new Promise(resolve => setTimeout(resolve, 250));
  return generateActivityData(courseId);
}

export async function getReportKPIs(): Promise<CourseReportKPIs> {
  await new Promise(resolve => setTimeout(resolve, 200));
  
  const totalStudents = courses.reduce((sum, c) => sum + c.totalStudents, 0);
  const overallCompletion = Math.round(
    courseMetricsData.reduce((sum, c) => sum + c.completionRate, 0) / courseMetricsData.length
  );
  const overallGrade = Math.round(
    courseMetricsData.reduce((sum, c) => sum + c.averageGrade, 0) / courseMetricsData.length
  );
  
  const sortedByGrade = [...courseMetricsData].sort((a, b) => b.averageGrade - a.averageGrade);
  const sortedByGradeAsc = [...courseMetricsData].sort((a, b) => a.averageGrade - b.averageGrade);
  
  return {
    totalCourses: courses.length,
    totalStudents,
    overallCompletionRate: overallCompletion,
    overallAverageGrade: overallGrade,
    topPerformingCourse: sortedByGrade[0] || null,
    needsAttentionCourse: sortedByGradeAsc[0] || null,
  };
}
