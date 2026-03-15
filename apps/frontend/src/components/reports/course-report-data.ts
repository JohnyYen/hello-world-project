/**
 * 📊 Servicio de Datos para Reportes de Curso
 * Proporciona datos mock para el dashboard de reportes
 * Todos los cursos pertenecen a la misma materia (Matemáticas I)
 * y representan diferentes períodos/años escolares
 */

import type {
  Course,
  CourseMetrics,
  CourseProgressOverTime,
  StudentActivitySummary,
  CourseReportKPIs,
  ReportFilters,
} from '@/types/course-report.interface';

// Cursos - Todos son "Matemáticas I" en diferentes años escolares
const courses: Course[] = [
  {
    id: 'course-2024',
    name: 'Matemáticas I',
    period: '2024 - Segundo Semestre',
    schoolYear: '2024-2025',
    startDate: '2024-08-15',
    endDate: '2024-12-15',
    totalStudents: 45,
  },
  {
    id: 'course-2025-1',
    name: 'Matemáticas I',
    period: '2025 - Primer Semestre',
    schoolYear: '2024-2025',
    startDate: '2025-01-15',
    endDate: '2025-06-15',
    totalStudents: 52,
  },
  {
    id: 'course-2025-2',
    name: 'Matemáticas I',
    period: '2025 - Segundo Semestre',
    schoolYear: '2025-2026',
    startDate: '2025-08-15',
    endDate: '2025-12-15',
    totalStudents: 48,
  },
  {
    id: 'course-2026-1',
    name: 'Matemáticas I',
    period: '2026 - Primer Semestre',
    schoolYear: '2025-2026',
    startDate: '2026-01-15',
    endDate: '2026-06-15',
    totalStudents: 55,
  },
  {
    id: 'course-2026-2',
    name: 'Matemáticas I',
    period: '2026 - Segundo Semestre',
    schoolYear: '2026-2027',
    startDate: '2026-08-15',
    endDate: '2026-12-15',
    totalStudents: 42,
  },
];

// Métricas de cada curso - evolucionando positivamente año a año
const courseMetricsData: CourseMetrics[] = [
  {
    courseId: 'course-2024',
    courseName: 'Matemáticas I',
    period: '2024 - Segundo Semestre',
    schoolYear: '2024-2025',
    averageProgress: 52,
    averageGrade: 58,
    completionRate: 38,
    studentsCompleted: 17,
    averageActiveTime: 78,
    dailyActiveUsers: 28,
    weeklyActiveUsers: 35,
    averageSessionsPerStudent: 6,
    highPerformers: 8,
    mediumPerformers: 22,
    lowPerformers: 15,
    progressTrend: 0,    // Primer período, no hay tendencia previa
    gradeTrend: 0,
    engagementTrend: 0,
  },
  {
    courseId: 'course-2025-1',
    courseName: 'Matemáticas I',
    period: '2025 - Primer Semestre',
    schoolYear: '2024-2025',
    averageProgress: 61,
    averageGrade: 67,
    completionRate: 48,
    studentsCompleted: 25,
    averageActiveTime: 95,
    dailyActiveUsers: 35,
    weeklyActiveUsers: 42,
    averageSessionsPerStudent: 8,
    highPerformers: 14,
    mediumPerformers: 26,
    lowPerformers: 12,
    progressTrend: 9.2,    // +9.2% vs período anterior
    gradeTrend: 8.5,
    engagementTrend: 12.4,
  },
  {
    courseId: 'course-2025-2',
    courseName: 'Matemáticas I',
    period: '2025 - Segundo Semestre',
    schoolYear: '2025-2026',
    averageProgress: 68,
    averageGrade: 74,
    completionRate: 56,
    studentsCompleted: 27,
    averageActiveTime: 112,
    dailyActiveUsers: 38,
    weeklyActiveUsers: 44,
    averageSessionsPerStudent: 10,
    highPerformers: 18,
    mediumPerformers: 22,
    lowPerformers: 8,
    progressTrend: 7.1,
    gradeTrend: 6.8,
    engagementTrend: 9.8,
  },
  {
    courseId: 'course-2026-1',
    courseName: 'Matemáticas I',
    period: '2026 - Primer Semestre',
    schoolYear: '2025-2026',
    averageProgress: 75,
    averageGrade: 79,
    completionRate: 62,
    studentsCompleted: 34,
    averageActiveTime: 128,
    dailyActiveUsers: 42,
    weeklyActiveUsers: 50,
    averageSessionsPerStudent: 12,
    highPerformers: 22,
    mediumPerformers: 25,
    lowPerformers: 8,
    progressTrend: 5.8,
    gradeTrend: 4.9,
    engagementTrend: 7.2,
  },
  {
    courseId: 'course-2026-2',
    courseName: 'Matemáticas I',
    period: '2026 - Segundo Semestre',
    schoolYear: '2026-2027',
    averageProgress: 82,
    averageGrade: 85,
    completionRate: 71,
    studentsCompleted: 30,
    averageActiveTime: 145,
    dailyActiveUsers: 38,
    weeklyActiveUsers: 42,
    averageSessionsPerStudent: 14,
    highPerformers: 20,
    mediumPerformers: 17,
    lowPerformers: 5,
    progressTrend: 6.2,
    gradeTrend: 5.4,
    engagementTrend: 4.8,
  },
];

// Generar datos de progreso en el tiempo
function generateProgressOverTime(courseId: string): CourseProgressOverTime[] {
  const months = ['Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
  const baseProgress = Math.random() * 20 + 40;
  const baseGrade = Math.random() * 15 + 50;
  
  return months.map((month, index) => ({
    date: month,
    averageProgress: Math.min(100, Math.round(baseProgress + index * 15 + Math.random() * 5)),
    averageGrade: Math.min(100, Math.round(baseGrade + index * 10 + Math.random() * 5)),
  }));
}

// Generar datos de actividad diaria
function generateActivityData(courseId: string): StudentActivitySummary[] {
  const days = 14;
  const baseActive = Math.floor(Math.random() * 15) + 15;
  
  return Array.from({ length: days }, (_, i) => ({
    date: new Date(Date.now() - (days - 1 - i) * 24 * 60 * 60 * 1000)
      .toLocaleDateString('es-AR', { day: 'numeric', month: 'short' }),
    activeStudents: baseActive + Math.floor(Math.random() * 12),
    totalTimeSpent: (baseActive + Math.floor(Math.random() * 12)) * 42,
    averageSessionTime: 32 + Math.floor(Math.random() * 20),
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
  
  // Calcular tendencia año a año (excluyendo el primer período)
  const trends = courseMetricsData.slice(1);
  const yearOverYearProgress = Math.round(
    trends.reduce((sum, c) => sum + c.progressTrend, 0) / trends.length
  );
  const yearOverYearGrade = Math.round(
    trends.reduce((sum, c) => sum + c.gradeTrend, 0) / trends.length
  );
  
  return {
    totalCourses: courses.length,
    totalStudents,
    overallCompletionRate: overallCompletion,
    overallAverageGrade: overallGrade,
    topPerformingCourse: sortedByGrade[0] || null,
    needsAttentionCourse: sortedByGradeAsc[0] || null,
    yearOverYearProgress,
    yearOverYearGrade,
  };
}
