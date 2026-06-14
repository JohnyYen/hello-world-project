import { getMetricsOverview } from "@/lib/metrics-data";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { TrendingUp, TrendingDown, Minus, Clock, Users, BarChart3 } from "lucide-react";

export async function CourseCompletionServer() {
  let overview;
  try {
    overview = await getMetricsOverview();
  } catch {
    return (
      <Card className="border-0 shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold">
            Tendencias del Sistema
          </CardTitle>
          <CardDescription>
            No se pudieron cargar los datos de tendencias
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const { kpis, trends } = overview;

  const trendItems = [
    {
      title: "Estudiantes Activos",
      value: kpis.activeStudentsThisWeek.toLocaleString(),
      subtitle: "esta semana",
      change: trends.studentsChangePercent,
      icon: Users,
      color: "text-primary",
      bg: "bg-primary/10",
    },
    {
      title: "Niveles Completados",
      value: kpis.totalLevelsCompleted.toLocaleString(),
      subtitle: "en total",
      change: trends.activityChangePercent,
      icon: BarChart3,
      color: "text-emerald-600",
      bg: "bg-emerald-50",
    },
    {
      title: "Tiempo Total de Juego",
      value: formatPlayTime(kpis.totalPlayTimeMinutes),
      subtitle: "acumulado",
      change: null,
      icon: Clock,
      color: "text-amber-600",
      bg: "bg-amber-50",
    },
    {
      title: "Puntaje Promedio",
      value: `${Math.round(kpis.averageScore)}%`,
      subtitle: "cambio vs período anterior",
      change: trends.scoreChangePercent,
      icon: TrendingUp,
      color: "text-violet-600",
      bg: "bg-violet-50",
    },
  ];

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">
          Tendencias del Sistema
        </CardTitle>
        <CardDescription>
          Comparativa vs período anterior
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {trendItems.map((item, index) => (
            <div
              key={index}
              className="flex items-start gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50"
            >
              <div className={`p-2 rounded-lg ${item.bg} ${item.color}`}>
                <item.icon className="h-4 w-4" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs text-slate-500">{item.title}</p>
                <p className="text-lg font-bold text-slate-900 dark:text-white">
                  {item.value}
                </p>
                <div className="flex items-center gap-1 mt-0.5">
                  {item.change !== null ? (
                    <>
                      {item.change > 0 ? (
                        <TrendingUp className="h-3 w-3 text-emerald-500" />
                      ) : item.change < 0 ? (
                        <TrendingDown className="h-3 w-3 text-red-500" />
                      ) : (
                        <Minus className="h-3 w-3 text-slate-400" />
                      )}
                      <span
                        className={`text-xs font-medium ${
                          item.change > 0
                            ? "text-emerald-600"
                            : item.change < 0
                              ? "text-red-600"
                              : "text-slate-400"
                        }`}
                      >
                        {item.change > 0 ? "+" : ""}
                        {item.change.toFixed(1)}%
                      </span>
                    </>
                  ) : (
                    <span className="text-xs text-slate-400">
                      {item.subtitle}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function formatPlayTime(minutes: number): string {
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  if (hours < 24) return `${hours}h ${remainingMinutes}m`;
  const days = Math.floor(hours / 24);
  const remainingHours = hours % 24;
  return `${days}d ${remainingHours}h`;
}
