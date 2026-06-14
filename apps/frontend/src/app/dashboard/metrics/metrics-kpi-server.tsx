import { getMetricsOverview } from "@/lib/metrics-data";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, UserCheck, Target, Award } from "lucide-react";

export async function MetricsKPIServer() {
  let overview;
  try {
    overview = await getMetricsOverview();
  } catch {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i} className="border-0 shadow-lg">
            <CardContent className="py-6">
              <p className="text-sm text-muted-foreground text-center">
                Error al cargar métricas
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  const stats = [
    {
      title: "Total Estudiantes",
      value: overview.kpis.totalStudents.toLocaleString(),
      subtitle: "registrados",
      icon: Users,
      color: "text-primary",
      bg: "bg-primary/10",
    },
    {
      title: "Estudiantes Activos",
      value: overview.kpis.activeStudentsThisMonth.toLocaleString(),
      subtitle: "últimos 30 días",
      icon: UserCheck,
      color: "text-emerald-600",
      bg: "bg-emerald-50",
    },
    {
      title: "Niveles Completados",
      value: overview.kpis.totalLevelsCompleted.toLocaleString(),
      subtitle: "en total",
      icon: Target,
      color: "text-amber-600",
      bg: "bg-amber-50",
    },
    {
      title: "Puntaje Promedio",
      value: `${Math.round(overview.kpis.averageScore)}%`,
      subtitle: "general",
      icon: Award,
      color: "text-violet-600",
      bg: "bg-violet-50",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, index) => (
        <Card
          key={index}
          className="overflow-hidden border-0 shadow-lg hover:shadow-xl transition-shadow"
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">
              {stat.title}
            </CardTitle>
            <stat.icon className={`h-4 w-4 ${stat.color}`} />
          </CardHeader>
          <CardContent>
            <div className={`text-3xl font-bold ${stat.color}`}>
              {stat.value}
            </div>
            <p className="text-xs text-slate-400 mt-1">{stat.subtitle}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
