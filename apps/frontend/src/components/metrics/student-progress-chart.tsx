'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown } from "lucide-react";

type StudentProgressProps = {
  students: StudentProgress[];
};

// Define the StudentProgress type here to avoid issues
type StudentProgress = {
  id: string;
  name: string;
  progress: number;
  score: number;
  lastActivity: string;
};

const StudentProgressChart = ({ students }: StudentProgressProps) => {
  // Calculate trend direction for each student
  const getTrend = (progress: number) => {
    if (progress >= 80) return { icon: TrendingUp, color: "text-green-500", trend: "Alto" };
    if (progress >= 60) return { icon: TrendingUp, color: "text-yellow-500", trend: "Medio" };
    return { icon: TrendingDown, color: "text-red-500", trend: "Bajo" };
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Progreso de Estudiantes</CardTitle>
        <CardDescription>Progreso y puntuación de los estudiantes más activos</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Estudiante</TableHead>
              <TableHead>Progreso</TableHead>
              <TableHead>Puntaje</TableHead>
              <TableHead>Última Actividad</TableHead>
              <TableHead>Tendencia</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {students.map((student) => {
              const trend = getTrend(student.progress);
              const TrendIcon = trend.icon;
              
              return (
                <TableRow key={student.id}>
                  <TableCell className="font-medium">{student.name}</TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      <span className="mr-2">{student.progress}%</span>
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            student.progress > 75 ? 'bg-green-500' : 
                            student.progress > 50 ? 'bg-yellow-500' : 'bg-red-500'
                          }`} 
                          style={{ width: `${student.progress}%` }}
                        ></div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant={student.score >= 80 ? "default" : student.score >= 60 ? "secondary" : "outline"}>
                      {student.score}%
                    </Badge>
                  </TableCell>
                  <TableCell>{new Date(student.lastActivity).toLocaleDateString()}</TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      <TrendIcon className={`h-4 w-4 ${trend.color} mr-1`} />
                      <span className={trend.color}>{trend.trend}</span>
                    </div>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default StudentProgressChart;