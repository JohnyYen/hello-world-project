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
import { ExportButton } from '@/components/export/ExportButton';
import { CourseMultiSelector } from '@/components/reports/course-multi-selector';
import { cn } from '@/lib/utils';
import { courseReportsService, apiClient } from '@/lib/api-client';
import type { Course, CourseMetrics, CourseReportKPIs, CourseProgressOverTime } from '@/types/course-report.interface';

// Utility functions
function formatPlayTime(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  if (hours > 0) {
    return `${hours}h`;
  }
  return `${minutes}m`;
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
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);
  const [selectedMetrics, setSelectedMetrics] = useState<CourseMetrics[]>([]);
  const [kpis, setKpis] = useState<CourseReportKPIs | null>(null);
  const [progressData, setProgressData] = useState<Record<string, CourseProgressOverTime[]>>({});
  const [activeTab, setActiveTab] = useState('overview');

  const latestYear = useMemo(() => {
    if (courses.length === 0) return '';
    const sorted = [...courses].sort((a, b) => b.schoolYear.localeCompare(a.schoolYear));
    return sorted[0].schoolYear;
  }, [courses]);

  const subjectName = useMemo(() => {
    return courses.length > 0 ? courses[0].name : 'Matemáticas I';
  }, [courses]);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [coursesResponse, kpisResponse] = await Promise.all([
          courseReportsService.getCourses(),
          courseReportsService.getReportKPIs()
        ]);

        const coursesData = coursesResponse.data || [];
        const kpisData = kpisResponse.data || null;

        setCourses(coursesData);
        setKpis(kpisData);

        // Select latest year by default
        if (coursesData.length > 0) {
          const sorted = [...coursesData].sort((a, b) => b.schoolYear.localeCompare(a.schoolYear));
          const latestSchoolYear = sorted[0].schoolYear;
          const latestYearCourses = coursesData.filter(c => c.schoolYear === latestSchoolYear);
          setSelectedCourses(latestYearCourses.map(c => String(c.id)));
        }
      } catch (error) {
        console.error('Error loading reports data:', error);
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

        const metrics = metricsResponse.data || [];
        const sortedMetrics = [...metrics].sort((a, b) => {
          if (a.schoolYear === b.schoolYear) {
            return a.period.localeCompare(b.period);
          }
          return a.schoolYear.localeCompare(b.schoolYear);
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
      } catch (error) {
        if (!cancelled && !(error instanceof DOMException && error.name === 'AbortError')) {
          console.error('Error loading selected metrics:', error);
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="animate-pulse space-y-8">
            <div className="h-8 w-80 bg-slate-800 rounded" />
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-1 space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-24 bg-slate-800 rounded-xl" />
                ))}
              </div>
              <div className="lg:col-span-2 space-y-4">
                <div className="h-36 bg-slate-800 rounded-xl" />
                <div className="h-96 bg-slate-800 rounded-xl" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950/20">
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
                  {subjectName}
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
              <div className="flex items-center gap-4 px-4 py-2 rounded-full bg-slate-800/80 border border-slate-700 backdrop-blur-sm">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-indigo-400" />
                  <span className="text-sm font-medium text-slate-300">
                    {courses.length} períodos
                  </span>
                </div>
                <div className="w-px h-4 bg-slate-600" />
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-violet-400" />
                  <span className="text-sm font-medium text-slate-300">
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
                  className="flex-1 px-3 py-2 text-xs font-medium bg-slate-800/50 hover:bg-slate-700 rounded-lg border border-slate-700 transition-colors"
                >
                  Todos
                </button>
                <button
                  onClick={() => {
                    const latestYearCourses = courses.filter(c => c.schoolYear === latestYear);
                    setSelectedCourses(latestYearCourses.map(c => String(c.id)));
                  }}
                  className="flex-1 px-3 py-2 text-xs font-medium bg-indigo-500/20 hover:bg-indigo-500/30 rounded-lg border border-indigo-500/30 text-indigo-400 transition-colors"
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
                <div className="mt-4 p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/30">
                  <p className="text-sm text-indigo-400 font-medium">
                    {selectedCourses.length} período{selectedCourses.length > 1 ? 's' : ''} seleccionado{selectedCourses.length > 1 ? 's' : ''}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {selectedCourses.length >= 2 
                      ? `Comparando ${selectedMetrics[0]?.period} → ${selectedMetrics[selectedMetrics.length - 1]?.period}`
                      : 'Selecciona más períodos'}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Right content */}
          <div className="lg:col-span-8 xl:col-span-9">
            {/* Tab Navigation */}
            <div className="flex gap-2 mb-8 p-1 bg-slate-900/50 rounded-xl w-fit backdrop-blur-sm">
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

                {evolutionData && (
                  <section className="mb-8">
                    <SectionHeader 
                      title="Evolución Total" 
                      subtitle={`Desde ${selectedMetrics[0]?.period} hasta ${selectedMetrics[selectedMetrics.length - 1]?.period}`}
                      icon={TrendingUp}
                      delay={300}
                      accentColor="violet"
                    />
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-4 text-center">
                        <p className="text-xs text-muted-foreground mb-1">Progreso</p>
                        <p className={cn("text-2xl font-bold", evolutionData.progressDiff >= 0 ? "text-indigo-400" : "text-red-400")}>
                          {evolutionData.progressDiff > 0 ? '+' : ''}{evolutionData.progressDiff.toFixed(1)}%
                        </p>
                      </div>
                      <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-4 text-center">
                        <p className="text-xs text-muted-foreground mb-1">Calificación</p>
                        <p className={cn("text-2xl font-bold", evolutionData.gradeDiff >= 0 ? "text-indigo-400" : "text-red-400")}>
                          {evolutionData.gradeDiff > 0 ? '+' : ''}{evolutionData.gradeDiff.toFixed(1)}%
                        </p>
                      </div>
                      <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-4 text-center">
                        <p className="text-xs text-muted-foreground mb-1">Completación</p>
                        <p className={cn("text-2xl font-bold", evolutionData.completionDiff >= 0 ? "text-indigo-400" : "text-red-400")}>
                          {evolutionData.completionDiff > 0 ? '+' : ''}{evolutionData.completionDiff.toFixed(1)}%
                        </p>
                      </div>
                      <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-4 text-center">
                        <p className="text-xs text-muted-foreground mb-1">Tiempo</p>
                        <p className="text-2xl font-bold text-violet-400">+{formatPlayTime(evolutionData.timeDiff)}</p>
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
                  <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 overflow-hidden">
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="border-b border-slate-700/50">
                            <th className="text-left p-3 text-xs font-semibold text-slate-400">Período</th>
                            <th className="text-center p-3 text-xs font-semibold text-slate-400">Año</th>
                            <th className="text-center p-3 text-xs font-semibold text-slate-400">Est.</th>
                            <th className="text-center p-3 text-xs font-semibold text-slate-400">Prog.</th>
                            <th className="text-center p-3 text-xs font-semibold text-slate-400">Calif.</th>
                            <th className="text-center p-3 text-xs font-semibold text-slate-400">Tasa</th>
                            <th className="text-center p-3 text-xs font-semibold text-slate-400">Tendencia</th>
                          </tr>
                        </thead>
                        <tbody>
                          {selectedMetrics.map((metric) => (
                            <tr 
                              key={metric.courseId}
                              className="border-b border-slate-700/30 hover:bg-slate-800/50"
                            >
                              <td className="p-3 font-medium text-sm">{metric.period}</td>
                              <td className="p-3 text-center text-xs text-muted-foreground">{metric.schoolYear}</td>
                              <td className="p-3 text-center">{courses.find(c => c.id === metric.courseId)?.totalStudents || 0}</td>
                              <td className="p-3 text-center font-semibold">{metric.averageProgress}%</td>
                              <td className="p-3 text-center">
                                <span className={cn("font-bold", metric.averageGrade >= 80 ? "text-indigo-400" : metric.averageGrade >= 60 ? "text-amber-400" : "text-red-400")}>
                                  {metric.averageGrade}%
                                </span>
                              </td>
                              <td className="p-3">
                                <div className="flex justify-center">
                                  <div className="w-16 h-1.5 bg-slate-700 rounded-full overflow-hidden">
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
            {activeTab === 'evolution' && selectedMetrics.length > 0 && (
              <section className="mb-8">
                <SectionHeader 
                  title="Análisis de Evolución" 
                  icon={TrendingUp}
                  delay={0}
                  accentColor="violet"
                />
                
                <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-6 mb-6">
                  <h3 className="text-lg font-semibold mb-6">Progreso y Calificación</h3>
                  <LineChartComponent
                    data={selectedMetrics.map(m => ({ date: m.period.replace(' - ', '\n'), averageProgress: m.averageProgress, averageGrade: m.averageGrade }))}
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

                <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-6">
                  <h3 className="text-lg font-semibold mb-6">Completación y Engagement</h3>
                  <LineChartComponent
                    data={selectedMetrics.map(m => ({ date: m.period.replace(' - ', '\n'), completionRate: m.completionRate, sessionsPerStudent: m.averageSessionsPerStudent * 2 }))}
                    xAxisDataKey="date"
                    lines={[
                      { dataKey: "completionRate", name: "Tasa Completación", color: "#F59E0B" },
                      { dataKey: "sessionsPerStudent", name: "Sesiones (x2)", color: "#8B5CF6" },
                    ]}
                    title=""
                    subtitle=""
                    yAxisLabel="Valor"
                    height={300}
                  />
                </div>
              </section>
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
                
                <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-6 mb-6">
                  <h3 className="text-lg font-semibold mb-6">Métricas Comparadas</h3>
                  <BarChart
                    data={selectedMetrics.map(m => ({ name: m.period.replace(' - ', '\n'), Progreso: m.averageProgress, Calificación: m.averageGrade, Completación: m.completionRate }))}
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

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-6">
                    <h3 className="text-lg font-semibold mb-4">Distribución</h3>
                    <DonutChart
                      data={[
                        { name: 'Alto', value: selectedMetrics[selectedMetrics.length - 1]?.highPerformers || 0 },
                        { name: 'Medio', value: selectedMetrics[selectedMetrics.length - 1]?.mediumPerformers || 0 },
                        { name: 'Bajo', value: selectedMetrics[selectedMetrics.length - 1]?.lowPerformers || 0 },
                      ]}
                      title=""
                      subtitle=""
                      height={250}
                    />
                  </div>

                  <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 p-6">
                    <h3 className="text-lg font-semibold mb-4">Tendencias</h3>
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {selectedMetrics.slice(1).map((metric) => (
                        <div key={metric.courseId} className="p-3 rounded-lg bg-slate-800/30 border border-slate-700/30">
                          <p className="text-xs font-medium mb-1">{metric.period}</p>
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
                <div className="w-20 h-20 rounded-full bg-slate-800/50 flex items-center justify-center mb-6">
                  <ArrowRightLeft className="w-10 h-10 text-slate-500" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Selecciona al menos 2 períodos</h3>
                <p className="text-muted-foreground max-w-md">
                  Usa el selector de la izquierda para elegir períodos a comparar.
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="text-center py-8 border-t border-slate-800 mt-8">
          <p className="text-sm text-muted-foreground">
            📊 Reporte de {subjectName} • Hello World Platform
          </p>
        </div>
      </div>
    </div>
  );
}
