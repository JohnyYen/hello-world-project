import { unstable_cache } from 'next/cache';
import type { CourseReportKPIs } from '@/types/course-report.interface';
import { CourseReportKPIs as CourseReportKPISComponent } from '@/components/reports/course-report-kpis';

async function getReportKPIs(): Promise<CourseReportKPIs> {
  // Simulación de API call con caché
  const data = await unstable_cache(
    async () => {
      // Simular llamada a API
      await new Promise(resolve => setTimeout(resolve, 300));
      
      return {
        totalCourses: 5,
        totalStudents: 195,
        overallCompletionRate: 62,
        overallAverageGrade: 75,
        topPerformingCourse: {
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
        needsAttentionCourse: {
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
      };
    },
    ['report-kpis'],
    { revalidate: 3600, tags: ['reports'] }
  )();

  return data;
}

export async function CourseReportKPIServer() {
  const kpis = await getReportKPIs();
  return <CourseReportKPISComponent kpis={kpis} />;
}
