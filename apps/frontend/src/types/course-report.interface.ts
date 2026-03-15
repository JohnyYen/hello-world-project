/**
 * 📊 Tipos para Reportes de Curso
 * Reportes a nivel de curso para análisis de progreso y engagement
 */

export interface Course {
  id: string;
  name: string;           // Nombre de la materia (ej: "Matemáticas I")
  schoolYear: string;     // Año escolar completo (ej: "2025-2026")
  startDate: string;
  endDate: string;
  totalStudents: number;
  
  // Métricas del año completo
  averageProgress: number;
  averageGrade: number;
  completionRate: number;
  studentsCompleted: number;
  averageActiveTime: number;
  dailyActiveUsers: number;
  weeklyActiveUsers: number;
  averageSessionsPerStudent: number;
  highPerformers: number;
  mediumPerformers: number;
  lowPerformers: number;
}

export interface CourseMetrics extends Course {
  // Tendencia vs año anterior
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

// Tipos para filtros de reporte
export interface ReportFilters {
  courses: string[];
  dateRange?: {
    start: string;
    end: string;
  };
  compareMode: boolean;
}

// Tipos para KPIs de resumen
export interface CourseReportKPIs {
  totalCourses: number;
  totalStudents: number;
  overallCompletionRate: number;
  overallAverageGrade: number;
  topPerformingCourse: CourseMetrics | null;
  needsAttentionCourse: CourseMetrics | null;
  
  // Métricas de tendencia año a año
  yearOverYearProgress: number;
  yearOverYearGrade: number;
}
