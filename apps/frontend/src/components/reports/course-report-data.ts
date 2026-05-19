/**
 * 📊 Servicio de Datos para Reportes de Curso
 * Datos mock con períodos semestrales agrupados por año escolar
 */

import type {
  Course,
  CourseMetrics,
  CourseProgressOverTime,
  StudentActivitySummary,
  CourseReportKPIs,
} from '@/types/course-report.interface';

// Cursos - Semestres agrupados por año escolar
const courses: Course[] = [
  // 2024-2025
  { id: '2024-2025-1', name: 'Matemáticas I', period: '2024 - Primer Semestre', schoolYear: '2024-2025', startDate: '2024-01-15', endDate: '2024-06-15', totalStudents: 42 },
  { id: '2024-2025-2', name: 'Matemáticas I', period: '2024 - Segundo Semestre', schoolYear: '2024-2025', startDate: '2024-08-15', endDate: '2024-12-15', totalStudents: 45 },
  // 2025-2026
  { id: '2025-2026-1', name: 'Matemáticas I', period: '2025 - Primer Semestre', schoolYear: '2025-2026', startDate: '2025-01-15', endDate: '2025-06-15', totalStudents: 48 },
  { id: '2025-2026-2', name: 'Matemáticas I', period: '2025 - Segundo Semestre', schoolYear: '2025-2026', startDate: '2025-08-15', endDate: '2025-12-15', totalStudents: 52 },
  // 2026-2027
  { id: '2026-2027-1', name: 'Matemáticas I', period: '2026 - Primer Semestre', schoolYear: '2026-2027', startDate: '2026-01-15', endDate: '2026-06-15', totalStudents: 55 },
  { id: '2026-2027-2', name: 'Matemáticas I', period: '2026 - Segundo Semestre', schoolYear: '2026-2027', startDate: '2026-08-15', endDate: '2026-12-15', totalStudents: 48 },
  // 2027-2028
  { id: '2027-2028-1', name: 'Matemáticas I', period: '2027 - Primer Semestre', schoolYear: '2027-2028', startDate: '2027-01-15', endDate: '2027-06-15', totalStudents: 50 },
  { id: '2027-2028-2', name: 'Matemáticas I', period: '2027 - Segundo Semestre', schoolYear: '2027-2028', startDate: '2027-08-15', endDate: '2027-12-15', totalStudents: 46 },
  // 2028-2029
  { id: '2028-2029-1', name: 'Matemáticas I', period: '2028 - Primer Semestre', schoolYear: '2028-2029', startDate: '2028-01-15', endDate: '2028-06-15', totalStudents: 52 },
  { id: '2028-2029-2', name: 'Matemáticas I', period: '2028 - Segundo Semestre', schoolYear: '2028-2029', startDate: '2028-08-15', endDate: '2028-12-15', totalStudents: 54 },
];

