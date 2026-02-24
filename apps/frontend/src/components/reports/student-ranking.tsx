'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Student } from "./reports-data-provider";

type StudentRankingProps = {
  students: Student[];
};

const StudentRanking = ({ students }: StudentRankingProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Ranking de Estudiantes Destacados</CardTitle>
        <CardDescription>Top estudiantes por calificación promedio</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[80px]">Posición</TableHead>
              <TableHead>Nombre</TableHead>
              <TableHead>Calificación Promedio</TableHead>
              <TableHead>Progreso</TableHead>
              <TableHead>Rendimiento</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {students.map((student, index) => (
              <TableRow key={student.id}>
                <TableCell className="font-medium">
                  <div className="flex items-center">
                    {index < 3 ? (
                      // Medals for top 3
                      <span className={`mr-2 ${index === 0 ? 'text-yellow-500' : index === 1 ? 'text-gray-400' : 'text-amber-700'}`}>
                        {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                      </span>
                    ) : (
                      <span className="mr-2">#{index + 1}</span>
                    )}
                  </div>
                </TableCell>
                <TableCell className="font-medium">{student.name}</TableCell>
                <TableCell>
                  <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
                    {student.averageGrade}%
                  </span>
                </TableCell>
                <TableCell>{student.progress}%</TableCell>
                <TableCell>
                  {student.performanceLevel === "alta" ? (
                    <Badge variant="default" className="bg-green-600 text-white">
                      Alta
                    </Badge>
                  ) : student.performanceLevel === "media" ? (
                    <Badge variant="secondary" className="bg-yellow-600 text-white">
                      Media
                    </Badge>
                  ) : (
                    <Badge variant="outline" className="border-red-600 text-red-600">
                      Baja
                    </Badge>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default StudentRanking;