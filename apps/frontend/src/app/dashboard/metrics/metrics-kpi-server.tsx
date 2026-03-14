import { unstable_cache } from 'next/cache';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, UserCheck, Target, Award } from 'lucide-react';

// Data fetching con caché
async function getMetrics() {
  return unstable_cache(
    async () => {
      await new Promise(resolve => setTimeout(resolve, 100));
      return {
        totalStudents: 1250,
        activeStudents: 980,
        avgCompletionRate: 75,
        avgScore: 82,
        totalCourses: 24,
        activeCourses: 18
      };
    },
    ['metrics-summary'],
    { revalidate: 300, tags: ['metrics'] }
  )();
}

export async function MetricsKPIServer() {
  const metrics = await getMetrics();

  const stats = [
    {
      title: 'Total Estudiantes',
      value: metrics.totalStudents.toLocaleString(),
      icon: Users,
      color: 'text-blue-600',
      bg: 'bg-blue-50'
    },
    {
      title: 'Estudiantes Activos',
      value: metrics.activeStudents.toLocaleString(),
      icon: UserCheck,
      color: 'text-emerald-600',
      bg: 'bg-emerald-50'
    },
    {
      title: 'Tasa de Completado',
      value: `${metrics.avgCompletionRate}%`,
      icon: Target,
      color: 'text-amber-600',
      bg: 'bg-amber-50'
    },
    {
      title: 'Calificación Promedio',
      value: `${metrics.avgScore}%`,
      icon: Award,
      color: 'text-violet-600',
      bg: 'bg-violet-50'
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, index) => (
        <Card key={index} className="overflow-hidden border-0 shadow-lg hover:shadow-xl transition-shadow">
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
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