// Métricas con tendencia positiva
const courseMetricsData: CourseMetrics[] = [
  // 2024-2025
  { courseId: '2024-2025-1', courseName: 'Matemáticas I', totalStudents: 42, period: '2024 - Primer Semestre', schoolYear: '2024-2025', averageProgress: 48, averageGrade: 55, completionRate: 35, studentsCompleted: 15, averageActiveTime: 680, dailyActiveUsers: 25, weeklyActiveUsers: 30, averageSessionsPerStudent: 20, highPerformers: 6, mediumPerformers: 20, lowPerformers: 16, progressTrend: 0, gradeTrend: 0, engagementTrend: 0 },
  { courseId: '2024-2025-2', courseName: 'Matemáticas I', totalStudents: 45, period: '2024 - Segundo Semestre', schoolYear: '2024-2025', averageProgress: 52, averageGrade: 58, completionRate: 38, studentsCompleted: 17, averageActiveTime: 780, dailyActiveUsers: 28, weeklyActiveUsers: 35, averageSessionsPerStudent: 24, highPerformers: 8, mediumPerformers: 22, lowPerformers: 15, progressTrend: 8.3, gradeTrend: 5.5, engagementTrend: 14.7 },
  // 2025-2026
  { courseId: '2025-2026-1', courseName: 'Matemáticas I', totalStudents: 48, period: '2025 - Primer Semestre', schoolYear: '2025-2026', averageProgress: 58, averageGrade: 65, completionRate: 45, studentsCompleted: 22, averageActiveTime: 880, dailyActiveUsers: 32, weeklyActiveUsers: 40, averageSessionsPerStudent: 28, highPerformers: 12, mediumPerformers: 24, lowPerformers: 12, progressTrend: 11.5, gradeTrend: 12.1, engagementTrend: 12.8 },
  { courseId: '2025-2026-2', courseName: 'Matemáticas I', totalStudents: 52, period: '2025 - Segundo Semestre', schoolYear: '2025-2026', averageProgress: 65, averageGrade: 72, completionRate: 52, studentsCompleted: 27, averageActiveTime: 980, dailyActiveUsers: 36, weeklyActiveUsers: 44, averageSessionsPerStudent: 32, highPerformers: 16, mediumPerformers: 26, lowPerformers: 10, progressTrend: 12.1, gradeTrend: 10.8, engagementTrend: 11.4 },
  // 2026-2027
  { courseId: '2026-2027-1', courseName: 'Matemáticas I', totalStudents: 55, period: '2026 - Primer Semestre', schoolYear: '2026-2027', averageProgress: 72, averageGrade: 78, completionRate: 58, studentsCompleted: 32, averageActiveTime: 1080, dailyActiveUsers: 40, weeklyActiveUsers: 48, averageSessionsPerStudent: 36, highPerformers: 20, mediumPerformers: 25, lowPerformers: 10, progressTrend: 10.8, gradeTrend: 8.3, engagementTrend: 10.2 },
  { courseId: '2026-2027-2', courseName: 'Matemáticas I', totalStudents: 48, period: '2026 - Segundo Semestre', schoolYear: '2026-2027', averageProgress: 78, averageGrade: 82, completionRate: 64, studentsCompleted: 31, averageActiveTime: 1180, dailyActiveUsers: 38, weeklyActiveUsers: 44, averageSessionsPerStudent: 40, highPerformers: 22, mediumPerformers: 20, lowPerformers: 6, progressTrend: 8.3, gradeTrend: 5.1, engagementTrend: 9.3 },
  // 2027-2028
  { courseId: '2027-2028-1', courseName: 'Matemáticas I', totalStudents: 50, period: '2027 - Primer Semestre', schoolYear: '2027-2028', averageProgress: 82, averageGrade: 86, completionRate: 70, studentsCompleted: 35, averageActiveTime: 1280, dailyActiveUsers: 42, weeklyActiveUsers: 48, averageSessionsPerStudent: 44, highPerformers: 24, mediumPerformers: 20, lowPerformers: 6, progressTrend: 5.1, gradeTrend: 4.9, engagementTrend: 8.5 },
  { courseId: '2027-2028-2', courseName: 'Matemáticas I', totalStudents: 46, period: '2027 - Segundo Semestre', schoolYear: '2027-2028', averageProgress: 85, averageGrade: 88, completionRate: 74, studentsCompleted: 34, averageActiveTime: 1380, dailyActiveUsers: 40, weeklyActiveUsers: 44, averageSessionsPerStudent: 48, highPerformers: 26, mediumPerformers: 16, lowPerformers: 4, progressTrend: 3.7, gradeTrend: 2.3, engagementTrend: 7.8 },
  // 2028-2029
  { courseId: '2028-2029-1', courseName: 'Matemáticas I', totalStudents: 52, period: '2028 - Primer Semestre', schoolYear: '2028-2029', averageProgress: 88, averageGrade: 90, completionRate: 78, studentsCompleted: 41, averageActiveTime: 1480, dailyActiveUsers: 44, weeklyActiveUsers: 50, averageSessionsPerStudent: 52, highPerformers: 28, mediumPerformers: 18, lowPerformers: 4, progressTrend: 3.5, gradeTrend: 2.3, engagementTrend: 7.2 },
  { courseId: '2028-2029-2', courseName: 'Matemáticas I', totalStudents: 54, period: '2028 - Segundo Semestre', schoolYear: '2028-2029', averageProgress: 90, averageGrade: 92, completionRate: 82, studentsCompleted: 44, averageActiveTime: 1580, dailyActiveUsers: 46, weeklyActiveUsers: 50, averageSessionsPerStudent: 56, highPerformers: 30, mediumPerformers: 18, lowPerformers: 4, progressTrend: 2.3, gradeTrend: 2.2, engagementTrend: 6.8 },
];

function generateProgressOverTime(courseId: string): CourseProgressOverTime[] {
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
  const baseProgress = Math.random() * 20 + 30;
  const baseGrade = Math.random() * 15 + 45;
  
  return months.map((month, index) => ({
    date: month,
    averageProgress: Math.min(100, Math.round(baseProgress + index * 5 + Math.random() * 3)),
    averageGrade: Math.min(100, Math.round(baseGrade + index * 4 + Math.random() * 3)),
  }));
}

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
  const overallCompletion = Math.round(courseMetricsData.reduce((sum, c) => sum + c.completionRate, 0) / courseMetricsData.length);
  const overallGrade = Math.round(courseMetricsData.reduce((sum, c) => sum + c.averageGrade, 0) / courseMetricsData.length);
  
  const sortedByGrade = [...courseMetricsData].sort((a, b) => b.averageGrade - a.averageGrade);
  const sortedByGradeAsc = [...courseMetricsData].sort((a, b) => a.averageGrade - b.averageGrade);
  
  const trends = courseMetricsData.slice(1);
  const yearOverYearProgress = Math.round(trends.reduce((sum, c) => sum + c.progressTrend, 0) / trends.length);
  const yearOverYearGrade = Math.round(trends.reduce((sum, c) => sum + c.gradeTrend, 0) / trends.length);
  
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
