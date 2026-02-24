'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { COLORS } from '@/lib/colors';

type AverageGradesChartProps = {
  course: string;
  averageGrade: number;
};

// Mock data for the chart - in a real app, this would come from the API
const generateMockData = (averageGrade: number) => {
  return [
    { name: 'Curso Actual', grade: averageGrade },
    { name: 'Curso Anterior', grade: averageGrade - 5 },
    { name: 'Curso Anterior 2', grade: averageGrade + 2 },
    { name: 'Promedio Institución', grade: 75 },
  ];
};

export default function AverageGradesChart({ course, averageGrade }: AverageGradesChartProps) {
  const data = generateMockData(averageGrade);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Promedio General de Calificaciones</CardTitle>
        <CardDescription>Promedio de calificaciones por curso</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip 
                formatter={(value) => [`${value}`, 'Calificación']}
                labelFormatter={(label) => `Curso: ${label}`}
              />
              <Bar dataKey="grade" fill={COLORS.primary} name="Calificación Promedio" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 text-center">
          <p className="text-2xl font-bold">{averageGrade}%</p>
          <p className="text-sm text-muted-foreground">Promedio del curso {course}</p>
        </div>
      </CardContent>
    </Card>
  );
}