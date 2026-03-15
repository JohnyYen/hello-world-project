/**
 * 📊 Servicio de Datos para Reportes de Curso
 * Proporciona datos mock para el dashboard de reportes
 * Cada curso representa un año escolar completo (no por semestre)
 */

import type {
  Course,
  CourseMetrics,
  CourseProgressOverTime,
  StudentActivitySummary,
  CourseReportKPIs,
} from '@/types/course-report.interface';

// Cursos - Uno por año escolar (no por semestre)
const courses: Course[] = [
  {
    id: 'course-2024-2025',
    name: 'Matemáticas I',
    schoolYear: '2024-2025',
    startDate: '2024-08-15',
    endDate: '2025-07-15',
    totalStudents: 45,
    averageProgress: 52,
    averageGrade: 58,
    completionRate: 38,
    studentsCompleted: 17,
    averageActiveTime: 780,
    dailyActiveUsers: 28,
    weeklyActiveUsers: 35,
    averageSessionsPerStudent: 24,
    highPerformers: 8,
    mediumPerformers: 22,
    lowPerformers: 15,
  },
  {
    id: 'course-2025-2026',
    name: 'Matemáticas I',
    schoolYear: '2025-2026',
    startDate: '2025-08-15',
    endDate: '2026-07-15',
    totalStudents: 52,
    averageProgress: 68,
    averageGrade: 74,
    completionRate: 56,
    studentsCompleted: 29,
    averageActiveTime: 1120,
    dailyActiveUsers: 38,
    weeklyActiveUsers: 44,
    averageSessionsPerStudent: 32,
    highPerformers: 18,
    mediumPerformers: 26,
    lowPerformers: 8,
  },
  {
    id: 'course-2026-2027',
    name: 'Matemáticas I',
    schoolYear: '2026-2027',
    startDate: '2026-08-15',
    endDate: '2027-07-15',
    totalStudents: 55,
    averageProgress: 75,
    averageGrade: 79,
    completionRate: 62,
    studentsCompleted: 34,
    averageActiveTime: 1280,
    dailyActiveUsers: 42,
    weeklyActiveUsers: 50,
    averageSessionsPerStudent: 38,
    highPerformers: 22,
    mediumPerformers: 25,
    lowPerformers: 8,
  },
  {
    id: 'course-2027-2028',
    name: 'Matemáticas I',
    schoolYear: '2027-2028',
    startDate: '2027-08-15',
    endDate: '2028-07-15',
    totalStudents: 48,
    averageProgress: 82,
    averageGrade: 85,
    completionRate: 71,
    studentsCompleted: 34,
    averageActiveTime: 1450,
    dailyActiveUsers: 40,
    weeklyActiveUsers: 46,
    averageSessionsPerStudent: 42,
    highPerformers: 24,
    mediumPerformers: 18,
    lowPerformers: 6,
  },
  {
    id: 'course-2028-2029',
    name: 'Matemáticas I',
    schoolYear: '2028-2029',
    startDate: '2028-08-15',
    endDate: '2029-07-15',
    totalStudents: 42,
    averageProgress: 88,
    averageGrade: 89,
    completionRate: 78,
    studentsCompleted: 33,
    averageActiveTime: 1620,
    dailyActiveUsers: 36,
    weeklyActiveUsers: 40,
    averageSessionsPerStudent: 48,
    highPerformers: 22,
    mediumPerformers: 16,
    lowPerformers: 4,
  },
  {
    id: 'course-2029-2030',
    name: 'Matemáticas I',
    schoolYear: '2029-2030',
    startDate: '2029-08-15',
    endDate: '2030-07-15',
    totalStudents: 50,
    averageProgress: 91,
    averageGrade: 92,
    completionRate: 84,
    studentsCompleted: 42,
    averageActiveTime: 1780,
    dailyActiveUsers: 44,
    weeklyActiveUsers: 48,
    averageSessionsPerStudent: 52,
    highPerformers: 28,
    mediumPerformers: 18,
    lowPerformers: 4,
  },
  {
    id: 'course-2030-2031',
    name: 'Matemáticas I',
    schoolYear: '2030-2031',
    startDate: '2030-08-15',
    endDate: '2031-07-15',
    totalStudents: 46,
    averageProgress: 94,
    averageGrade: 94,
    completionRate: 89,
    studentsCompleted: 41,
    averageActiveTime: 1920,
    dailyActiveUsers: 40,
    weeklyActiveUsers: 44,
    averageSessionsPerStudent: 56,
    highPerformers: 28,
    mediumPerformers: 15,
    lowPerformers: 3,
  },
  {
    id: 'course-2031-2032',
    name: 'Matemáticas I',
    schoolYear: '2031-2032',
    startDate: '2031-08-15',
    endDate: '2032-07-15',
    totalStudents: 52,
    averageProgress: 95,
    averageGrade: 95,
    completionRate: 91,
    studentsCompleted: 47,
    averageActiveTime: 2050,
    dailyActiveUsers: 45,
    weeklyActiveUsers: 50,
    averageSessionsPerStudent: 60,
    highPerformers: 32,
    mediumPerformers: 17,
    lowPerformers: 3,
  },
  {
    id: 'course-2032-2033',
    name: 'Matemáticas I',
    schoolYear: '2032-2033',
    startDate: '2032-08-15',
    endDate: '2033-07-15',
    totalStudents: 48,
    averageProgress: 96,
    averageGrade: 96,
    completionRate: 92,
    studentsCompleted: 44,
    averageActiveTime: 2180,
    dailyActiveUsers: 42,
    weeklyActiveUsers: 46,
    averageSessionsPerStudent: 64,
    highPerformers: 30,
    mediumPerformers: 15,
    lowPerformers: 3,
  },
  {
    id: 'course-2033-2034',
    name: 'Matemáticas I',
    schoolYear: '2033-2034',
    startDate: '2033-08-15',
    endDate: '2034-07-15',
    totalStudents: 54,
    averageProgress: 97,
    averageGrade: 97,
    completionRate: 94,
    studentsCompleted: 51,
    averageActiveTime: 2320,
    dailyActiveUsers: 48,
    weeklyActiveUsers: 52,
    averageSessionsPerStudent: 68,
    highPerformers: 36,
    mediumPerformers: 15,
    lowPerformers: 3,
  },
];

