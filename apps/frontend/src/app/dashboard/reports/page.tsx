'use client';

import { Suspense, useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { LoadingState } from '@/components/ui/loading-state';
import { FileText, BarChart3, TrendingUp } from 'lucide-react';
import { 
  getCourses, 
  getSelectedCourseMetrics, 
  getCourseProgressOverTime,
  getReportKPIs 
} from '@/components/reports/course-report-data';
import { CourseComparisonChart } from '@/components/reports/course-comparison-chart';
import { ProgressTrendChart } from '@/components/reports/progress-trend-chart';
import { CoursePerformanceChart } from '@/components/reports/course-performance-chart';
import { CourseMultiSelector } from '@/components/reports/course-multi-selector';
import { CourseMetricsGrid } from '@/components/reports/course-metric-card';
import { CourseReportKPIs as CourseReportKPIsComponent, CourseHighlightCards } from '@/components/reports/course-report-kpis';
import type { Course, CourseMetrics, CourseReportKPIs, CourseProgressOverTime } from '@/types/course-report.interface';

export default function ReportsPage() {
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);
  const [selectedMetrics, setSelectedMetrics] = useState<CourseMetrics[]>([]);
  const [kpis, setKpis] = useState<CourseReportKPIs | null>(null);
  const [progressData, setProgressData] = useState<Record<string, CourseProgressOverTime[]>>({});
  const [activeTab, setActiveTab] = useState('overview');

  // Cargar datos iniciales
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [coursesData, kpisData] = await Promise.all([
          getCourses(),
          getReportKPIs()
        ]);
        
        setCourses(coursesData);
        setKpis(kpisData);
        
        // Seleccionar primeros 2 cursos por defecto
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

  // Cargar métricas de cursos seleccionados
  useEffect(() => {
    const loadSelectedMetrics = async () => {
      if (selectedCourses.length === 0) {
        setSelectedMetrics([]);
        return;
      }

      try {
        const metrics = await getSelectedCourseMetrics(selectedCourses);
        setSelectedMetrics(metrics);

        // Cargar datos de tendencia para cada curso
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

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <LoadingState message="Cargando reportes..." size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header con estilo editorial */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-12 px-6 md:px-12">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="h-6 w-6 text-slate-300" />
            <span className="text-sm font-medium text-slate-300 uppercase tracking-wider">
              Reportes Institucionales
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            Reportes de Curso
          </h1>
          <p className="text-slate-300 text-lg max-w-2xl">
            Análisis integral del rendimiento académico y engagement de estudiantes por curso.
            Compara el desempeño entre diferentes grupos.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8">
        {/* Selector de cursos para comparación */}
        <div className="mb-8">
          <CourseMultiSelector
            courses={courses}
            selectedCourses={selectedCourses}
            onSelectionChange={setSelectedCourses}
            maxSelection={4}
          />
        </div>

        {/* Tabs de navegación */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="bg-white border border-slate-200 p-1 h-auto">
            <TabsTrigger 
              value="overview" 
              className="flex items-center gap-2 px-4 py-2 data-[state=active]:bg-slate-900 data-[state=active]:text-white"
            >
              <BarChart3 className="w-4 h-4" />
              Vista General
            </TabsTrigger>
            <TabsTrigger 
              value="comparison" 
              className="flex items-center gap-2 px-4 py-2 data-[state=active]:bg-slate-900 data-[state=active]:text-white"
            >
              <TrendingUp className="w-4 h-4" />
              Comparación
            </TabsTrigger>
          </TabsList>

          {/* Tab: Vista General */}
          <TabsContent value="overview" className="space-y-6">
            {/* KPIs */}
            {kpis && <CourseReportKPIsComponent kpis={kpis} />}

            {/* Cursos destacados */}
            {kpis && (
              <CourseHighlightCards 
                topCourse={kpis.topPerformingCourse}
                attentionCourse={kpis.needsAttentionCourse}
              />
            )}

            {/* Métricas del curso seleccionado */}
            {selectedMetrics.length > 0 && selectedMetrics.length <= 1 && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-bold text-slate-900 mb-4">
                    Métricas de {selectedMetrics[0].courseName}
                  </h2>
                  <CourseMetricsGrid course={selectedMetrics[0]} />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <ProgressTrendChart 
                    data={{ [selectedMetrics[0].courseId]: progressData[selectedMetrics[0].courseId] || [] }}
                    courses={selectedMetrics}
                  />
                  <CoursePerformanceChart course={selectedMetrics[0]} />
                </div>
              </div>
            )}

            {/* Mensaje cuando no hay cursos seleccionados */}
            {selectedMetrics.length === 0 && (
              <Card className="border-dashed border-2 border-slate-300">
                <CardContent className="py-12 text-center">
                  <BarChart3 className="h-12 w-12 text-slate-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-600 mb-2">
                    Selecciona un curso para ver sus métricas
                  </h3>
                  <p className="text-slate-500">
                    Usa el selector de arriba para elegir qué curso quieres analizar
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Tab: Comparación */}
          <TabsContent value="comparison" className="space-y-6">
            {selectedMetrics.length >= 2 ? (
              <>
                {/* Gráficos de comparación */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <CourseComparisonChart
                    courses={selectedMetrics}
                    metric="averageProgress"
                    title="Progreso Promedio"
                    description="Comparación del avance general"
                  />
                  <CourseComparisonChart
                    courses={selectedMetrics}
                    metric="averageGrade"
                    title="Calificación Promedio"
                    description="Comparación del rendimiento académico"
                  />
                  <CourseComparisonChart
                    courses={selectedMetrics}
                    metric="completionRate"
                    title="Tasa de Completado"
                    description="Porcentaje de contenido finalizado"
                  />
                  <CourseComparisonChart
                    courses={selectedMetrics}
                    metric="averageActiveTime"
                    title="Tiempo Activo Promedio"
                    description="Minutos de actividad por estudiante"
                    unit=" min"
                  />
                </div>

                {/* Tendencia de progreso */}
                <ProgressTrendChart 
                  data={progressData}
                  courses={selectedMetrics}
                  title="Tendencia de Progreso"
                  description="Evolución del promedio a lo largo del período"
                />

                {/* Distribución de rendimiento por curso */}
                <div>
                  <h2 className="text-xl font-bold text-slate-900 mb-4">
                    Distribución de Rendimiento
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {selectedMetrics.map((metric) => (
                      <CoursePerformanceChart 
                        key={metric.courseId} 
                        course={metric}
                        showDetails={true}
                      />
                    ))}
                  </div>
                </div>
              </>
            ) : (
              <Card className="border-dashed border-2 border-slate-300">
                <CardContent className="py-12 text-center">
                  <TrendingUp className="h-12 w-12 text-slate-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-600 mb-2">
                    Selecciona al menos 2 cursos para comparar
                  </h3>
                  <p className="text-slate-500">
                    Elige múltiples cursos del selector para ver análisis comparativos
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
