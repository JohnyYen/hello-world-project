'use client';

import { useState, useEffect, useMemo, useRef } from 'react';
import { 
  Users, 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Target, 
  Award,
  BarChart3,
  ArrowRightLeft,
  BookOpen,
  CheckCircle2,
  Calendar,
  ChevronDown,
  Check,
  X,
} from 'lucide-react';
import { MetricCard, LineChart as LineChartComponent, BarChart, DonutChart } from '@/components/charts';
import { ChartHelp } from '@/components/ui/chart-help';
import { ExportButton } from '@/components/export/ExportButton';
import { CourseMultiSelector } from '@/components/reports/course-multi-selector';
import { CourseHighlightCards } from '@/components/reports/course-report-kpis';
import { cn } from '@/lib/utils';
import Link from 'next/link';
import { courseReportsService, apiClient } from '@/lib/api-client';
import type { Course, CourseMetrics, CourseReportKPIs, CourseProgressOverTime } from '@/types/course-report.interface';

// Utility functions

// Normalize course metrics to handle both snake_case and camelCase from backend
function normalizeMetric(metric: any): any {
  return {
    ...metric,
    // Handle snake_case from backend
    courseId: metric.courseId ?? metric.course_id ?? '',
    courseName: metric.courseName || metric.course_name || '',
    schoolYear: metric.schoolYear || metric.school_year || '',
    periodLabel: metric.periodLabel || metric.period_label || metric.period || metric.display_period || '',
    period: metric.periodLabel || metric.period_label || metric.period || metric.display_period || '',
  };
}

function formatPlayTime(minutes: number): string {
  const abs = Math.abs(minutes);
  const hours = Math.floor(abs / 60);
  const mins = Math.round(abs % 60);
  const sign = minutes < 0 ? '−' : '+';
  if (hours > 0) {
    return `${sign}${hours}h ${mins}m`;
  }
  return `${sign}${mins}m`;
}

// Animated section header
function SectionHeader({ 
  title, 
  subtitle, 
  icon: Icon, 
  delay = 0,
  accentColor = 'indigo'
}: { 
  title: string; 
  subtitle?: string; 
  icon?: React.ElementType; 
  delay?: number;
  accentColor?: 'indigo' | 'violet' | 'amber';
}) {
  const colorClasses = {
    indigo: 'border-indigo-500 dark:border-indigo-400 text-indigo-600 dark:text-indigo-400 bg-indigo-100 dark:bg-indigo-900/50',
    violet: 'border-violet-500 dark:border-violet-400 text-violet-600 dark:text-violet-400 bg-violet-100 dark:bg-violet-900/50',
    amber: 'border-amber-500 dark:border-amber-400 text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/50',
  };

  return (
    <div 
      className="relative mb-8 pl-4 border-l-4 border-indigo-500 dark:border-indigo-400"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center gap-3 mb-2">
        {Icon && (
          <div className={cn("p-2 rounded-lg", colorClasses[accentColor])}>
            <Icon className="w-5 h-5" />
          </div>
        )}
        <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      </div>
      {subtitle && (
        <p className="text-muted-foreground ml-12">{subtitle}</p>
      )}
    </div>
  );
}



