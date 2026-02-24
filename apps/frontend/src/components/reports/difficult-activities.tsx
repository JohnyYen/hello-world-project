'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { COLORS } from '@/lib/colors';

type DifficultActivitiesProps = {
  activities: Activity[];
};

// Define the Activity type here to avoid issues
type Activity = {
  id: string;
  name: string;
  difficulty: number; // 1-10 scale
  averageScore: number; // 0-100 percentage
  topic: string;
};

const DifficultActivities = ({ activities }: DifficultActivitiesProps) => {
  // Sort activities by difficulty (hardest first)
  const sortedActivities = [...activities].sort((a, b) => b.difficulty - a.difficulty);
  
  // Prepare data for the chart
  const chartData = sortedActivities.map(activity => ({
    name: activity.name,
    difficulty: activity.difficulty,
    averageScore: activity.averageScore
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Actividades Más Difíciles</CardTitle>
        <CardDescription>Actividades con mayor nivel de dificultad y menor puntuación promedio</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 60,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                angle={-45} 
                textAnchor="end" 
                height={70}
                tick={{ fontSize: 12 }}
              />
              <YAxis yAxisId="left" domain={[0, 10]} label={{ value: 'Dificultad', angle: -90, position: 'insideLeft' }} />
              <YAxis yAxisId="right" orientation="right" domain={[0, 100]} label={{ value: 'Puntaje Promedio', angle: 90, position: 'insideRight' }} />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'difficulty') return [`${value}/10`, 'Dificultad'];
                  if (name === 'averageScore') return [`${value}%`, 'Puntaje Promedio'];
                  return [value, name];
                }}
              />
              <Legend />
<Bar yAxisId="left" dataKey="difficulty" fill={COLORS.error} name="Dificultad (1-10)" />
<Bar yAxisId="right" dataKey="averageScore" fill={COLORS.info} name="Puntaje Promedio %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default DifficultActivities;