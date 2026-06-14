import { getMetricsOverview } from "@/lib/metrics-data";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

export async function StudentProgressServer() {
  let overview;
  try {
    overview = await getMetricsOverview();
  } catch {
    return (
      <Card className="border-0 shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold">
            Rendimiento por Juego
          </CardTitle>
          <CardDescription>
            No se pudieron cargar los datos
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  // Agrupar level_performance por juego
  const gameMap = new Map<string, {
    gameName: string;
    totalLevels: number;
    avgCompletionRate: number;
    avgAttempts: number;
  }>();

  for (const level of overview.levelPerformance) {
    const existing = gameMap.get(level.gameName);
    if (existing) {
      existing.totalLevels += 1;
      existing.avgCompletionRate += level.completionRate;
      existing.avgAttempts += level.averageAttempts;
    } else {
      gameMap.set(level.gameName, {
        gameName: level.gameName,
        totalLevels: 1,
        avgCompletionRate: level.completionRate,
        avgAttempts: level.averageAttempts,
      });
    }
  }

  const games = Array.from(gameMap.values())
    .map((g) => ({
      ...g,
      avgCompletionRate: Math.round((g.avgCompletionRate / g.totalLevels) * 100),
      avgAttempts: parseFloat((g.avgAttempts / g.totalLevels).toFixed(1)),
    }))
    .sort((a, b) => b.avgCompletionRate - a.avgCompletionRate);

  if (games.length === 0) {
    return (
      <Card className="border-0 shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold">
            Rendimiento por Juego
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
          Rendimiento por Juego
        </CardTitle>
        <CardDescription>
          Completado promedio por juego
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {games.map((game, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <div className="flex-1 min-w-0 mr-2">
                    <span className="text-sm font-medium text-slate-900 block truncate">
                      {game.gameName}
                    </span>
                    <span className="text-xs text-slate-400">
                      {game.totalLevels} niveles · Ø {game.avgAttempts} intentos
                    </span>
                  </div>
                  <span className="text-sm font-bold text-primary shrink-0">
                    {game.avgCompletionRate}%
                  </span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-primary to-primary h-2 rounded-full transition-all duration-500"
                    style={{ width: `${game.avgCompletionRate}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
