/**
 * 📊 Tipos para Reportes de Curso
 * Reportes a nivel de curso para análisis de progreso y engagement
 */

export interface Course {
  id: number | string;
  name: string;
  period: string;
  schoolYear: string;
  startDate: string;
  endDate: string;
  totalStudents: number;
}

export interface CourseMetrics {
  courseId: string;
  courseName: string;  // backend puede devolver course_name (snake_case)
  course_name?: string;  // alternativa por compatibilidad
  period: string;
  schoolYear: string;
  school_year?: string;  // alternativa por compatibilidad
  totalStudents: number;  // ← AGREGADO: Total de estudiantes del curso
  
  // Progreso y Rendimiento
  averageProgress: number;
  averageGrade: number;
  completionRate: number;
  studentsCompleted: number;
  
  // Engagement
  averageActiveTime: number;
  dailyActiveUsers: number;
  weeklyActiveUsers: number;
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
