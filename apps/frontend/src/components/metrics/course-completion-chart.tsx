'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { COLORS } from '@/lib/colors';

type CourseCompletionChartProps = {
  courses: CourseCompletion[];
};

// Define the CourseCompletion type here to avoid issues
type CourseCompletion = {
  courseId: string;
  courseName: string;
  completionRate: number;
  enrolled: number;
  completed: number;
};

const CourseCompletionChart = ({ courses }: CourseCompletionChartProps) => {
  // Prepare data for the chart
  const chartData = courses.map(course => ({
    name: course.courseName,
    enrolled: course.enrolled,
    completed: course.completed,
    completionRate: course.completionRate
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Completado de Cursos</CardTitle>
        <CardDescription>Porcentaje de completado por curso</CardDescription>
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
              <YAxis />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'completionRate') return [`${value}%`, 'Tasa de Completado'];
                  return [value, name === 'enrolled' ? 'Inscritos' : 'Completados'];
                }}
              />
              <Legend />
<Bar dataKey="enrolled" fill={COLORS.primary} name="Inscritos" />
<Bar dataKey="completed" fill={COLORS.secondary} name="Completados" />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-4">
            <p className="text-sm text-muted-foreground">La tasa de completado se muestra como porcentaje sobre la barra</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CourseCompletionChart;