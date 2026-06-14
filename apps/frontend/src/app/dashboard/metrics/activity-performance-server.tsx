import { getMetricsOverview } from "@/lib/metrics-data";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

function getDifficultyLabel(completionRate: number): {
  label: string;
  className: string;
} {
  if (completionRate >= 0.8) return { label: "Fácil", className: "bg-emerald-100 text-emerald-700" };
  if (completionRate >= 0.5) return { label: "Medio", className: "bg-amber-100 text-amber-700" };
  return { label: "Difícil", className: "bg-red-100 text-red-700" };
}

export async function ActivityPerformanceServer() {
  let overview;
  try {
    overview = await getMetricsOverview();
  } catch {
    return (
      <Card className="border-0 shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold">
            Rendimiento por Nivel
          </CardTitle>
          <CardDescription>
            No se pudieron cargar los datos de rendimiento
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const levels = overview.levelPerformance;

  if (levels.length === 0) {
    return (
      <Card className="border-0 shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold">
            Rendimiento por Nivel
          </CardTitle>
          <CardDescription>
            No hay datos de rendimiento disponibles
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">
          Rendimiento por Nivel
        </CardTitle>
        <CardDescription>
          Tasa de completado e intentos por nivel
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {levels.map((level, index) => {
            const completionPercent = Math.round(level.completionRate * 100);
            const difficulty = getDifficultyLabel(level.completionRate);

            return (
              <div key={index} className="flex items-center gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex-1 min-w-0 mr-2">
                      <span className="text-sm font-medium text-slate-900 block truncate">
                        {level.levelName}
                      </span>
                      <span className="text-xs text-slate-400 block truncate">
                        {level.gameName}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className="text-sm font-bold text-primary">
                        {completionPercent}%
                      </span>
                      <span className="text-xs text-slate-400">|</span>
                      <span className="text-xs text-slate-500">
                        Ø {level.averageAttempts.toFixed(1)} intentos
                      </span>
                    </div>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-primary to-primary/70 h-full rounded-full transition-all"
                      style={{ width: `${completionPercent}%` }}
                    />
                  </div>
                </div>
                <span
                  className={`text-xs px-2 py-0.5 rounded font-medium shrink-0 ${difficulty.className}`}
                >
                  {difficulty.label}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
