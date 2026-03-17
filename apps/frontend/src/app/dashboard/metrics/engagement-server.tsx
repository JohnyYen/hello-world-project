import { unstable_cache } from 'next/cache';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

async function getDailyActivity() {
  return unstable_cache(
    async () => {
      await new Promise(resolve => setTimeout(resolve, 80));
      return [
        { date: "2024-10-20", activityCount: 120, avgTimeSpent: 45 },
        { date: "2024-10-21", activityCount: 145, avgTimeSpent: 52 },
        { date: "2024-10-22", activityCount: 168, avgTimeSpent: 48 },
        { date: "2024-10-23", activityCount: 132, avgTimeSpent: 50 },
        { date: "2024-10-24", activityCount: 156, avgTimeSpent: 54 },
        { date: "2024-10-25", activityCount: 110, avgTimeSpent: 42 },
        { date: "2024-10-26", activityCount: 98, avgTimeSpent: 38 },
        { date: "2024-10-27", activityCount: 175, avgTimeSpent: 58 },
        { date: "2024-10-28", activityCount: 182, avgTimeSpent: 60 },
        { date: "2024-10-29", activityCount: 201, avgTimeSpent: 62 },
        { date: "2024-10-30", activityCount: 195, avgTimeSpent: 59 },
      ];
    },
    ['daily-activity'],
    { revalidate: 300, tags: ['metrics'] }
  )();
}

export async function EngagementServer() {
  const activity = await getDailyActivity();
  const maxActivity = Math.max(...activity.map(d => d.activityCount));
  
  // Promedio simple
  const avgActivity = Math.round(activity.reduce((sum, d) => sum + d.activityCount, 0) / activity.length);
  const avgTime = Math.round(activity.reduce((sum, d) => sum + d.avgTimeSpent, 0) / activity.length);

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">Métricas de Engagement</CardTitle>
        <CardDescription>Actividad diaria de estudiantes</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-around mb-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-primary">{avgActivity}</div>
            <div className="text-xs text-slate-500">Promedio diario</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-accent">{maxActivity}</div>
            <div className="text-xs text-slate-500">Máximo</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-accent">{avgTime}min</div>
            <div className="text-xs text-slate-500">Tiempo prom.</div>
          </div>
        </div>
        
        {/* Mini chart visual */}
        <div className="flex items-end justify-between gap-1 h-24">
          {activity.slice(-7).map((day, i) => (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div 
                className="w-full bg-gradient-to-t from-primary to-primary rounded-t"
                style={{ height: `${(day.activityCount / maxActivity) * 100}%` }}
              />
              <span className="text-[10px] text-slate-400">
                {new Date(day.date).getDate()}
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