// Comparison badge
function ComparisonBadge({ trend }: { trend: number }) {
  const isPositive = trend >= 0;
  return (
    <span className={cn(
      "inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold",
      isPositive 
        ? "bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-400" 
        : "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400"
    )}>
      {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
      {Math.abs(trend).toFixed(1)}%
    </span>
  );
}

// Find previous metric for same course to show difference
function getPreviousMetric(metrics: CourseMetrics[], currentIndex: number): CourseMetrics | null {
  if (currentIndex <= 0) return null;
  const current = metrics[currentIndex];
  for (let i = currentIndex - 1; i >= 0; i--) {
    const prev = metrics[i];
    if (prev.courseName?.toLowerCase() === current.courseName?.toLowerCase()) {
      return prev;
    }
  }
  return null;
}

// Trend indicator arrow
function TrendArrow({ value }: { value: number }) {
  const isPositive = value >= 0;
  return (
    <span className={cn("inline-flex items-center", isPositive ? "text-indigo-400" : "text-red-400")}>
      {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
      <span className="ml-1 font-semibold">{Math.abs(value).toFixed(1)}%</span>
    </span>
  );
}

// Main component
export default function ReportsPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);
  const [selectedMetrics, setSelectedMetrics] = useState<CourseMetrics[]>([]);
  const [kpis, setKpis] = useState<CourseReportKPIs | null>(null);
  const [progressData, setProgressData] = useState<Record<string, CourseProgressOverTime[]>>({});
  const [activeTab, setActiveTab] = useState('overview');

  const latestYear = useMemo(() => {
    if (!courses || courses.length === 0) return '';
    // Find max year without sort to avoid localeCompare errors
    let maxYear = '';
    for (const c of courses) {
      if (!c) continue;
      const year = (c as any)?.schoolYear || (c as any)?.school_year || '';
      if (year && year > maxYear) maxYear = year;
    }
    return maxYear;
  }, [courses]);

  const subjectName = useMemo(() => {
    return courses.length > 0 ? courses[0].name : 'Matemáticas I';
  }, [courses]);

  useEffect(() => {
    const loadInitialData = async () => {
        try {
          const [coursesData, kpisData] = await Promise.all([
            courseReportsService.getCourses(),
            courseReportsService.getReportKPIs()
          ]);

        // Backend returns raw data (not wrapped in ApiResponse), handle both formats
        const coursesArray = Array.isArray(coursesData) ? coursesData : (coursesData?.data ?? []);

        // Backend returns snake_case (school_year), handle both cases
        const normalizedCourses = coursesArray.map((c: any) => ({
          ...c,
          schoolYear: c.schoolYear || c.school_year || '',
          name: c.name || c.course_name || '',
          periodLabel: c.periodLabel || c.period_label || c.period || c.display_period || '',
          period: c.periodLabel || c.period_label || c.period || c.display_period || '',
        }));

        setCourses(normalizedCourses);
        setKpis(kpisData?.data ?? kpisData ?? null);

        // Select latest year by default (without sort)
        if (coursesArray.length > 0) {
          let latestSchoolYear = '';
          for (const c of coursesArray) {
            const year = (c as any)?.schoolYear || (c as any)?.school_year || '';
            if (year && year > latestSchoolYear) latestSchoolYear = year;
          }
          const latestYearCourses = coursesArray.filter(c => {
            const year = (c as any)?.schoolYear || (c as any)?.school_year || '';
            return year === latestSchoolYear;
          });
          setSelectedCourses(latestYearCourses.map(c => String(c.id)));
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Error al cargar los reportes';
        setError(message);
        console.error('Error loading reports data:', err);
      } finally {
        setLoading(false);
      }
    };

    loadInitialData();
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    let cancelled = false;

    const loadSelectedMetrics = async () => {
      if (selectedCourses.length === 0) {
        if (!cancelled) {
          setSelectedMetrics([]);
          setProgressData({});
        }
        return;
      }

      try {
        const metricsResponse = await courseReportsService.getCourseMetrics(
          selectedCourses
        );
        if (cancelled) return;

        const metrics = (Array.isArray(metricsResponse) ? metricsResponse : (metricsResponse?.data || metricsResponse || [])) as any[];
        // Normalize metrics to handle snake_case from backend
        const normalizedMetrics = metrics.map(normalizeMetric);
        // Sort without localeCompare to avoid errors
        const sortedMetrics = [...normalizedMetrics].sort((a: any, b: any) => {
          const yearA = a?.schoolYear || a?.school_year || '';
          const yearB = b?.schoolYear || b?.school_year || '';
          if (yearA === yearB) {
            const periodA = a?.period || a?.display_period || '';
            const periodB = b?.period || b?.display_period || '';
            return String(periodB).localeCompare(String(periodA));
          }
          return String(yearB).localeCompare(String(yearA));
        });

        setSelectedMetrics(sortedMetrics);

        const progressPromises = selectedCourses.map(async (courseId) => {
          const response = await courseReportsService.getProgressOverTime(courseId);
          return { courseId, data: response.data || [] };
        });

        const progressResults = await Promise.all(progressPromises);
        if (cancelled) return;

        const progressMap: Record<string, CourseProgressOverTime[]> = {};
        progressResults.forEach(({ courseId, data }) => {
          progressMap[courseId] = data;
        });
        setProgressData(progressMap);
      } catch (err) {
        if (!cancelled && !(err instanceof DOMException && err.name === 'AbortError')) {
          const message = err instanceof Error ? err.message : 'Error al cargar métricas';
          setError(message);
          console.error('Error loading selected metrics:', err);
        }
      }
    };

    loadSelectedMetrics();

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [selectedCourses]);

  const toggleCourse = (courseId: string) => {
    setSelectedCourses(prev => 
      prev.includes(courseId) 
        ? prev.filter(id => id !== courseId)
        : [...prev, courseId]
    );
  };

  const evolutionData = useMemo(() => {
    if (selectedMetrics.length < 2) return null;
    
    const first = selectedMetrics[0];
    const last = selectedMetrics[selectedMetrics.length - 1];
    
    return {
      progressDiff: last.averageProgress - first.averageProgress,
      gradeDiff: last.averageGrade - first.averageGrade,
      completionDiff: last.completionRate - first.completionRate,
      timeDiff: last.averageActiveTime - first.averageActiveTime,
      periodsCompared: selectedMetrics.length,
    };
  }, [selectedMetrics]);

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/20 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="w-20 h-20 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center mb-6">
              <X className="w-10 h-10 text-red-500" />
            </div>
            <h2 className="text-2xl font-bold mb-3">Error al cargar reportes</h2>
            <p className="text-muted-foreground max-w-md mb-6">{error}</p>
            <button
              onClick={() => { setError(null); setLoading(true); window.location.reload(); }}
              className="px-6 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg font-medium transition-colors"
            >
              Reintentar
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/20 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="animate-pulse space-y-8">
            <div className="h-8 w-80 bg-slate-200 dark:bg-slate-800 rounded" />
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-1 space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-24 bg-slate-200 dark:bg-slate-800 rounded-xl" />
                ))}
              </div>
              <div className="lg:col-span-2 space-y-4">
                <div className="h-36 bg-slate-200 dark:bg-slate-800 rounded-xl" />
                <div className="h-96 bg-slate-200 dark:bg-slate-800 rounded-xl" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/20 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="w-20 h-20 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center mb-6">
              <X className="w-10 h-10 text-red-500" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Error al cargar reportes</h3>
            <p className="text-muted-foreground max-w-md mb-6">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg transition-colors"
            >
              Reintentar
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/20 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
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

      <div ref={containerRef} className="container mx-auto py-12 px-6 relative z-10">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-6">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 rounded-lg bg-indigo-500/20">
                  <BookOpen className="w-6 h-6 text-indigo-400" />
                </div>
                <span className="text-sm font-medium text-indigo-400/80 uppercase tracking-wider">
                  Reporte
                </span>
              </div>
              <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-indigo-400 via-violet-400 to-indigo-400 bg-clip-text text-transparent">
                Evolución Histórica
              </h1>
              <p className="text-muted-foreground text-lg">
                Seguimiento del rendimiento académico a lo largo de los períodos escolares
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              <ExportButton 
                targetRef={containerRef}
                fileName="reporte-cursos"
                variant="outline"
                size="sm"
                label="Exportar PDF"
              />
              <div className="flex items-center gap-4 px-4 py-2 rounded-full bg-white/80 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 backdrop-blur-sm">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-indigo-400" />
                  <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                    {courses.length} períodos
                  </span>
                </div>
                <div className="w-px h-4 bg-slate-300 dark:bg-slate-600" />
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-violet-400" />
                  <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                    {courses.reduce((sum, c) => sum + c.totalStudents, 0)} estudiantes
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main content - 2 columns */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left sidebar - Year selector */}
          <div className="lg:col-span-4 xl:col-span-3">
            <div className="sticky top-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                  Seleccionar Períodos
                </h3>
                {selectedCourses.length > 0 && (
                  <button
                    onClick={() => setSelectedCourses([])}
                    className="text-xs text-red-400 hover:text-red-300 flex items-center gap-1"
                  >
                    <X className="w-3 h-3" />
                    Limpiar
                  </button>
                )}
              </div>
              
              {/* Quick select buttons */}
              <div className="flex gap-2 mb-4">
                <button
                  onClick={() => setSelectedCourses(courses.map(c => String(c.id)))}
                  className="flex-1 px-3 py-2 text-xs font-medium bg-slate-200/80 hover:bg-slate-300/80 dark:bg-slate-700/50 dark:hover:bg-slate-600 rounded-lg border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-200 transition-colors"
                >
                  Todos
                </button>
                <button
                  onClick={() => {
                    const latestYearCourses = courses.filter(c => c.schoolYear === latestYear);
                    setSelectedCourses(latestYearCourses.map(c => String(c.id)));
                  }}
                  className="flex-1 px-3 py-2 text-xs font-medium bg-indigo-100 hover:bg-indigo-200 dark:bg-indigo-500/20 dark:hover:bg-indigo-500/30 rounded-lg border border-indigo-300 dark:border-indigo-500/30 text-indigo-700 dark:text-indigo-400 transition-colors"
                >
                  Último Año
                </button>
              </div>

              {/* Course multiselect */}
              <CourseMultiSelector
                courses={courses}
                selectedCourses={selectedCourses}
                onSelectionChange={(selected) => setSelectedCourses(selected)}
              />

              {selectedCourses.length > 0 && (
                <div className={cn(
                  "mt-4 p-3 rounded-lg border",
                  "bg-indigo-500/10 border-indigo-500/30",
                  "dark:bg-indigo-500/10 dark:border-indigo-500/30",
                  "light:bg-slate-100/50 light:border-slate-200/50"
                )}>
                  <p className="text-sm text-indigo-400 font-medium">
                    {selectedCourses.length} período{selectedCourses.length > 1 ? 's' : ''} seleccionado{selectedCourses.length > 1 ? 's' : ''}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {selectedCourses.length >= 2 
                      ? `Comparando ${selectedMetrics[0]?.courseName} (${selectedMetrics[0]?.period}) → ${selectedMetrics[selectedMetrics.length - 1]?.courseName} (${selectedMetrics[selectedMetrics.length - 1]?.period})`
                      : 'Selecciona más períodos'}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Right content */}
          <div className="lg:col-span-8 xl:col-span-9">
            {/* Tab Navigation */}
            <div className="flex gap-2 mb-8 p-1 bg-slate-100 dark:bg-slate-900/50 rounded-xl w-fit backdrop-blur-sm border border-slate-200 dark:border-slate-800">
              {[
                { id: 'overview', label: 'Resumen', icon: BarChart3 },
                { id: 'evolution', label: 'Evolución', icon: TrendingUp },
                { id: 'comparison', label: 'Comparación', icon: ArrowRightLeft },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300",
                    activeTab === tab.id 
                      ? "bg-gradient-to-r from-indigo-500 to-violet-500 text-white shadow-lg" 
                      : "text-slate-400 hover:text-white hover:bg-slate-800"
                  )}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Overview Tab */}
            {activeTab === 'overview' && (
              <>
                <section className="mb-8">
                  <SectionHeader 
                    title="Métricas Consolidadas" 
                    subtitle={`Promedio de ${selectedCourses.length} períodos`}
                    icon={Activity}
                    delay={0}
                  />
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div style={{ animationDelay: "100ms" }} className="animate-fade-in-up">
                      <MetricCard
                        title="Períodos"
                        value={selectedCourses.length}
                        icon={<Calendar className="h-5 w-5" />}
                        description="Seleccionados"
                        variant="default"
                      />
                    </div>
                    <div style={{ animationDelay: "150ms" }} className="animate-fade-in-up">
                      <MetricCard
                        title="Estudiantes"
                        value={selectedCourses.reduce((sum, id) => sum + (courses.find(c => c.id === id)?.totalStudents || 0), 0)}
                        icon={<Users className="h-5 w-5" />}
                        description="En seleccionados"
                        variant="default"
                      />
                    </div>
                    <div style={{ animationDelay: "200ms" }} className="animate-fade-in-up">
                      <MetricCard
                        title="Completación"
                        value={`${Math.round(selectedMetrics.reduce((sum, m) => sum + m.completionRate, 0) / (selectedMetrics.length || 1))}%`}
                        icon={<CheckCircle2 className="h-5 w-5" />}
                        description="Promedio"
                        variant="highlight"
                      />
                    </div>
                    <div style={{ animationDelay: "250ms" }} className="animate-fade-in-up">
                      <MetricCard
                        title="Calificación"
                        value={`${Math.round(selectedMetrics.reduce((sum, m) => sum + m.averageGrade, 0) / (selectedMetrics.length || 1))}%`}
                        icon={<Target className="h-5 w-5" />}
                        description="Promedio"
                        variant="accent"
                      />
                    </div>
                  </div>
                </section>

                {/* Course highlights - actionable insights */}
                {kpis?.topPerformingCourse && kpis?.needsAttentionCourse && (
                  <section className="mb-8">
                    <SectionHeader 
                      title="Cursos Destacados" 
                      subtitle="Rendimiento comparativo entre cursos"
                      icon={Award}
                      delay={250}
                      accentColor="amber"
                    />
                    <CourseHighlightCards 
                      topCourse={kpis.topPerformingCourse}
                      attentionCourse={kpis.needsAttentionCourse}
                    />
                  </section>
                )}

                {evolutionData && (
                  <section className="mb-8">
                    <SectionHeader 
                      title="Evolución Total" 
                      subtitle={`${selectedMetrics[0]?.courseName} (${selectedMetrics[0]?.period}) → ${selectedMetrics[selectedMetrics.length - 1]?.courseName} (${selectedMetrics[selectedMetrics.length - 1]?.period})`}
                      icon={TrendingUp}
                      delay={300}
                      accentColor="violet"
                    />
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                       <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-4 text-center">
                         <p className="text-xs text-muted-foreground mb-1">Progreso</p>
                        <p className={cn("text-2xl font-bold", evolutionData.progressDiff >= 0 ? "text-indigo-400" : "text-red-400")}>
                          {evolutionData.progressDiff > 0 ? '+' : ''}{evolutionData.progressDiff.toFixed(1)}%
                        </p>
                      </div>
                       <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-4 text-center">
                         <p className="text-xs text-muted-foreground mb-1">Calificación</p>
                        <p className={cn("text-2xl font-bold", evolutionData.gradeDiff >= 0 ? "text-indigo-400" : "text-red-400")}>
                          {evolutionData.gradeDiff > 0 ? '+' : ''}{evolutionData.gradeDiff.toFixed(1)}%
                        </p>
                      </div>
                       <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-4 text-center">
                         <p className="text-xs text-muted-foreground mb-1">Completación</p>
                        <p className={cn("text-2xl font-bold", evolutionData.completionDiff >= 0 ? "text-indigo-400" : "text-red-400")}>
                          {evolutionData.completionDiff > 0 ? '+' : ''}{evolutionData.completionDiff.toFixed(1)}%
                        </p>
                      </div>
                       <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-4 text-center">
                         <p className="text-xs text-muted-foreground mb-1">Tiempo</p>
                         <p className="text-2xl font-bold text-violet-400">{formatPlayTime(evolutionData.timeDiff)}</p>
                      </div>
                    </div>
                  </section>
                )}

                <section className="mb-8">
                  <SectionHeader 
                    title="Rendimiento por Período" 
                    icon={Award}
                    delay={500}
                  />
                   <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 overflow-hidden">
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                           <tr className="border-b border-slate-200 dark:border-slate-800">
                              <th className="text-left p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Curso</th>
                              <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Período</th>
                              <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Año</th>
                              <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Est.</th>
                             <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Prog.</th>
                              <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Calif.</th>
                              <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">vs Ant.</th>
                              <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Tasa</th>
                              <th className="text-center p-3 text-xs font-semibold text-slate-600 dark:text-slate-300">Tendencia</th>
                           </tr>
                        </thead>
                        <tbody>
                            {selectedMetrics.map((metric) => (
                              <tr 
                                key={metric.courseId}
                                onClick={() => window.location.href = `/dashboard/courses/${metric.courseId}`}
                                className="border-b border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50 cursor-pointer transition-colors"
                              >
                                <td className="p-3 font-medium text-sm">
                                  <Link 
                                    href={`/dashboard/courses/${metric.courseId}`}
                                    className="text-indigo-500 hover:text-indigo-400 hover:underline underline-offset-2"
                                    onClick={(e) => e.stopPropagation()}
                                  >
                                    {metric.courseName || metric.course_name || '—'}
                                  </Link>
                                </td>
                                <td className="p-3 text-center text-sm text-muted-foreground">{metric.period}</td>
                                <td className="p-3 text-center text-xs text-muted-foreground">{metric.schoolYear}</td>
                               <td className="p-3 text-center">{metric.totalStudents || 0}</td>
                              <td className="p-3 text-center font-semibold">{metric.averageProgress}%</td>
                              <td className="p-3 text-center">
                                <span className={cn("font-bold", metric.averageGrade >= 80 ? "text-indigo-400" : metric.averageGrade >= 60 ? "text-amber-400" : "text-red-400")}>
                                  {metric.averageGrade}%
                                </span>
                              </td>
                              <td className="p-3 text-center">
                                {(() => {
                                  const index = selectedMetrics.indexOf(metric);
                                  const prev = getPreviousMetric(selectedMetrics, index);
                                  if (!prev) return <span className="text-xs text-slate-500">—</span>;
                                  const diff = metric.averageGrade - prev.averageGrade;
                                  return (
                                    <span className={cn("inline-flex items-center gap-0.5 text-xs font-semibold", diff >= 0 ? "text-emerald-400" : "text-red-400")}>
                                      {diff >= 0 ? '+' : ''}{diff.toFixed(1)}%
                                    </span>
                                  );
                                })()}
                              </td>
                              <td className="p-3">
                                <div className="flex justify-center">
                                   <div className="w-16 h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                    <div className="h-full bg-gradient-to-r from-indigo-500 to-violet-500" style={{ width: `${metric.completionRate}%` }} />
                                  </div>
                                </div>
                              </td>
                              <td className="p-3 text-center">
                                {metric.progressTrend !== 0 && <ComparisonBadge trend={metric.progressTrend} />}
                                {metric.progressTrend === 0 && <span className="text-xs text-slate-500">—</span>}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </section>
              </>
            )}

            {/* Evolution Tab */}
            {activeTab === 'evolution' && selectedMetrics.length >= 2 && (
              <section className="mb-8">
                <SectionHeader 
                  title="Análisis de Evolución" 
                  icon={TrendingUp}
                  delay={0}
                  accentColor="violet"
                />
                 
                  <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-6 mb-6">
                    <h3 className="text-lg font-semibold mb-6">Progreso y Calificación<ChartHelp content="Muestra la evolución del progreso y calificación promedio entre períodos. Útil para comparar el rendimiento general de los cursos seleccionados." /></h3>
                    <LineChartComponent
                       data={selectedMetrics.map(m => ({ date: `${m.courseName}\n${m.period || ''}`, averageProgress: m.averageProgress, averageGrade: m.averageGrade }))}
                      xAxisDataKey="date"
                      lines={[
                        { dataKey: "averageProgress", name: "Progreso", color: "#10B981" },
                        { dataKey: "averageGrade", name: "Calificación", color: "#06B6D4" },
                      ]}
                      title=""
                      subtitle=""
                      yAxisLabel="%"
                      height={300}
                    />
                  </div>

                   <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-6">
                     <h3 className="text-lg font-semibold mb-6">Completación y Engagement<ChartHelp content="Analiza la tasa de completación y sesiones promedio por estudiante. Ayuda a identificar si los estudiantes finalizan los cursos y con qué frecuencia participan." /></h3>
                    <LineChartComponent
                      data={selectedMetrics.map(m => ({ date: `${m.courseName}\n${m.period || ''}`, completionRate: m.completionRate, sessionsPerStudent: m.averageSessionsPerStudent }))}
                     xAxisDataKey="date"
                     lines={[
                       { dataKey: "completionRate", name: "Tasa Completación", color: "#F59E0B" },
                       { dataKey: "sessionsPerStudent", name: "Sesiones Promedio", color: "#8B5CF6" },
                     ]}
                     title=""
                     subtitle=""
                     yAxisLabel="Valor"
                     height={300}
                   />
                 </div>
               </section>
            )}

            {/* Time-series progress chart using real progress-over-time data */}
            {activeTab === 'evolution' && selectedCourses.length > 0 && (
              (() => {
                const courseWithData = selectedCourses.find(id => (progressData[id]?.length ?? 0) > 0);
                if (!courseWithData) return null;
                const timeSeriesData = progressData[courseWithData] ?? [];
                if (timeSeriesData.length < 2) return null;
                return (
                  <section className="mb-8">
                    <SectionHeader 
                      title="Progreso Diario" 
                      subtitle={`${timeSeriesData.length} puntos de datos — ${timeSeriesData[0]?.date ?? ''} → ${timeSeriesData[timeSeriesData.length - 1]?.date ?? ''}`}
                      icon={Activity}
                      delay={600}
                      accentColor="violet"
                    />
                    <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-6">
                      <h3 className="text-lg font-semibold mb-6">Progreso y Calificación en el Tiempo<ChartHelp content="Muestra la evolución diaria del progreso y calificación. Útil para detectar tendencias a corto plazo y el impacto de intervenciones educativas." /></h3>
                      <LineChartComponent
                        data={timeSeriesData}
                        xAxisDataKey="date"
                        lines={[
                          { dataKey: "averageProgress", name: "Progreso", color: "#10B981" },
                          { dataKey: "averageGrade", name: "Calificación", color: "#06B6D4" },
                        ]}
                        title=""
                        subtitle=""
                        yAxisLabel="%"
                        height={300}
                      />
                    </div>
                  </section>
                );
              })()
            )}

            {activeTab === 'evolution' && selectedMetrics.length === 1 && (
              <div className="flex flex-col items-center justify-center py-20 text-center">
                <div className="w-20 h-20 rounded-full bg-slate-100 dark:bg-slate-800/50 flex items-center justify-center mb-6">
                  <TrendingUp className="w-10 h-10 text-slate-500 dark:text-slate-400" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Selecciona al menos 2 cursos o períodos</h3>
                <p className="text-muted-foreground max-w-md">
                  Los gráficos de evolución necesitan al menos 2 puntos de datos para mostrar tendencias.
                  Seleccioná más cursos del panel izquierdo.
                </p>
              </div>
            )}

            {/* Comparison Tab */}
            {activeTab === 'comparison' && selectedMetrics.length >= 2 && (
              <section className="mb-8">
                <SectionHeader 
                  title="Comparación de Períodos" 
                  subtitle={`${selectedMetrics.length} períodos`}
                  icon={ArrowRightLeft}
                  delay={0}
                  accentColor="amber"
                />
                 
                  <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-6 mb-6">
                    <h3 className="text-lg font-semibold mb-6">Métricas Comparadas<ChartHelp content="Compara progreso, calificación y completación entre distintos cursos o períodos. Las barras agrupadas facilitan la comparación visual directa." /></h3>
                   <BarChart
                      data={selectedMetrics.map(m => ({ name: `${m.courseName}\n${m.period || ''}`, Progreso: m.averageProgress, Calificación: m.averageGrade, Completación: m.completionRate }))}
                     xAxisDataKey="name"
                    bars={[
                      { dataKey: "Progreso", name: "Progreso", color: "#10B981" },
                      { dataKey: "Calificación", name: "Calificación", color: "#06B6D4" },
                      { dataKey: "Completación", name: "Completación", color: "#F59E0B" },
                    ]}
                    title=""
                    subtitle=""
                    yAxisLabel="%"
                    height={350}
                  />
                </div>

                <div className="grid grid-cols-1 gap-6">
                   <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-6">
                     <h3 className="text-lg font-semibold mb-4">Distribución por Período<ChartHelp content="Muestra cómo se distribuyen los estudiantes en niveles de rendimiento (alto, medio, bajo) para cada período. Útil para ver cambios en la composición del rendimiento." /></h3>
                     <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {selectedMetrics.map((metric) => (
                        <div key={`dist-${metric.courseId}`}>
                          <p className="text-sm font-medium text-center mb-2 text-muted-foreground">
                            {metric.courseName} — {metric.period}
                          </p>
                          <DonutChart
                            data={[
                              { name: 'Alto', value: metric.highPerformers || 0 },
                              { name: 'Medio', value: metric.mediumPerformers || 0 },
                              { name: 'Bajo', value: metric.lowPerformers || 0 },
                            ]}
                            title=""
                            subtitle=""
                            height={200}
                            innerRadius={40}
                            outerRadius={70}
                          />
                        </div>
                      ))}
                    </div>
                  </div>

                   <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 p-6">
                     <h3 className="text-lg font-semibold mb-4">Tendencias</h3>
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {selectedMetrics.slice(1).map((metric) => (
                         <div key={metric.courseId} className="p-3 rounded-lg bg-slate-100 dark:bg-slate-800/30 border border-slate-200 dark:border-slate-700/30">
                           <p className="text-xs font-medium mb-1">{metric.courseName} — {metric.period}</p>
                          <div className="flex gap-4 text-xs">
                            <span className="text-muted-foreground">Prog: <TrendArrow value={metric.progressTrend} /></span>
                            <span className="text-muted-foreground">Calif: <TrendArrow value={metric.gradeTrend} /></span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </section>
            )}

            {activeTab === 'comparison' && selectedMetrics.length < 2 && (
              <div className="flex flex-col items-center justify-center py-20 text-center">
                <div className="w-20 h-20 rounded-full bg-slate-100 dark:bg-slate-800/50 flex items-center justify-center mb-6">
                  <ArrowRightLeft className="w-10 h-10 text-slate-500 dark:text-slate-400" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Selecciona al menos 2 cursos o períodos</h3>
                <p className="text-muted-foreground max-w-md mb-4">
                  Usa el panel izquierdo para seleccionar múltiples cursos del mismo o diferente año escolar.
                  Podrás comparar sus métricas lado a lado, ver distribuciones de rendimiento y tendencias.
                </p>
                <button
                  onClick={() => setActiveTab('overview')}
                  className="text-sm text-indigo-400 hover:text-indigo-300 underline underline-offset-2"
                >
                  Volver a Resumen
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="text-center py-8 border-t border-slate-200 dark:border-slate-800 mt-8">
          <p className="text-sm text-muted-foreground">
            📊 Reporte de {subjectName} • Hello World Platform
          </p>
        </div>
      </div>
    </div>
  );
}
