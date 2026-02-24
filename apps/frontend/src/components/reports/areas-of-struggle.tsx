'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { COLORS } from '@/lib/colors';

type AreasOfStruggleProps = {
  performanceIssues: PerformanceIssue[];
};

// Define the PerformanceIssue type here to avoid issues
type PerformanceIssue = {
  topic: string;
  percentage: number; // Percentage of students struggling (0-100)
};

const AreasOfStruggle = ({ performanceIssues }: AreasOfStruggleProps) => {
  // Prepare data for the chart, sorted by percentage (highest first)
  const sortedIssues = [...performanceIssues].sort((a, b) => b.percentage - a.percentage);
  
  const chartData = sortedIssues.map(issue => ({
    name: issue.topic,
    percentage: issue.percentage
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Áreas Donde Fallan Más</CardTitle>
        <CardDescription>Porcentaje de estudiantes que tienen dificultades en cada área</CardDescription>
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
              <YAxis domain={[0, 100]} tickFormatter={(value) => `${value}%`} />
              <Tooltip 
                formatter={(value) => [`${value}%`, 'Estudiantes con dificultades']}
                labelFormatter={(label) => `Área: ${label}`}
              />
              <Bar dataKey="percentage" fill={COLORS.chart.orange} name="Porcentaje de Dificultad" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default AreasOfStruggle;