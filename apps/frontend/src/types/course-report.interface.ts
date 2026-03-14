/**
 * 📊 Tipos para Reportes de Curso
 * Reportes a nivel de curso para análisis de progreso y engagement
 */

export interface Course {
  id: string;
  name: string;
  period: string;
  startDate: string;
  endDate: string;
  totalStudents: number;
}

export interface CourseMetrics {
  courseId: string;
  courseName: string;
  period: string;
  
  // Progreso y Rendimiento
  averageProgress: number;
  averageGrade: number;
  completionRate: number;
  studentsCompleted: number;
  
  // Engagement
  averageActiveTime: number; // minutos promedio
  dailyActiveUsers: number;
  weeklyActiveUsers: number;
  averageSessionsPerStudent: number;
  
  // Distribución de rendimiento
  highPerformers: number;
  mediumPerformers: number;
  lowPerformers: number;
  
  // Tendencia (porcentaje de cambio vs período anterior)
  progressTrend: number;
  gradeTrend: number;
  engagementTrend: number;
}

export interface CourseComparison {
  courses: CourseMetrics[];
  metrics: ComparisonMetric[];
}

export interface ComparisonMetric {
  name: string;
  key: keyof CourseMetrics;
  values: number[];
  unit: string;
  higherIsBetter: boolean;
}

export interface CourseProgressOverTime {
  date: string;
  averageProgress: number;
  averageGrade: number;
}

export interface StudentActivitySummary {
  date: string;
  activeStudents: number;
  totalTimeSpent: number; // minutos
  averageSessionTime: number;
}

export interface PerformanceDistribution {
  range: string;
  minScore: number;
  maxScore: number;
  count: number;
  percentage: number;
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
}
