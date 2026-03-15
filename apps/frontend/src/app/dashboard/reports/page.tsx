'use client';

import { useState, useEffect, useMemo } from 'react';
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
  Check,
  X,
} from 'lucide-react';
import { MetricCard, LineChart as LineChartComponent, BarChart, DonutChart } from '@/components/charts';
import { cn } from '@/lib/utils';
import { 
  getCourses, 
  getSelectedCourseMetrics, 
  getCourseProgressOverTime,
  getReportKPIs 
} from '@/components/reports/course-report-data';
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
  accentColor = 'emerald'
}: { 
  title: string; 
  subtitle?: string; 
  icon?: React.ElementType; 
  delay?: number;
  accentColor?: 'emerald' | 'cyan' | 'amber';
}) {
  const colorClasses = {
    emerald: 'border-emerald-500 dark:border-emerald-400 text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/50',
    cyan: 'border-cyan-500 dark:border-cyan-400 text-cyan-600 dark:text-cyan-400 bg-cyan-100 dark:bg-cyan-900/50',
    amber: 'border-amber-500 dark:border-amber-400 text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/50',
  };

  return (
    <div 
      className="relative mb-8 pl-4 border-l-4 border-emerald-500 dark:border-emerald-400"
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

// Year chip selector
function YearChip({ 
  course, 
  isSelected, 
  onClick,
  isLatest = false
}: { 
  course: Course & { progressTrend?: number }; 
  isSelected: boolean; 
  onClick: () => void;
  isLatest?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "relative flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300",
        "border backdrop-blur-sm min-w-[180px]",
        isSelected 
          ? "bg-gradient-to-r from-emerald-500 to-cyan-500 text-white border-transparent shadow-lg shadow-emerald-500/25" 
          : "bg-slate-100 dark:bg-slate-800/60 border-slate-200 dark:border-slate-700 hover:border-emerald-400 dark:hover:border-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/20"
      )}
    >
      <div className={cn(
        "w-5 h-5 rounded border flex items-center justify-center transition-colors",
        isSelected 
          ? "bg-white/20 border-white/40" 
          : "border-slate-400"
      )}>
        {isSelected && <Check className="w-3 h-3 text-white" />}
      </div>
      <div className="text-left">
        <span className="block font-semibold">{course.schoolYear}</span>
        <span className={cn(
          "block text-xs",
          isSelected ? "text-white/70" : "text-muted-foreground"
        )}>
          {course.totalStudents} estudiantes
        </span>
      </div>
      {isLatest && !isSelected && (
        <span className="absolute -top-2 -right-2 px-2 py-0.5 text-[10px] font-bold bg-amber-500 text-white rounded-full shadow-lg">
          ACTUAL
        </span>
      )}
      {isSelected && (
        <span className="absolute -top-2 -right-2 px-2 py-0.5 text-[10px] font-bold bg-white/20 text-white rounded-full">
          ACTUAL
        </span>
      )}
    </button>
  );
}

