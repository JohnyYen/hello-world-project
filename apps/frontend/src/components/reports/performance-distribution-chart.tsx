'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { COLORS } from '@/lib/colors';

type PerformanceDistributionChartProps = {
  alta: number;
  media: number;
  baja: number;
};

const PerformanceDistributionChart = ({ alta, media, baja }: PerformanceDistributionChartProps) => {
  const data = [
    { name: 'Alta', value: alta, color: COLORS.success },
    { name: 'Media', value: media, color: COLORS.warning },
    { name: 'Baja', value: baja, color: COLORS.error },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Distribución del Rendimiento</CardTitle>
        <CardDescription>Proporción de estudiantes por nivel de rendimiento</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={true}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value} estudiantes`, 'Cantidad']} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="grid grid-cols-3 gap-4 mt-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-accent">{alta}</div>
            <p className="text-sm text-muted-foreground">Alto Rendimiento</p>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-accent">{media}</div>
            <p className="text-sm text-muted-foreground">Rendimiento Medio</p>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">{baja}</div>
            <p className="text-sm text-muted-foreground">Bajo Rendimiento</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PerformanceDistributionChart;