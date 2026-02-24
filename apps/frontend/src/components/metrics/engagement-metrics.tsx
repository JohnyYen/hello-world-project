'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { COLORS } from '@/lib/colors';

type EngagementMetricsProps = {
  dailyActivity: DailyActivity[];
};

// Define the DailyActivity type here to avoid issues
type DailyActivity = {
  date: string;
  activityCount: number;
  avgTimeSpent: number;
};

const EngagementMetrics = ({ dailyActivity }: EngagementMetricsProps) => {
  // Prepare data for the chart
  const chartData = dailyActivity.map(activity => ({
    date: new Date(activity.date).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' }),
    activityCount: activity.activityCount,
    avgTimeSpent: activity.avgTimeSpent
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Metriicas de Engagement</CardTitle>
        <CardDescription>Actividad diaria y tiempo promedio invertido</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 50,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45} 
                textAnchor="end" 
                height={70}
                tick={{ fontSize: 12 }}
              />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'activityCount') return [value, 'Actividades'];
                  if (name === 'avgTimeSpent') return [`${value} min`, 'Tiempo Promedio'];
                  return [value, name];
                }}
              />
              <Legend />
              <Line 
                yAxisId="left"
                type="monotone" 
                dataKey="activityCount" 
                stroke={COLORS.primary} 
                activeDot={{ r: 8 }} 
                name="Actividades"
              />
              <Line 
                yAxisId="right"
                type="monotone" 
                dataKey="avgTimeSpent" 
                stroke={COLORS.secondary} 
                name="Tiempo Promedio (min)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default EngagementMetrics;