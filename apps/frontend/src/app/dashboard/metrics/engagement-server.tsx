import { getMetricsOverview } from "@/lib/metrics-data";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export async function EngagementServer() {
  let overview;
  try {
    overview = await getMetricsOverview();
  } catch {
    return (
      <Card className="border-0 shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold">
            Métricas de Engagement
          </CardTitle>
          <CardDescription>
            No se pudieron cargar los datos de actividad
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const activity = overview.activityOverTime;

  if (activity.length === 0) {
    return (
      <Card className="border-0 shadow-lg">
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold">
            Métricas de Engagement
          </CardTitle>
          <CardDescription>
            No hay datos de actividad en el período seleccionado
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const maxSessions = Math.max(...activity.map((d) => d.sessions));
  const totalSessions = activity.reduce((sum, d) => sum + d.sessions, 0);
  const avgSessions = Math.round(totalSessions / activity.length);
  const totalPlayTime = activity.reduce((sum, d) => sum + d.playTimeMinutes, 0);

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">
          Métricas de Engagement
        </CardTitle>
        <CardDescription>
          Actividad diaria de estudiantes (últimos {activity.length} días)
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-around mb-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-primary">
              {avgSessions}
            </div>
            <div className="text-xs text-slate-500">Sesiones/día (prom.)</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-amber-600">
              {maxSessions}
            </div>
            <div className="text-xs text-slate-500">Máximo de sesiones</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-emerald-600">
              {Math.round(totalPlayTime / activity.length)}m
            </div>
            <div className="text-xs text-slate-500">Tiempo prom./día</div>
          </div>
        </div>

        {/* Bar chart de sesiones diarias */}
        <div className="flex items-end justify-between gap-1 h-24">
          {activity.map((day, i) => (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div
                className="w-full bg-gradient-to-t from-primary to-primary/70 rounded-t min-h-[4px]"
                style={{
                  height: `${Math.max((day.sessions / maxSessions) * 100, 2)}%`,
                }}
              />
              <span className="text-[10px] text-slate-400">
                {new Date(day.date).getDate()}/{new Date(day.date).getMonth() + 1}
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
