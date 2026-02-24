'use client';

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { User, Users, FileText, Target } from "lucide-react";

type MetricsSummaryProps = {
  totalStudents: number;
  activeStudents: number;
  avgCompletionRate: number;
  avgScore: number;
};

const MetricsSummary = ({ totalStudents, activeStudents, avgCompletionRate, avgScore }: MetricsSummaryProps) => {
  const activeRate = Math.round((activeStudents / totalStudents) * 100);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Estudiantes</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totalStudents.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">+5% desde el mes pasado</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Estudiantes Activos</CardTitle>
          <User className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{activeStudents.toLocaleString()}</div>
          <p className="text-xs text-muted-foreground">{activeRate}% del total</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Tasa de Completado</CardTitle>
          <FileText className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{avgCompletionRate}%</div>
          <p className="text-xs text-muted-foreground">+2% desde el mes pasado</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Puntaje Promedio</CardTitle>
          <Target className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{avgScore}%</div>
          <p className="text-xs text-muted-foreground">+3% desde el mes pasado</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default MetricsSummary;