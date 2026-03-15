'use client';

import { useState, useEffect } from 'react';
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
  const mins = minutes % 60;
  if (hours > 0) {
    return `${hours}h ${mins}m`;
  }
  return `${mins}m`;
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

// Course selector chip
function CourseChip({ 
  course, 
  isSelected, 
  onClick 
}: { 
  course: Course; 
  isSelected: boolean; 
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "relative px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-300",
        "border backdrop-blur-sm",
        isSelected 
          ? "bg-gradient-to-r from-emerald-500 to-cyan-500 text-white border-transparent shadow-lg shadow-emerald-500/25" 
          : "bg-slate-100 dark:bg-slate-800/60 border-slate-200 dark:border-slate-700 hover:border-emerald-400 dark:hover:border-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/20"
      )}
    >
      <span className="flex items-center gap-2">
        <BookOpen className="w-4 h-4" />
        {course.name}
      </span>
      <span className={cn(
        "block text-xs mt-1 opacity-80",
        isSelected ? "text-white/90" : "text-muted-foreground"
      )}>
        {course.period}
      </span>
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

// Main component
export default function ReportsPage() {
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);
  const [selectedMetrics, setSelectedMetrics] = useState<CourseMetrics[]>([]);
  const [kpis, setKpis] = useState<CourseReportKPIs | null>(null);
  const [progressData, setProgressData] = useState<Record<string, CourseProgressOverTime[]>>({});
  const [activeTab, setActiveTab] = useState('overview');

  // Group courses by school year
  const coursesByYear = courses.reduce<Record<string, Course[]>>((acc, course) => {
    const yearMatch = course.period.match(/(\d{4})/);
    const year = yearMatch ? yearMatch[1] : 'Unknown';
    if (!acc[year]) acc[year] = [];
    acc[year].push(course);
    return acc;
  }, {});

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
        
        // Select first 2 courses by default for comparison
        if (coursesData.length >= 2) {
          setSelectedCourses([coursesData[0].id, coursesData[1].id]);
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
        setSelectedMetrics(metrics);

        // Load progress data for each course
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

  const getComparisonData = () => {
    if (selectedMetrics.length < 2) return null;
    
    const [course1, course2] = selectedMetrics;
    return {
      progressDiff: course1.averageProgress - course2.averageProgress,
      gradeDiff: course1.averageGrade - course2.averageGrade,
      engagementDiff: course1.engagementTrend - course2.engagementTrend,
    };
  };

  const comparison = getComparisonData();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="animate-pulse space-y-8">
            <div className="h-8 w-64 bg-slate-800 rounded" />
            <div className="flex gap-3">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-12 w-32 bg-slate-800 rounded-xl" />
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
            <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="2" cy="2" r="1" fill="currentColor"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          <rect width="100%" height="100%" fill="url(#dots)" />
        </svg>
      </div>

      <div className="container mx-auto py-12 px-6 relative z-10">
        {/* Header */}
        <div className="mb-12">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div>
              <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-emerald-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">
                Reportes de Curso
              </h1>
              <p className="text-muted-foreground text-lg">
                Análisis comparativo de rendimiento académico por período
              </p>
            </div>
            
            {/* Decorative badge */}
            <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-slate-800/80 dark:bg-slate-900/80 border border-slate-700 dark:border-slate-600 backdrop-blur-sm">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-sm font-medium text-slate-300">{courses.length} cursos analizados</span>
            </div>
          </div>

          {/* Course Selection */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <ArrowRightLeft className="w-4 h-4" />
              <span>Selecciona cursos para comparar:</span>
              <span className="font-medium text-emerald-400">{selectedCourses.length} seleccionados</span>
            </div>
            <div className="flex flex-wrap gap-3">
              {courses.map((course) => (
                <CourseChip
                  key={course.id}
                  course={course}
                  isSelected={selectedCourses.includes(course.id)}
                  onClick={() => toggleCourse(course.id)}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-8 p-1 bg-slate-900/50 dark:bg-slate-800/50 rounded-xl w-fit backdrop-blur-sm">
          {[
            { id: 'overview', label: 'Resumen', icon: BarChart3 },
            { id: 'comparison', label: 'Comparación', icon: ArrowRightLeft },
            { id: 'trends', label: 'Tendencias', icon: TrendingUp },
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
            {/* KPIs Section */}
            <section className="mb-12">
              <SectionHeader 
                title="Métricas Globales" 
                subtitle="Indicadores consolidados de todos los cursos"
                icon={Activity}
                delay={0}
              />
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div style={{ animationDelay: "100ms" }} className="animate-fade-in-up">
                  <MetricCard
                    title="Total Cursos"
                    value={kpis?.totalCourses || 0}
                    icon={<BookOpen className="h-5 w-5" />}
                    description={`${Object.keys(coursesByYear).length} períodos académicos`}
                    variant="default"
                  />
                </div>
                <div style={{ animationDelay: "200ms" }} className="animate-fade-in-up">
                  <MetricCard
                    title="Total Estudiantes"
                    value={kpis?.totalStudents || 0}
                    icon={<Users className="h-5 w-5" />}
                    description="Matriculados activamente"
                    variant="default"
                  />
                </div>
                <div style={{ animationDelay: "300ms" }} className="animate-fade-in-up">
                  <MetricCard
                    title="Tasa de Completación"
                    value={`${kpis?.overallCompletionRate || 0}%`}
                    icon={<CheckCircle2 className="h-5 w-5" />}
                    description="Promedio entre cursos"
                    variant="highlight"
                  />
                </div>
                <div style={{ animationDelay: "400ms" }} className="animate-fade-in-up">
                  <MetricCard
                    title="Calificación Promedio"
                    value={`${kpis?.overallAverageGrade || 0}%`}
                    icon={<Target className="h-5 w-5" />}
                    description="Rendimiento académico medio"
                    variant="accent"
                  />
                </div>
              </div>
            </section>

            {/* Course Performance Table */}
            <section className="mb-12">
              <SectionHeader 
                title="Rendimiento por Curso" 
                subtitle="Métricas detalladas de cada curso"
                icon={Award}
                delay={500}
              />
              <div className="rounded-2xl border border-slate-700/50 dark:border-slate-600/30 bg-slate-900/50 dark:bg-slate-800/30 backdrop-blur-sm shadow-xl shadow-emerald-500/5 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-700/50 dark:border-slate-600/30">
                        <th className="text-left p-4 text-sm font-semibold text-slate-400">Curso</th>
                        <th className="text-left p-4 text-sm font-semibold text-slate-400">Período</th>
                        <th className="text-center p-4 text-sm font-semibold text-slate-400">Progreso</th>
                        <th className="text-center p-4 text-sm font-semibold text-slate-400">Calificación</th>
                        <th className="text-center p-4 text-sm font-semibold text-slate-400">Completación</th>
                        <th className="text-center p-4 text-sm font-semibold text-slate-400">Tiempo Activo</th>
                        <th className="text-center p-4 text-sm font-semibold text-slate-400">Tendencia</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedMetrics.map((metric, index) => (
                        <tr 
                          key={metric.courseId}
                          className="border-b border-slate-700/30 dark:border-slate-600/20 hover:bg-slate-800/50 transition-colors"
                          style={{ animationDelay: `${600 + index * 100}ms` }}
                        >
                          <td className="p-4">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 flex items-center justify-center">
                                <BookOpen className="w-4 h-4 text-emerald-400" />
                              </div>
                              <span className="font-medium">{metric.courseName}</span>
                            </div>
                          </td>
                          <td className="p-4 text-sm text-muted-foreground">{metric.period}</td>
                          <td className="p-4 text-center">
                            <span className="font-semibold">{metric.averageProgress}%</span>
                          </td>
                          <td className="p-4 text-center">
                            <span className={cn(
                              "font-bold",
                              metric.averageGrade >= 80 ? "text-emerald-400" :
                              metric.averageGrade >= 60 ? "text-amber-400" : "text-red-400"
                            )}>
                              {metric.averageGrade}%
                            </span>
                          </td>
                          <td className="p-4 text-center">
                            <div className="flex items-center justify-center gap-2">
                              <div className="w-16 h-2 bg-slate-700 rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full"
                                  style={{ width: `${metric.completionRate}%` }}
                                />
                              </div>
                              <span className="text-sm">{metric.completionRate}%</span>
                            </div>
                          </td>
                          <td className="p-4 text-center text-sm">
                            {formatPlayTime(metric.averageActiveTime)}
                          </td>
                          <td className="p-4 text-center">
                            <ComparisonBadge trend={metric.progressTrend} />
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>

            {/* Progress Over Time Chart */}
            {selectedMetrics.length > 0 && (
              <section className="mb-12">
                <SectionHeader 
                  title="Evolución del Rendimiento" 
                  subtitle="Tendencia de progreso y calificación a lo largo del tiempo"
                  icon={TrendingUp}
                  delay={1000}
                  accentColor="cyan"
                />
                <div className="rounded-2xl border border-slate-700/50 dark:border-slate-600/30 bg-slate-900/50 dark:bg-slate-800/30 backdrop-blur-sm shadow-xl shadow-cyan-500/5 overflow-hidden">
                  <div className="p-6 border-b border-slate-700/50 dark:border-slate-600/30">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-lg font-semibold">Progreso vs Calificación</h3>
                        <p className="text-sm text-muted-foreground">Evolución mensual por curso</p>
                      </div>
                      <div className="flex items-center gap-4 text-sm">
                        {selectedMetrics.slice(0, 3).map((m, i) => (
                          <div key={m.courseId} className="flex items-center gap-2">
                            <div 
                              className="w-3 h-3 rounded-full" 
                              style={{ 
                                backgroundColor: ['#10B981', '#06B6D4', '#F59E0B'][i] 
                              }} 
                            />
                            <span className="text-muted-foreground">{m.courseName.split(' ')[0]}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="p-6">
                    <LineChartComponent
                      data={progressData[selectedMetrics[0]?.courseId] || []}
                      xAxisDataKey="date"
                      lines={[
                        { dataKey: "averageProgress", name: "Progreso", color: "#10B981" },
                        { dataKey: "averageGrade", name: "Calificación", color: "#06B6D4" },
                      ]}
                      title=""
                      subtitle=""
                      yAxisLabel="%"
                      height={320}
                    />
                  </div>
                </div>
              </section>
            )}
          </>
        )}

        {/* Comparison Tab */}
        {activeTab === 'comparison' && selectedMetrics.length >= 2 && (
          <section className="mb-12">
            <SectionHeader 
              title="Análisis Comparativo" 
              subtitle={`Comparación entre ${selectedMetrics[0]?.courseName} y ${selectedMetrics[1]?.courseName}`}
              icon={ArrowRightLeft}
              delay={0}
              accentColor="cyan"
            />
            
            {/* Comparison Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="rounded-2xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm text-muted-foreground">Diferencia en Progreso</span>
                  {comparison && (
                    <ComparisonBadge trend={comparison.progressDiff} />
                  )}
                </div>
                <div className="text-3xl font-bold">
                  {comparison && (
                    <span className={comparison.progressDiff >= 0 ? "text-emerald-400" : "text-red-400"}>
                      {comparison.progressDiff > 0 ? '+' : ''}{comparison.progressDiff.toFixed(1)}%
                    </span>
                  )}
                </div>
                <div className="mt-4 flex justify-between text-xs text-muted-foreground">
                  <span>{selectedMetrics[0]?.averageProgress}%</span>
                  <span>{selectedMetrics[1]?.averageProgress}%</span>
                </div>
              </div>

              <div className="rounded-2xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm text-muted-foreground">Diferencia en Calificación</span>
                  {comparison && (
                    <ComparisonBadge trend={comparison.gradeDiff} />
                  )}
                </div>
                <div className="text-3xl font-bold">
                  {comparison && (
                    <span className={comparison.gradeDiff >= 0 ? "text-emerald-400" : "text-red-400"}>
                      {comparison.gradeDiff > 0 ? '+' : ''}{comparison.gradeDiff.toFixed(1)}%
                    </span>
                  )}
                </div>
                <div className="mt-4 flex justify-between text-xs text-muted-foreground">
                  <span>{selectedMetrics[0]?.averageGrade}%</span>
                  <span>{selectedMetrics[1]?.averageGrade}%</span>
                </div>
              </div>

              <div className="rounded-2xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm text-muted-foreground">Diferencia en Engagement</span>
                  {comparison && (
                    <ComparisonBadge trend={comparison.engagementDiff} />
                  )}
                </div>
                <div className="text-3xl font-bold">
                  {comparison && (
                    <span className={comparison.engagementDiff >= 0 ? "text-emerald-400" : "text-red-400"}>
                      {comparison.engagementDiff > 0 ? '+' : ''}{comparison.engagementDiff.toFixed(1)}%
                    </span>
                  )}
                </div>
                <div className="mt-4 flex justify-between text-xs text-muted-foreground">
                  <span>{selectedMetrics[0]?.engagementTrend}%</span>
                  <span>{selectedMetrics[1]?.engagementTrend}%</span>
                </div>
              </div>
            </div>

            {/* Comparison Chart */}
            <div className="rounded-2xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
              <h3 className="text-lg font-semibold mb-6">Comparación de Métricas</h3>
              <BarChart
                data={selectedMetrics.map(m => ({
                  name: m.courseName.split(' ').slice(0, 2).join(' '),
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
          </section>
        )}

        {activeTab === 'comparison' && selectedMetrics.length < 2 && (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="w-20 h-20 rounded-full bg-slate-800/50 flex items-center justify-center mb-6">
              <ArrowRightLeft className="w-10 h-10 text-slate-500" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Selecciona al menos 2 cursos</h3>
            <p className="text-muted-foreground max-w-md">
              Para ver la comparación, necesitas seleccionar al menos 2 cursos diferentes. 
              Haz clic en los chips de arriba para añadir cursos a la comparación.
            </p>
          </div>
        )}

        {/* Trends Tab */}
        {activeTab === 'trends' && (
          <section className="mb-12">
            <SectionHeader 
              title="Análisis de Tendencias" 
              subtitle="Evolución del rendimiento entre períodos"
              icon={TrendingUp}
              delay={0}
              accentColor="amber"
            />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Performance Distribution */}
              <div className="rounded-2xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
                <h3 className="text-lg font-semibold mb-4">Distribución de Rendimiento</h3>
                <p className="text-sm text-muted-foreground mb-6">Distribución de estudiantes por nivel de rendimiento</p>
                <DonutChart
                  data={[
                    { name: 'Alto Rendimiento', value: selectedMetrics.reduce((sum, m) => sum + m.highPerformers, 0) },
                    { name: 'Rendimiento Medio', value: selectedMetrics.reduce((sum, m) => sum + m.mediumPerformers, 0) },
                    { name: 'Necesita Apoyo', value: selectedMetrics.reduce((sum, m) => sum + m.lowPerformers, 0) },
                  ]}
                  title=""
                  subtitle=""
                  height={300}
                />
              </div>

              {/* Engagement Over Time */}
              <div className="rounded-2xl border border-slate-700/50 bg-slate-900/50 backdrop-blur-sm p-6">
                <h3 className="text-lg font-semibold mb-4">Tendencia de Engagement</h3>
                <p className="text-sm text-muted-foreground mb-6">Cambio porcentual respecto al período anterior</p>
                <div className="space-y-4">
                  {selectedMetrics.map((metric) => (
                    <div 
                      key={metric.courseId}
                      className="flex items-center justify-between p-4 rounded-xl bg-slate-800/30 border border-slate-700/30"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 flex items-center justify-center">
                          <BookOpen className="w-5 h-5 text-emerald-400" />
                        </div>
                        <div>
                          <p className="font-medium">{metric.courseName}</p>
                          <p className="text-xs text-muted-foreground">{metric.period}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <p className="text-xs text-muted-foreground">Progreso</p>
                          <ComparisonBadge trend={metric.progressTrend} />
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-muted-foreground">Calificación</p>
                          <ComparisonBadge trend={metric.gradeTrend} />
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-muted-foreground">Engagement</p>
                          <ComparisonBadge trend={metric.engagementTrend} />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Footer */}
        <div className="text-center py-8 border-t border-slate-800">
          <p className="text-sm text-muted-foreground">
            📊 Reporte generado automáticamente • Hello World Platform
          </p>
        </div>
      </div>
    </div>
  );
}
