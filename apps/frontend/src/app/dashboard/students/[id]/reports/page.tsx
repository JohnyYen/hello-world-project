import { Button } from "@/components/ui/button";
import { ChevronLeft, Trophy, Gamepad2, Clock, Target, Flame } from "lucide-react";
import Link from "next/link";
import { MetricCard, LineChart, BarChart, DonutChart } from "@/components/charts";
import { useStudentReports } from "@/hooks/use-student-reports";

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

export default function StudentReportPage({ params }: { params: { id: string } }) {
  const { kpis, progressOverTime, levelPerformance, activityDistribution, isLoading, error } =
    useStudentReports(params.id);

  if (isLoading) {
    return (
      <div className="container mx-auto py-10">
        <div className="mb-6">
          <Link href={`/dashboard/students/${params.id}`}>
            <Button variant="outline" className="mb-4">
              <ChevronLeft className="h-4 w-4 mr-2" />
              Volver al perfil
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Reportes de Progreso</h1>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="text-muted-foreground">Cargando datos...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-10">
        <div className="mb-6">
          <Link href={`/dashboard/students/${params.id}`}>
            <Button variant="outline" className="mb-4">
              <ChevronLeft className="h-4 w-4 mr-2" />
              Volver al perfil
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Reportes de Progreso</h1>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="text-red-500">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <div className="mb-6">
        <Link href={`/dashboard/students/${params.id}`}>
          <Button variant="outline" className="mb-4">
            <ChevronLeft className="h-4 w-4 mr-2" />
            Volver al perfil
          </Button>
        </Link>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Reportes de Progreso</h1>
            <p className="text-muted-foreground">Análisis detallado del estudiante</p>
          </div>
        </div>
      </div>

      {/* KPIs Section */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Métricas Principales</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Niveles Completados"
            value={kpis?.totalLevelsCompleted || 0}
            icon={<Trophy className="h-5 w-5" />}
            description="Niveles terminados exitosamente"
          />
          <MetricCard
            title="Partidas Jugadas"
            value={kpis?.totalGamesPlayed || 0}
            icon={<Gamepad2 className="h-5 w-5" />}
            description="Total de sesiones de juego"
          />
          <MetricCard
            title="Tiempo de Juego"
            value={formatPlayTime(kpis?.totalPlayTime || 0)}
            icon={<Clock className="h-5 w-5" />}
            description="Tiempo total activo"
          />
          <MetricCard
            title="Racha Actual"
            value={`${kpis?.currentStreak || 0} días`}
            icon={<Flame className="h-5 w-5" />}
            description={`Última actividad: ${formatDate(kpis?.lastActivity || null)}`}
          />
        </div>
      </section>

      {/* Progress Over Time Chart */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Progreso en el Tiempo</h2>
        <LineChart
          data={progressOverTime}
          xAxisDataKey="date"
          lines={[
            { dataKey: "score", name: "Puntuación", color: "#2563EB" },
            { dataKey: "level", name: "Nivel", color: "#10B981" },
          ]}
          title="Evolución de puntuación y nivel"
          yAxisLabel="Valor"
          height={320}
        />
      </section>

      {/* Level Performance & Activity Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <section>
          <h2 className="text-xl font-semibold mb-4">Desempeño por Nivel</h2>
          <BarChart
            data={levelPerformance}
            xAxisDataKey="levelName"
            bars={[{ dataKey: "score", name: "Puntuación", color: "#8B5CF6" }]}
            title="Puntuación por nivel"
            yAxisLabel="Puntos"
            height={320}
          />
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-4">Distribución de Actividades</h2>
          <DonutChart
            data={activityDistribution.map((item) => ({
              name: item.gameName,
              value: item.timeSpent,
            }))}
            title="Tiempo por juego (minutos)"
            height={320}
          />
        </section>
      </div>

      {/* Additional Stats */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <MetricCard
          title="Puntuación Promedio"
          value={`${kpis?.averageScore || 0}%`}
          icon={<Target className="h-5 w-5" />}
          description="Promedio de puntuación en todos los niveles"
        />
        <div className="rounded-lg border bg-card p-6 shadow-sm">
          <h3 className="text-lg font-semibold mb-4">Resumen de Actividad</h3>
          <div className="space-y-4">
            {activityDistribution.map((activity, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-primary" />
                  <span className="text-sm">{activity.gameName}</span>
                </div>
                <div className="text-sm text-muted-foreground">
                  {activity.sessions} sesiones • {formatPlayTime(activity.timeSpent)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
