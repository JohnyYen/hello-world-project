'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { COLORS } from '@/lib/colors';

type IndividualStudentPerformanceProps = {
  students: Student[];
};

// Define the Student type here to avoid issues
type Student = {
  id: string;
  name: string;
  course: string;
  averageGrade: number;
  performanceLevel: "alta" | "media" | "baja";
  completedLessons: number;
  totalLessons: number;
  progress: number;
  achievements: string[];
};

const IndividualStudentPerformance = ({ students }: IndividualStudentPerformanceProps) => {
  // Transform student data for the chart (using progress as a value over time)
  const chartData = students.map((student) => ({
    name: student.name,
    progress: student.progress,
    averageGrade: student.averageGrade,
    completed: student.completedLessons
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Rendimiento Individual de Estudiantes</CardTitle>
        <CardDescription>Progreso y calificación promedio por estudiante</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={chartData}
              margin={{
                top: 10,
                right: 30,
                left: 0,
                bottom: 0,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis yAxisId="left" domain={[0, 100]} />
              <YAxis yAxisId="right" orientation="right" domain={[0, 40]} />
              <Tooltip />
              <Area 
                yAxisId="left"
                type="monotone" 
                dataKey="averageGrade" 
                stroke={COLORS.primary} 
                fill={COLORS.primary} 
                fillOpacity={0.3} 
                name="Calificación Promedio" 
              />
              <Area 
                yAxisId="left"
                type="monotone" 
                dataKey="progress" 
                stroke={COLORS.secondary} 
                fill={COLORS.secondary} 
                fillOpacity={0.3} 
                name="Progreso %" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default IndividualStudentPerformance;