// Comparison badge
function ComparisonBadge({ trend }: { trend: number }) {
  const isPositive = trend >= 0;
  return (
    <span className={cn(
      "inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold",
      isPositive 
        ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400" 
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
    <span className={cn(
      "inline-flex items-center",
      isPositive ? "text-emerald-400" : "text-red-400"
    )}>
      {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
      <span className="ml-1 font-semibold">{Math.abs(value).toFixed(1)}%</span>
    </span>
  );
}

// Main component
export default function ReportsPage() {
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);
  const [selectedMetrics, setSelectedMetrics] = useState<CourseMetrics[]>([]);
  const [kpis, setKpis] = useState<CourseReportKPIs | null>(null);
  const [progressData, setProgressData] = useState<Record<string, CourseProgressOverTime[]>>({});
  const [activeTab, setActiveTab] = useState('overview');

  // Get latest year
  const latestYear = useMemo(() => {
    if (courses.length === 0) return '';
    return courses[courses.length - 1].schoolYear;
  }, [courses]);

  // Get subject name
  const subjectName = useMemo(() => {
    return courses.length > 0 ? courses[0].name : 'Matemáticas I';
  }, [courses]);

  // Sort courses by year
  const sortedCourses = useMemo(() => {
    return [...courses].sort((a, b) => a.schoolYear.localeCompare(b.schoolYear));
  }, [courses]);

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [coursesData, kpisData] = await Promise.all([
          getCourses(),
          getReportKPIs()
        ]);
        
        setCourses(coursesData);
        setKpis(kpisData);
        
        // Select latest 3 years by default for trend analysis
        if (coursesData.length > 0) {
          const sorted = [...coursesData].sort((a, b) => b.schoolYear.localeCompare(a.schoolYear));
          const latest = sorted.slice(0, 3);
          setSelectedCourses(latest.map(c => c.id));
        }
      } catch (error) {
        console.error('Error loading reports data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadInitialData();
  }, []);

  // Load selected course metrics
  useEffect(() => {
    const loadSelectedMetrics = async () => {
      if (selectedCourses.length === 0) {
        setSelectedMetrics([]);
        return;
      }

      try {
        const metrics = await getSelectedCourseMetrics(selectedCourses);
        
        // Sort chronologically
        const sortedMetrics = [...metrics].sort((a, b) => 
          a.schoolYear.localeCompare(b.schoolYear)
        );
        
        setSelectedMetrics(sortedMetrics);

        // Load progress data
        const progressPromises = selectedCourses.map(async (courseId) => {
          const data = await getCourseProgressOverTime(courseId);
          return { courseId, data };
        });

        const progressResults = await Promise.all(progressPromises);
        const progressMap: Record<string, CourseProgressOverTime[]> = {};
        progressResults.forEach(({ courseId, data }) => {
          progressMap[courseId] = data;
        });
        setProgressData(progressMap);
      } catch (error) {
        console.error('Error loading selected metrics:', error);
      }
    };

    loadSelectedMetrics();
  }, [selectedCourses]);

  const toggleCourse = (courseId: string) => {
    setSelectedCourses(prev => 
      prev.includes(courseId) 
        ? prev.filter(id => id !== courseId)
        : [...prev, courseId]
    );
  };

  // Calculate evolution
  const evolutionData = useMemo(() => {
    if (selectedMetrics.length < 2) return null;
    
    const first = selectedMetrics[0];
    const last = selectedMetrics[selectedMetrics.length - 1];
    
    return {
      progressDiff: last.averageProgress - first.averageProgress,
      gradeDiff: last.averageGrade - first.averageGrade,
      completionDiff: last.completionRate - first.completionRate,
      timeDiff: last.averageActiveTime - first.averageActiveTime,
      yearsCompared: selectedMetrics.length,
    };
  }, [selectedMetrics]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="animate-pulse space-y-8">
            <div className="h-8 w-80 bg-slate-800 rounded" />
            <div className="flex gap-3 flex-wrap">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-14 w-40 bg-slate-800 rounded-xl" />
              ))}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-36 bg-slate-800 rounded-xl" />
              ))}
            </div>
            <div className="h-96 bg-slate-800 rounded-xl" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950/20">
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

      <div className="container mx-auto py-12 px-6 relative z-10">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-6">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 rounded-lg bg-emerald-500/20">
                  <BookOpen className="w-6 h-6 text-emerald-400" />
                </div>
                <span className="text-sm font-medium text-emerald-400/80 uppercase tracking-wider">
                  {subjectName}
                </span>
              </div>
              <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-emerald-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">
                Evolución Histórica
              </h1>
              <p className="text-muted-foreground text-lg">
                Seguimiento del rendimiento académico año tras año
              </p>
            </div>
            
            {/* Summary badge */}
            <div className="flex items-center gap-4 px-4 py-2 rounded-full bg-slate-800/80 border border-slate-700 backdrop-blur-sm">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-emerald-400" />
                <span className="text-sm font-medium text-slate-300">
                  {courses.length} años escolares
                </span>
              </div>
              <div className="w-px h-4 bg-slate-600" />
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-cyan-400" />
                <span className="text-sm font-medium text-slate-300">
                  {courses.reduce((sum, c) => sum + c.totalStudents, 0)} estudiantes
                </span>
              </div>
            </div>
          </div>

          {/* Year selector */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <ArrowRightLeft className="w-4 h-4" />
                <span>Selecciona los años a comparar:</span>
                <span className="font-medium text-emerald-400">{selectedCourses.length} seleccionados</span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setSelectedCourses(sortedCourses.map(c => c.id))}
                  className="px-3 py-1.5 text-xs font-medium bg-slate-800/50 hover:bg-slate-700 rounded-lg border border-slate-700 transition-colors"
                >
                  Todos
                </button>
                <button
                  onClick={() => setSelectedCourses([])}
                  className="px-3 py-1.5 text-xs font-medium bg-slate-800/50 hover:bg-red-900/30 rounded-lg border border-slate-700 hover:border-red-700 text-slate-400 hover:text-red-400 transition-colors"
                >
                  Limpiar
                </button>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-3">
              {sortedCourses.map((course) => {
                const metric = selectedMetrics.find(m => m.id === course.id);
                return (
                  <YearChip
                    key={course.id}
                    course={{ ...course, progressTrend: metric?.progressTrend }}
                    isSelected={selectedCourses.includes(course.id)}
                    onClick={() => toggleCourse(course.id)}
                    isLatest={course.schoolYear === latestYear}
                  />
                );
              })}
            </div>
          </div>
        </div>

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
                  ? "bg-gradient-to-r from-emerald-500 to-cyan-500 text-white shadow-lg" 
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
            {/* KPIs */}
            <section className="mb-8">
              <SectionHeader 
                title="Métricas Consolidadas" 
                subtitle={`Promedio de ${selectedCourses.length} años seleccionados`}
                icon={Activity}
                delay={0}
              />
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div style={{ animationDelay: "100ms" }} className="animate-fade-in-up">
                  <MetricCard
                    title="Años Escolares"
                    value={selectedCourses.length}
                    icon={<Calendar className="h-5 w-5" />}
                    description="Seleccionados"
                    variant="default"
                  />
                </div>
                <div style={{ animationDelay: "150ms" }} className="animate-fade-in-up">
                  <MetricCard
                    title="Total Estudiantes"
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

            {/* Evolution Summary */}
            {evolutionData && (
              <section className="mb-8">
                <SectionHeader 
                  title="Evolución Total" 
                  subtitle={`De ${selectedMetrics[0]?.schoolYear} a ${selectedMetrics[selectedMetrics.length - 1]?.schoolYear}`}
                  icon={TrendingUp}
                  delay={300}
                  accentColor="cyan"
                />
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-4 text-center">
                    <p className="text-xs text-muted-foreground mb-1">Progreso</p>
                    <p className={cn("text-2xl font-bold", evolutionData.progressDiff >= 0 ? "text-emerald-400" : "text-red-400")}>
                      {evolutionData.progressDiff > 0 ? '+' : ''}{evolutionData.progressDiff.toFixed(1)}%
                    </p>
                  </div>
                  <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-4 text-center">
                    <p className="text-xs text-muted-foreground mb-1">Calificación</p>
                    <p className={cn("text-2xl font-bold", evolutionData.gradeDiff >= 0 ? "text-emerald-400" : "text-red-400")}>
                      {evolutionData.gradeDiff > 0 ? '+' : ''}{evolutionData.gradeDiff.toFixed(1)}%
                    </p>
                  </div>
                  <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-4 text-center">
                    <p className="text-xs text-muted-foreground mb-1">Completación</p>
                    <p className={cn("text-2xl font-bold", evolutionData.completionDiff >= 0 ? "text-emerald-400" : "text-red-400")}>
                      {evolutionData.completionDiff > 0 ? '+' : ''}{evolutionData.completionDiff.toFixed(1)}%
                    </p>
                  </div>
                  <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-4 text-center">
                    <p className="text-xs text-muted-foreground mb-1">Tiempo</p>
                    <p className="text-2xl font-bold text-cyan-400">
                      +{formatPlayTime(evolutionData.timeDiff)}
                    </p>
                  </div>
                </div>
              </section>
            )}

            {/* Table */}
            <section className="mb-8">
              <SectionHeader 
                title="Rendimiento por Año" 
                subtitle="Métricas de cada año escolar"
                icon={Award}
                delay={500}
              />
              <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-700/50">
                        <th className="text-left p-3 text-xs font-semibold text-slate-400">Año Escolar</th>
                        <th className="text-center p-3 text-xs font-semibold text-slate-400">Est.</th>
                        <th className="text-center p-3 text-xs font-semibold text-slate-400">Progreso</th>
                        <th className="text-center p-3 text-xs font-semibold text-slate-400">Calif.</th>
                        <th className="text-center p-3 text-xs font-semibold text-slate-400">Tasa</th>
                        <th className="text-center p-3 text-xs font-semibold text-slate-400">Tiempo</th>
                        <th className="text-center p-3 text-xs font-semibold text-slate-400">Tendencia</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedMetrics.map((metric, index) => (
                        <tr 
                          key={metric.id}
                          className="border-b border-slate-700/30 hover:bg-slate-800/50 transition-colors"
                        >
                          <td className="p-3">
                            <div className="flex items-center gap-3">
                              <div className={cn(
                                "w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold",
                                index === selectedMetrics.length - 1 
                                  ? "bg-gradient-to-br from-emerald-500 to-cyan-500 text-white"
                                  : "bg-slate-700 text-slate-300"
                              )}>
                                {index + 1}
                              </div>
                              <span className="font-semibold">{metric.schoolYear}</span>
                            </div>
                          </td>
                          <td className="p-3 text-center">{metric.totalStudents}</td>
                          <td className="p-3 text-center font-semibold">{metric.averageProgress}%</td>
                          <td className="p-3 text-center">
                            <span className={cn(
                              "font-bold",
                              metric.averageGrade >= 80 ? "text-emerald-400" :
                              metric.averageGrade >= 60 ? "text-amber-400" : "text-red-400"
                            )}>
                              {metric.averageGrade}%
                            </span>
                          </td>
                          <td className="p-3">
                            <div className="flex items-center justify-center gap-2">
                              <div className="w-16 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full"
                                  style={{ width: `${metric.completionRate}%` }}
                                />
                              </div>
                            </div>
                          </td>
                          <td className="p-3 text-center text-sm text-muted-foreground">
                            {formatPlayTime(metric.averageActiveTime)}
                          </td>
                          <td className="p-3 text-center">
                            {metric.progressTrend !== 0 && (
                              <ComparisonBadge trend={metric.progressTrend} />
                            )}
                            {metric.progressTrend === 0 && (
                              <span className="text-xs text-slate-500">—</span>
                            )}
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
              subtitle="Tendencia histórica de las métricas"
              icon={TrendingUp}
              delay={0}
              accentColor="cyan"
            />
            
            <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6 mb-6">
              <h3 className="text-lg font-semibold mb-6">Progreso y Calificación</h3>
              <LineChartComponent
                data={selectedMetrics.map(m => ({
                  date: m.schoolYear,
                  averageProgress: m.averageProgress,
                  averageGrade: m.averageGrade,
                }))}
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

            <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
              <h3 className="text-lg font-semibold mb-6">Completación y Engagement</h3>
              <LineChartComponent
                data={selectedMetrics.map(m => ({
                  date: m.schoolYear,
                  completionRate: m.completionRate,
                  sessionsPerStudent: m.averageSessionsPerStudent,
                }))}
                xAxisDataKey="date"
                lines={[
                  { dataKey: "completionRate", name: "Tasa Completación", color: "#F59E0B" },
                  { dataKey: "sessionsPerStudent", name: "Sesiones/Est", color: "#8B5CF6" },
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
              title="Comparación de Años" 
              subtitle={`${selectedMetrics.length} años seleccionados`}
              icon={ArrowRightLeft}
              delay={0}
              accentColor="amber"
            />
            
            <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6 mb-6">
              <h3 className="text-lg font-semibold mb-6">Métricas Comparadas</h3>
              <BarChart
                data={selectedMetrics.map(m => ({
                  name: m.schoolYear,
                  Progreso: m.averageProgress,
                  Calificación: m.averageGrade,
                  Completación: m.completionRate,
                }))}
                xAxisDataKey="name"
                bars={[
                  { dataKey: "Progreso", color: "#10B981" },
                  { dataKey: "Calificación", color: "#06B6D4" },
                  { dataKey: "Completación", color: "#F59E0B" },
                ]}
                title=""
                subtitle=""
                yAxisLabel="%"
                height={350}
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
                <h3 className="text-lg font-semibold mb-4">Distribución de Rendimiento</h3>
                <p className="text-sm text-muted-foreground mb-4">Último año seleccionado</p>
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

              <div className="rounded-xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
                <h3 className="text-lg font-semibold mb-4">Tendencias Año a Año</h3>
                <p className="text-sm text-muted-foreground mb-4">Vs año anterior</p>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {selectedMetrics.slice(1).map((metric, idx) => (
                    <div 
                      key={metric.id}
                      className="p-3 rounded-lg bg-slate-800/30 border border-slate-700/30"
                    >
                      <p className="text-xs font-medium mb-1">{metric.schoolYear}</p>
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
            <h3 className="text-xl font-semibold mb-2">Selecciona al menos 2 años</h3>
            <p className="text-muted-foreground max-w-md">
              Elige dos o más años escolares para comparar su rendimiento.
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="text-center py-8 border-t border-slate-800 mt-8">
          <p className="text-sm text-muted-foreground">
            📊 Reporte de {subjectName} • Hello World Platform
          </p>
        </div>
      </div>
    </div>
  );
}