// Generar métricas con tendencias (CourseMetrics)
function generateCourseMetrics(): CourseMetrics[] {
  return courses.map((course, index) => {
    // Calcular tendencia vs año anterior
    let progressTrend = 0;
    let gradeTrend = 0;
    let engagementTrend = 0;
    
    if (index > 0) {
      const prev = courses[index - 1];
      progressTrend = ((course.averageProgress - prev.averageProgress) / prev.averageProgress) * 100;
      gradeTrend = ((course.averageGrade - prev.averageGrade) / prev.averageGrade) * 100;
      engagementTrend = ((course.averageActiveTime - prev.averageActiveTime) / prev.averageActiveTime) * 100;
    }
    
    return {
      ...course,
      progressTrend,
      gradeTrend,
      engagementTrend,
    };
  });
}

const courseMetricsData = generateCourseMetrics();

// Generar datos de progreso en el tiempo (mensual)
function generateProgressOverTime(courseId: string): CourseProgressOverTime[] {
  const months = ['Ago', 'Sep', 'Oct', 'Nov', 'Dic', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul'];
  const baseProgress = Math.random() * 20 + 30;
  const baseGrade = Math.random() * 15 + 45;
  
  return months.map((month, index) => ({
    date: month,
    averageProgress: Math.min(100, Math.round(baseProgress + index * 6 + Math.random() * 3)),
    averageGrade: Math.min(100, Math.round(baseGrade + index * 4 + Math.random() * 3)),
  }));
}

// Generar datos de actividad diaria
function generateActivityData(courseId: string): StudentActivitySummary[] {
  const days = 30;
  const baseActive = Math.floor(Math.random() * 10) + 20;
  
  return Array.from({ length: days }, (_, i) => ({
    date: new Date(Date.now() - (days - 1 - i) * 24 * 60 * 60 * 1000)
      .toLocaleDateString('es-AR', { day: 'numeric', month: 'short' }),
    activeStudents: baseActive + Math.floor(Math.random() * 15),
    totalTimeSpent: (baseActive + Math.floor(Math.random() * 15)) * 45,
    averageSessionTime: 35 + Math.floor(Math.random() * 20),
  }));
}

// API simulada
export async function getCourses(): Promise<Course[]> {
  await new Promise(resolve => setTimeout(resolve, 300));
  return courses;
}

export async function getCourseMetrics(courseId: string): Promise<CourseMetrics | null> {
  await new Promise(resolve => setTimeout(resolve, 200));
  return courseMetricsData.find(c => c.id === courseId) || null;
}

export async function getAllCourseMetrics(): Promise<CourseMetrics[]> {
  await new Promise(resolve => setTimeout(resolve, 400));
  return courseMetricsData;
}

export async function getSelectedCourseMetrics(courseIds: string[]): Promise<CourseMetrics[]> {
  await new Promise(resolve => setTimeout(resolve, 300));
  return courseMetricsData.filter(c => courseIds.includes(c.id));
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
    courses.reduce((sum, c) => sum + c.completionRate, 0) / courses.length
  );
  const overallGrade = Math.round(
    courses.reduce((sum, c) => sum + c.averageGrade, 0) / courses.length
  );
  
  const sortedByGrade = [...courseMetricsData].sort((a, b) => b.averageGrade - a.averageGrade);
  const sortedByGradeAsc = [...courseMetricsData].sort((a, b) => a.averageGrade - b.averageGrade);
  
  // Calcular tendencia promedio año a año
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
