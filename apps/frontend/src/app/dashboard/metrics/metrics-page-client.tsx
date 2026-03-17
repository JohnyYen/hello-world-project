"use client";

import { useRef } from "react";
import { ExportButton } from "@/components/export/ExportButton";
import { Suspense } from "react";
import { LoadingState } from "@/components/ui/loading-state";
import { BarChart2 } from "lucide-react";

// Server Components
import { MetricsKPIServer } from "./metrics-kpi-server";
import { StudentProgressServer } from "./student-progress-server";
import { CourseCompletionServer } from "./course-completion-server";
import { EngagementServer } from "./engagement-server";
import { ActivityPerformanceServer } from "./activity-performance-server";
import { MetricTypesServer } from "./metric-types-server";

export function MetricsPageClient() {
  const containerRef = useRef<HTMLDivElement>(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Background pattern */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 via-indigo-500 to-violet-600 text-white py-10 px-6 md:px-12 relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <BarChart2 className="h-6 w-6 text-indigo-200" />
              <span className="text-sm font-medium text-indigo-200 uppercase tracking-wider">
                Analytics
              </span>
            </div>
            <ExportButton 
              targetRef={containerRef}
              fileName="metricas-sistema"
              variant="outline"
              size="sm"
              label="Exportar PDF"
              className="bg-white/10 border-white/20 text-white hover:bg-white/20"
            />
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2 mt-2">
            Métricas del Sistema
          </h1>
          <p className="text-indigo-100 text-lg max-w-2xl">
            Visualización y análisis del rendimiento del sistema educativo.
            Estadísticas en tiempo real de estudiantes y cursos.
          </p>
        </div>
      </div>

      <div ref={containerRef} className="max-w-7xl mx-auto px-6 md:px-12 py-8 relative z-10">
        {/* KPIs - Server Component con streaming */}
        <Suspense fallback={<LoadingState message="Cargando métricas..." />}>
          <MetricsKPIServer />
        </Suspense>

        {/* Gráficos principales */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <Suspense fallback={<div className="h-80 bg-slate-200 dark:bg-slate-800 animate-pulse rounded-xl" />}>
            <StudentProgressServer />
          </Suspense>
          <Suspense fallback={<div className="h-80 bg-slate-200 dark:bg-slate-800 animate-pulse rounded-xl" />}>
            <CourseCompletionServer />
          </Suspense>
        </div>

        {/* Métricas de engagement y rendimiento */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <Suspense fallback={<div className="h-80 bg-slate-200 dark:bg-slate-800 animate-pulse rounded-xl" />}>
            <EngagementServer />
          </Suspense>
          <Suspense fallback={<div className="h-80 bg-slate-200 dark:bg-slate-800 animate-pulse rounded-xl" />}>
            <ActivityPerformanceServer />
          </Suspense>
        </div>

        {/* Catálogo de tipos de métricas */}
        <Suspense fallback={<LoadingState message="Cargando tipos de métricas..." />}>
          <MetricTypesServer />
        </Suspense>
      </div>
    </div>
  );
}
