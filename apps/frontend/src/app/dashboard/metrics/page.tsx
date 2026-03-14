import { Suspense } from 'react';
import { LoadingState } from '@/components/ui/loading-state';
import { BarChart2 } from 'lucide-react';

// Server Components
import { MetricsKPIServer } from './metrics-kpi-server';
import { StudentProgressServer } from './student-progress-server';
import { CourseCompletionServer } from './course-completion-server';
import { EngagementServer } from './engagement-server';
import { ActivityPerformanceServer } from './activity-performance-server';

export default async function MetricsPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-900 text-white py-10 px-6 md:px-12">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3 mb-2">
            <BarChart2 className="h-6 w-6 text-blue-300" />
            <span className="text-sm font-medium text-blue-300 uppercase tracking-wider">
              Analytics
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            Métricas del Sistema
          </h1>
          <p className="text-blue-200 text-lg max-w-2xl">
            Visualización y análisis del rendimiento del sistema educativo.
            Estadísticas en tiempo real de estudiantes y cursos.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8">
        {/* KPIs - Server Component con streaming */}
        <Suspense fallback={<LoadingState message="Cargando métricas..." />}>
          <MetricsKPIServer />
        </Suspense>

        {/* Gráficos principales */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <Suspense fallback={<div className="h-80 bg-slate-200 animate-pulse rounded-lg" />}>
            <StudentProgressServer />
          </Suspense>
          <Suspense fallback={<div className="h-80 bg-slate-200 animate-pulse rounded-lg" />}>
            <CourseCompletionServer />
          </Suspense>
        </div>

        {/* Métricas de engagement y rendimiento */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <Suspense fallback={<div className="h-80 bg-slate-200 animate-pulse rounded-lg" />}>
            <EngagementServer />
          </Suspense>
          <Suspense fallback={<div className="h-80 bg-slate-200 animate-pulse rounded-lg" />}>
            <ActivityPerformanceServer />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
