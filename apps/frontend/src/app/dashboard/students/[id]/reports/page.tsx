"use client";

import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  ChevronLeft,
  Trophy,
  Gamepad2,
  Clock,
  Target,
  Flame,
  TrendingUp,
  Activity,
  Zap,
  Award,
  Info,
} from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  MetricCard,
  LineChart,
  BarChart,
  DonutChart,
  AreaChart,
  HeatMap,
} from "@/components/charts";
import { ChartHelp } from "@/components/ui/chart-help";
import { ExportButton } from "@/components/export/ExportButton";
import { useStudentReports } from "@/hooks/use-student-reports";
import { useStudentHeatmap } from "@/hooks/use-student-heatmap";
import { useStudentGames } from "@/hooks/use-student-games";
import { GameSelector } from "@/components/games/GameSelector";

function formatPlayTime(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours > 0) {
    return `${hours}h ${mins}m`;
  }
  return `${mins}m`;
}

function formatDate(dateString: string | null): string {
  if (!dateString) return "Sin actividad";
  const date = new Date(dateString);
  return date.toLocaleDateString("es-ES", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Animated section header component
function SectionHeader({
  title,
  subtitle,
  icon: Icon,
  delay = 0,
}: {
  title: string;
  subtitle?: string;
  icon?: React.ElementType;
  delay?: number;
}) {
  return (
    <div
      className="relative mb-8 pl-4 border-l-4 border-indigo-500 dark:border-indigo-400"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center gap-3 mb-2">
        {Icon && (
          <div className="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400">
            <Icon className="w-5 h-5" />
          </div>
        )}
        <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      </div>
      {subtitle && <p className="text-muted-foreground ml-12">{subtitle}</p>}
      {/* Decorative line */}
      <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-indigo-500 to-violet-500 group-hover:w-full transition-all duration-500" />
    </div>
  );
}

export default function StudentReportPage() {
  const params = useParams();
  const studentId = params.id as string;
  const containerRef = useRef<HTMLDivElement>(null);

  const [selectedGameId, setSelectedGameId] = useState<string | null>(null);

  const {
    games: availableGames,
    isLoading: isLoadingGames,
  } = useStudentGames(studentId);

  const {
    kpis,
    progressOverTime,
    levelPerformance,
    activityDistribution,
    isLoading,
    error,
  } = useStudentReports(studentId, selectedGameId);

  // Get real heatmap data from API
  const { heatmapData, isLoading: isLoadingHeatmap } = useStudentHeatmap(
    studentId,
    30,
  );

  // Calculate cumulative time for area chart
  const cumulativeProgress = progressOverTime.reduce<
    Array<{ date: string; cumulativeScore: number; cumulativeTime: number }>
  >((acc, item, index) => {
    const prevCumulative = index > 0 ? acc[index - 1].cumulativeScore : 0;
    const prevTime = index > 0 ? acc[index - 1].cumulativeTime : 0;
    acc.push({
      date: item.date,
      cumulativeScore: prevCumulative + item.score,
      cumulativeTime: prevTime + item.timeSpent,
    });
    return acc;
  }, []);

  // Sort level performance by score descending for better readability
  const sortedLevelPerformance = [...levelPerformance].sort(
    (a, b) => b.score - a.score,
  );

  // Color bars by score threshold for instant visual comprehension
  function getScoreColor(score: number): string {
    if (score >= 80) return "#10B981"; // Excelente
    if (score >= 50) return "#F59E0B"; // En progreso
    return "#EF4444"; // Necesita mejorar
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="animate-pulse space-y-8">
            <div className="h-8 w-48 bg-slate-200 dark:bg-slate-800 rounded" />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div
                  key={i}
                  className="h-32 bg-slate-200 dark:bg-slate-800 rounded-xl"
                />
              ))}
            </div>
            <div className="h-96 bg-slate-200 dark:bg-slate-800 rounded-xl" />
          </div>
        </div>
      </div>
    );
  }

  // Build game selector options: "Todos los juegos" + lista de juegos disponibles
  const gameOptions = [
    { id: null, title: "Todos los juegos" },
    ...availableGames.map((game) => ({ id: game.id, title: game.title })),
  ];

  // Cuando hay un juego específico seleccionado, el donut de distribución
  // no tiene sentido (solo mostraría 1 juego), así que lo ocultamos
  const hasSingleGameSelected = selectedGameId !== null;

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
        <div className="container mx-auto py-12 px-6">
          <div className="mb-6">
            <Link href={`/dashboard/students/${studentId}`}>
              <Button variant="outline" className="mb-4">
                <ChevronLeft className="h-4 w-4 mr-2" />
                Volver al perfil
              </Button>
            </Link>
          </div>
          <div className="flex items-center justify-center h-64">
            <div className="text-red-500 p-4 rounded-lg bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800">
              {error}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Background pattern */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern
              id="grid"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="currentColor"
                strokeWidth="1"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div
        ref={containerRef}
        className="container mx-auto py-12 px-6 relative z-10"
      >
        {/* Header */}
        <div className="mb-12">
          <Link href={`/dashboard/students/${studentId}`}>
            <Button
              variant="ghost"
              className="mb-6 hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:text-indigo-600 transition-colors"
            >
              <ChevronLeft className="h-4 w-4 mr-2" />
              Volver al perfil
            </Button>
          </Link>

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400 bg-clip-text text-transparent">
                Reportes de Progreso
              </h1>
              <p className="text-muted-foreground text-lg">
                Análisis detallado del rendimiento académico
              </p>
            </div>

            <div className="flex items-center gap-4">
              <ExportButton
                targetRef={containerRef}
                fileName={`reporte-estudiante-${studentId}`}
                variant="outline"
                size="sm"
                label="Exportar PDF"
              />
              {/* Decorative badge */}
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-100 dark:bg-indigo-900/40 border border-indigo-200 dark:border-indigo-800">
                <div className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
                <span className="text-sm font-medium text-indigo-700 dark:text-indigo-300">
                  Datos actualizados
                </span>
                <span className="text-xs text-indigo-500 dark:text-indigo-400">
                  •
                </span>
                <span className="text-xs text-indigo-500 dark:text-indigo-400">
                  {formatDate(kpis?.lastActivity || null)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Game Selector - Filtrar por juego */}
        {gameOptions.length > 1 && (
          <div className="mb-10 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm shadow-sm">
            <GameSelector
              games={gameOptions}
              selectedGameId={selectedGameId}
              onSelect={setSelectedGameId}
              isLoading={isLoadingGames}
            />
          </div>
        )}

        {/* KPIs Section - Now with variant highlights */}
        <section className="mb-12">
          <SectionHeader
            title="Métricas Principales"
            subtitle={selectedGameId
              ? "Rendimiento en el juego seleccionado"
              : "Indicadores clave de rendimiento del estudiante"}
            icon={Activity}
            delay={0}
          />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div
              style={{ animationDelay: "100ms" }}
              className="animate-fade-in-up"
            >
              <MetricCard
                title="Niveles Completados"
                value={kpis?.totalLevelsCompleted || 0}
                icon={<Trophy className="h-5 w-5" />}
                description="Niveles terminados exitosamente"
                variant="default"
              />
            </div>
            <div
              style={{ animationDelay: "200ms" }}
              className="animate-fade-in-up"
            >
              <MetricCard
                title="Partidas Jugadas"
                value={kpis?.totalGamesPlayed || 0}
                icon={<Gamepad2 className="h-5 w-5" />}
                description="Total de sesiones de juego"
                variant="default"
              />
            </div>
            <div
              style={{ animationDelay: "300ms" }}
              className="animate-fade-in-up"
            >
              <MetricCard
                title="Tiempo de Juego"
                value={formatPlayTime(kpis?.totalPlayTime || 0)}
                icon={<Clock className="h-5 w-5" />}
                description="Tiempo total activo"
                variant="highlight"
              />
            </div>
            <div
              style={{ animationDelay: "400ms" }}
              className="animate-fade-in-up"
            >
              <MetricCard
                title="Racha Actual"
                value={`${kpis?.currentStreak || 0} días`}
                icon={<Flame className="h-5 w-5" />}
                description={`Última actividad: ${formatDate(kpis?.lastActivity || null)}`}
                variant="accent"
              />
            </div>
          </div>
        </section>

        {/* Progress Over Time - Line & Area Charts */}
        <section className="mb-12">
          <SectionHeader
            title="Análisis Temporal"
            subtitle={selectedGameId
              ? "Evolución del rendimiento en el juego seleccionado"
              : "Evolución del rendimiento a lo largo del tiempo"}
            icon={TrendingUp}
            delay={500}
          />

          {/* Line Chart - Score & Level */}
          <div
            className="mb-8 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden"
            style={{ animationDelay: "600ms" }}
          >
            <div className="p-6 border-b border-slate-100 dark:border-slate-800">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold">
                    Evolución de puntuación y nivel
                    <ChartHelp content="Muestra la tendencia de puntuación y nivel a lo largo del tiempo. Útil para identificar momentos de mejora, estancamiento o retroceso." />
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Rendimiento semanal del estudiante
                  </p>
                </div>
                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-primary" />
                    <span className="text-muted-foreground">Puntuación</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-accent/100" />
                    <span className="text-muted-foreground">Nivel</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="p-6">
              <LineChart
                data={progressOverTime}
                xAxisDataKey="date"
                lines={[
                  { dataKey: "score", name: "Puntuación", color: "#3B82F6" },
                  { dataKey: "level", name: "Nivel", color: "#10B981" },
                ]}
                title=""
                subtitle=""
                yAxisLabel="Puntuación / Nivel"
                xAxisLabel="Fecha"
                yAxisDomain={[0, 100]}
                height={320}
                tooltipFormatter={(value, name) => {
                  if (name === "Puntuación") return `${value} pts`;
                  if (name === "Nivel") return `${value}`;
                  return String(value);
                }}
              />
            </div>
          </div>

          {/* Area Chart - Cumulative Progress - Separated into two charts for clarity */}
          {/* Cumulative Score */}
          <div className="mb-8 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
            <div className="p-6 border-b border-slate-100 dark:border-slate-800">
              <h3 className="text-lg font-semibold">
                Puntuación Acumulada
                <ChartHelp content="Refleja la suma total de puntos obtenidos. Una curva con pendiente constante indica progreso consistente." />
              </h3>
              <p className="text-sm text-muted-foreground">
                Evolución de la puntuación total a lo largo del tiempo
              </p>
            </div>
            <div className="p-6">
              <AreaChart
                data={cumulativeProgress}
                xAxisDataKey="date"
                areas={[
                  {
                    dataKey: "cumulativeScore",
                    name: "Puntuación Acumulada",
                    color: "#3B82F6",
                    yAxisId: "left",
                  },
                ]}
                title=""
                subtitle=""
                yAxisLabels={{ left: "Puntos" }}
                xAxisLabel="Fecha"
                height={280}
              />
            </div>
          </div>

          {/* Cumulative Time */}
          <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
            <div className="p-6 border-b border-slate-100 dark:border-slate-800">
              <h3 className="text-lg font-semibold">
                Tiempo Acumulado
                <ChartHelp content="Muestra el tiempo total invertido. Permite correlacionar horas de estudio con el rendimiento obtenido." />
              </h3>
              <p className="text-sm text-muted-foreground">
                Evolución del tiempo total invertido (minutos)
              </p>
            </div>
            <div className="p-6">
              <AreaChart
                data={cumulativeProgress}
                xAxisDataKey="date"
                areas={[
                  {
                    dataKey: "cumulativeTime",
                    name: "Tiempo Acumulado",
                    color: "#F59E0B",
                    yAxisId: "left",
                  },
                ]}
                title=""
                subtitle=""
                yAxisLabels={{ left: "Minutos" }}
                xAxisLabel="Fecha"
                height={280}
              />
            </div>
          </div>
        </section>

        {/* Activity Heatmap */}
        <section className="mb-12">
          <SectionHeader
            title="Patrón de Actividad"
            subtitle={selectedGameId
              ? "Distribución temporal de actividad en el juego seleccionado"
              : "Distribución temporal del tiempo de estudio"}
            icon={Zap}
            delay={800}
          />
          <div
            className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden"
            style={{ animationDelay: "900ms" }}
          >
            <div className="p-6 border-b border-slate-100 dark:border-slate-800">
              <h3 className="text-lg font-semibold">
                Mapa de Actividad Semanal
                <ChartHelp content="Visualiza los momentos de mayor actividad del estudiante. Ayuda a identificar horarios y días de mayor productividad." />
              </h3>
              <p className="text-sm text-muted-foreground">
                Distribución de tiempo de juego por día y hora
              </p>
            </div>
            <div className="p-6">
              <HeatMap
                data={heatmapData?.data || []}
                title=""
                subtitle=""
                height={320}
                tooltipFormatter={(value, day, hour) => `${value} actividades`}
              />
            </div>
          </div>
        </section>

        {/* Level Performance & Activity Distribution */}
        <section className="mb-12">
          <SectionHeader
            title="Desempeño por Área"
            subtitle={selectedGameId
              ? "Análisis detallado por nivel del juego seleccionado"
              : "Análisis detallado por nivel y tipo de actividad"}
            icon={Award}
            delay={1000}
          />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div
              className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden"
              style={{ animationDelay: "1100ms" }}
            >
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h3 className="text-lg font-semibold">
                  Desempeño por Nivel
                  <ChartHelp content="Compara el rendimiento en cada nivel. Las barras verdes muestran fortalezas; las rojas, áreas que necesitan refuerzo." />
                </h3>
                <p className="text-sm text-muted-foreground">
                  Puntuación obtenida en cada nivel (ordenado de mejor a peor)
                </p>
                {/* Color key legend */}
                <div className="flex items-center gap-4 mt-3 text-xs">
                  <span className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                    Excelente (80+)
                  </span>
                  <span className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                    En progreso (50-79)
                  </span>
                  <span className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-red-500" />
                    Necesita mejorar (&lt;50)
                  </span>
                </div>
              </div>
              <div className="p-6">
                <BarChart
                  data={sortedLevelPerformance}
                  xAxisDataKey="levelName"
                  bars={[
                    { dataKey: "score", name: "Puntuación" },
                  ]}
                  title=""
                  subtitle=""
                  yAxisLabel="Puntos"
                  height={320}
                  layout="vertical"
                  yAxisDomain={[0, 100]}
                  hideLegend
                  barFill={(entry) =>
                    getScoreColor((entry as { score: number }).score)
                  }
                  tooltipLabelFormatter={(label, item) => {
                    const typedItem = item as {
                      levelName: string;
                      score: number;
                      attempts?: number;
                      timeSpent?: number;
                      completed?: boolean;
                    };
                    const parts: string[] = [];
                    if (typedItem.completed) {
                      parts.push("✅ Completado");
                    } else {
                      parts.push("⏳ En progreso");
                    }
                    if (typedItem.attempts) {
                      parts.push(`${typedItem.attempts} intentos`);
                    }
                    if (typedItem.timeSpent) {
                      parts.push(
                        formatPlayTime(typedItem.timeSpent),
                      );
                    }
                    const extra = parts.join(" • ");
                    return extra ? `${label} (${extra})` : label;
                  }}
                  tooltipFormatter={(value) => `${value} pts`}
                />
              </div>
            </div>

            {hasSingleGameSelected ? (
              <div
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden"
                style={{ animationDelay: "1200ms" }}
              >
                <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                  <h3 className="text-lg font-semibold">
                    Juego seleccionado
                    <ChartHelp content="Vista filtrada para un juego específico. El resto de los gráficos también se actualizan para reflejar solo los datos de este juego." />
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Datos filtrados para un juego específico
                  </p>
                </div>
                <div className="p-6 flex items-center justify-center h-[320px]">
                  <div className="text-center">
                    <Gamepad2 className="w-12 h-12 mx-auto mb-3 text-indigo-400" />
                    <p className="text-muted-foreground">
                      Mostrando datos del juego seleccionado.
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Seleccioná "Todos los juegos" para ver la distribución
                      entre juegos.
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden"
                style={{ animationDelay: "1200ms" }}
              >
                <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                  <h3 className="text-lg font-semibold">
                    Distribución de Actividades
                    <ChartHelp content="Muestra cómo se distribuye el tiempo entre los distintos juegos. Útil para detectar si el estudiante se enfoca en un área o diversifica su aprendizaje." />
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    Tiempo dedicado a cada juego
                  </p>
                </div>
                <div className="p-6">
                  <DonutChart
                    data={activityDistribution.map((item) => ({
                      name: item.gameName,
                      value: item.timeSpent,
                    }))}
                    title=""
                    subtitle=""
                    height={320}
                  />
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Footer decorative element */}
        <div className="text-center py-8 border-t border-slate-200 dark:border-slate-800">
          <p className="text-sm text-muted-foreground">
            📊 Reporte generado automáticamente • Hello World Platform
          </p>
        </div>
      </div>
    </div>
  );
}
