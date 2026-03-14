import { unstable_cache } from 'next/cache';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

async function getActivityPerformance() {
  return unstable_cache(
    async () => {
      await new Promise(resolve => setTimeout(resolve, 80));
      return [
        { activityId: "a1", name: "Variables y Tipos", avgScore: 92, completionRate: 88, difficulty: 2 },
        { activityId: "a2", name: "Condicionales", avgScore: 85, completionRate: 82, difficulty: 3 },
        { activityId: "a3", name: "Bucles", avgScore: 78, completionRate: 75, difficulty: 4 },
        { activityId: "a4", name: "Funciones", avgScore: 72, completionRate: 68, difficulty: 6 },
        { activityId: "a5", name: "Arrays", avgScore: 68, completionRate: 65, difficulty: 5 },
      ];
    },
    ['activity-performance'],
    { revalidate: 300, tags: ['metrics'] }
  )();
}

export async function ActivityPerformanceServer() {
  const activities = await getActivityPerformance();

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">Rendimiento por Actividad</CardTitle>
        <CardDescription>Calificación y completado por tema</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {activities.map((activity) => (
            <div key={activity.activityId} className="flex items-center gap-4">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-slate-900">{activity.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-emerald-600">{activity.avgScore}%</span>
                    <span className="text-xs text-slate-400">|</span>
                    <span className="text-sm text-slate-500">{activity.completionRate}%</span>
                  </div>
                </div>
                <div className="flex gap-1">
                  {/* Score bar */}
                  <div className="flex-1 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div 
                      className="bg-emerald-500 h-full rounded-full"
                      style={{ width: `${activity.avgScore}%` }}
                    />
                  </div>
                  {/* Completion bar */}
                  <div className="flex-1 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div 
                      className="bg-blue-500 h-full rounded-full"
                      style={{ width: `${activity.completionRate}%` }}
                    />
                  </div>
                </div>
              </div>
              <div className={`text-xs px-2 py-0.5 rounded ${
                activity.difficulty <= 3 ? 'bg-emerald-100 text-emerald-700' :
                activity.difficulty <= 5 ? 'bg-amber-100 text-amber-700' :
                'bg-red-100 text-red-700'
              }`}>
                {activity.difficulty <= 3 ? 'Fácil' : activity.difficulty <= 5 ? 'Medio' : 'Difícil'}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
