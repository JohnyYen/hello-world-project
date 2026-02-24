'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { COLORS } from '@/lib/colors';

type ActivityPerformanceProps = {
  activities: ActivityPerformance[];
};

// Define the ActivityPerformance type here to avoid issues
type ActivityPerformance = {
  activityId: string;
  name: string;
  avgScore: number;
  completionRate: number;
  difficulty: number;
};

const ActivityPerformanceChart = ({ activities }: ActivityPerformanceProps) => {
  // Prepare data for the chart
  const chartData = activities.map(activity => ({
    name: activity.name,
    avgScore: activity.avgScore,
    completionRate: activity.completionRate,
    difficulty: activity.difficulty
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Rendimiento de Actividades</CardTitle>
        <CardDescription>Promedio de puntuación y tasa de completado por actividad</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 70,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                angle={-45} 
                textAnchor="end" 
                height={80}
                tick={{ fontSize: 12 }}
              />
              <YAxis yAxisId="left" domain={[0, 100]} />
              <YAxis yAxisId="right" orientation="right" domain={[0, 10]} />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'avgScore' || name === 'completionRate') return [`${value}%`, 'Porcentaje'];
                  if (name === 'difficulty') return [value, 'Dificultad (1-10)'];
                  return [value, name];
                }}
              />
              <Legend />
<Bar yAxisId="left" dataKey="avgScore" fill={COLORS.primary} name="Puntaje Promedio" />
<Bar yAxisId="left" dataKey="completionRate" fill={COLORS.secondary} name="Tasa de Completado" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default ActivityPerformanceChart;