/**
 * 📊 Tipos para Reportes de Curso
 * Reportes a nivel de curso para análisis de progreso y engagement
 */

export interface Course {
  id: number | string;
  name: string;
  periodLabel: string;       // backend devuelve periodLabel (camelCase)
  period?: string;           // fallback snake_case/legacy
  schoolYear: string;
  school_year?: string;      // fallback snake_case
  startDate: string;
  endDate: string;
  totalStudents: number;
}

export interface CourseMetrics {
  courseId: string;
  courseName: string;
  course_name?: string;      // fallback snake_case
  
  periodLabel: string;       // backend devuelve periodLabel (camelCase)
  period?: string;           // fallback snake_case/legacy
  display_period?: string;   // fallback adicional
  
  schoolYear: string;
  school_year?: string;      // fallback snake_case
  totalStudents: number;
  
  // Progreso y Rendimiento
  averageProgress: number;
  averageGrade: number;
  completionRate: number;
  studentsCompleted: number;
  
  // Engagement
  averageActiveTime: number;
  dailyActiveUsers: number;     // estudiantes activos en las últimas 24h
  weeklyActiveUsers: number;    // estudiantes activos en los últimos 7 días
  averageSessionsPerStudent: number;
  
  // Distribución de rendimiento
  highPerformers: number;
  mediumPerformers: number;
  lowPerformers: number;
  
  // Tendencia
  progressTrend: number;
  gradeTrend: number;
  engagementTrend: number;
}

export interface CourseProgressOverTime {
  date: string;
  averageProgress: number;
  averageGrade: number;
}

export interface StudentActivitySummary {
  date: string;
  activeStudents: number;
  totalTimeSpent: number;
  averageSessionTime: number;
}

export interface CourseReportKPIs {
  totalCourses: number;
  totalStudents: number;
  overallCompletionRate: number;
  overallAverageGrade: number;
  topPerformingCourse: CourseMetrics | null;
  needsAttentionCourse: CourseMetrics | null;
  yearOverYearProgress: number;
  yearOverYearGrade: number;
}
