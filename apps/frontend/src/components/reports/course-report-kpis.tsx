'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { 
  GraduationCap, 
  Users, 
  TrendingUp, 
  Target,
  AlertTriangle,
  Star,
  Clock,
  BarChart3
} from 'lucide-react';
import type { CourseReportKPIs, CourseMetrics } from '@/types/course-report.interface';

interface CourseReportKPIsProps {
  kpis: CourseReportKPIs;
}

export function CourseReportKPIs({ kpis }: CourseReportKPIsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Total Cursos */}
      <Card className="border-0 shadow-lg overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
          <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-300">
            Cursos Activos
          </CardTitle>
          <GraduationCap className="h-4 w-4 text-slate-500" />
        </CardHeader>
        <CardContent className="relative z-10">
          <div className="text-3xl font-bold text-slate-900 dark:text-white">
            {kpis.totalCourses}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            {kpis.totalStudents} estudiantes total
          </p>
        </CardContent>
      </Card>

      {/* Tasa de Completado */}
      <Card className="border-0 shadow-lg overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-accent via-accent to-accent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
          <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-300">
            Tasa de Completado
          </CardTitle>
          <TrendingUp className="h-4 w-4 text-accent" />
        </CardHeader>
        <CardContent className="relative z-10">
          <div className="text-3xl font-bold text-accent">
            {kpis.overallCompletionRate}%
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Promedio general
          </p>
        </CardContent>
      </Card>

      {/* Promedio de Calificaciones */}
      <Card className="border-0 shadow-lg overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-primary via-primary to-primary opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
          <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-300">
            Calificación Promedio
          </CardTitle>
          <Target className="h-4 w-4 text-primary" />
        </CardHeader>
        <CardContent className="relative z-10">
          <div className="text-3xl font-bold text-primary">
            {kpis.overallAverageGrade}%
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Entre todos los cursos
          </p>
        </CardContent>
      </Card>

      {/* Estudiantes */}
      <Card className="border-0 shadow-lg overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-violet-600 via-violet-500 to-violet-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
          <CardTitle className="text-sm font-medium text-slate-600 dark:text-slate-300">
            Total Estudiantes
          </CardTitle>
          <Users className="h-4 w-4 text-violet-600" />
        </CardHeader>
        <CardContent className="relative z-10">
          <div className="text-3xl font-bold text-violet-600">
            {kpis.totalStudents}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Matriculados actualmente
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

interface CourseHighlightCardsProps {
  topCourse: CourseMetrics | null;
  attentionCourse: CourseMetrics | null;
}

export function CourseHighlightCards({ topCourse, attentionCourse }: CourseHighlightCardsProps) {
  if (!topCourse || !attentionCourse) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Curso Destacado */}
      <Card className="border-0 shadow-lg overflow-hidden">
        <div className="h-2 bg-gradient-to-r from-accent via-accent to-accent" />
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <Star className="h-5 w-5 text-accent" />
            <CardTitle className="text-lg font-semibold">Curso Mejor Rendimiento</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-bold text-slate-900">{topCourse.courseName}</h3>
              <p className="text-sm text-slate-500">{topCourse.period}</p>
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center p-3 bg-accent/10 rounded-lg">
                <div className="text-2xl font-bold text-accent">{topCourse.averageGrade}%</div>
                <div className="text-xs text-slate-500">Promedio</div>
              </div>
              <div className="text-center p-3 bg-accent/10 rounded-lg">
                <div className="text-2xl font-bold text-accent">{topCourse.completionRate}%</div>
                <div className="text-xs text-slate-500">Completado</div>
              </div>
              <div className="text-center p-3 bg-accent/10 rounded-lg">
                <div className="text-2xl font-bold text-accent">{topCourse.highPerformers}</div>
                <div className="text-xs text-slate-500">Destacados</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Curso que Necesita Atención */}
      <Card className="border-0 shadow-lg overflow-hidden">
        <div className="h-2 bg-gradient-to-r from-red-400 via-red-500 to-red-600" />
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-red-500" />
            <CardTitle className="text-lg font-semibold">Requiere Atención</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-bold text-slate-900">{attentionCourse.courseName}</h3>
              <p className="text-sm text-slate-500">{attentionCourse.period}</p>
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center p-3 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">{attentionCourse.averageGrade}%</div>
                <div className="text-xs text-slate-500">Promedio</div>
              </div>
              <div className="text-center p-3 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">{attentionCourse.completionRate}%</div>
                <div className="text-xs text-slate-500">Completado</div>
              </div>
              <div className="text-center p-3 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">{attentionCourse.lowPerformers}</div>
                <div className="text-xs text-slate-500">Bajo Rend.</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
