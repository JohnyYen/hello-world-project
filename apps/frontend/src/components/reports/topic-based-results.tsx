'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { COLORS } from '@/lib/colors';

type TopicBasedResultsProps = {
  topics: Topic[];
};

// Define the Topic type here to avoid issues
type Topic = {
  id: string;
  name: string;
  averageScore: number; // 0-100 percentage
};

const TopicBasedResults = ({ topics }: TopicBasedResultsProps) => {
  // Prepare data for the chart, sorted by average score
  const sortedTopics = [...topics].sort((a, b) => b.averageScore - a.averageScore);
  
  const chartData = sortedTopics.map(topic => ({
    name: topic.name,
    averageScore: topic.averageScore
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Promedio de Resultado por Temas</CardTitle>
        <CardDescription>Promedio de calificaciones por cada tema del curso</CardDescription>
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
                bottom: 50,
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
              <YAxis domain={[0, 100]} />
              <Tooltip 
                formatter={(value) => [`${value}%`, 'Puntaje Promedio']}
                labelFormatter={(label) => `Tema: ${label}`}
              />
              <Bar dataKey="averageScore" fill={COLORS.chart.purple} name="Puntaje Promedio" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default TopicBasedResults;