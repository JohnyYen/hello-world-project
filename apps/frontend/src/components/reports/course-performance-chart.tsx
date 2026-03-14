'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell,
  LabelList 
} from 'recharts';
import { cn } from '@/lib/utils';
import type { CourseMetrics } from '@/types/course-report.interface';

interface CoursePerformanceChartProps {
  course: CourseMetrics;
  showDetails?: boolean;
}

const COLORS = {
  high: '#10B981',
  medium: '#F59E0B', 
  low: '#EF4444',
};

export function CoursePerformanceChart({
  course,
  showDetails = true
}: CoursePerformanceChartProps) {
  const total = course.highPerformers + course.mediumPerformers + course.lowPerformers;
  
  const data = [
    { 
      name: 'Alto', 
      value: course.highPerformers, 
      percentage: Math.round((course.highPerformers / total) * 100),
      color: COLORS.high 
    },
    { 
      name: 'Medio', 
      value: course.mediumPerformers, 
      percentage: Math.round((course.mediumPerformers / total) * 100),
      color: COLORS.medium
    },
    { 
      name: 'Bajo', 
      value: course.lowPerformers, 
      percentage: Math.round((course.lowPerformers / total) * 100),
      color: COLORS.low 
    },
  ];

  return (
    <Card className="overflow-hidden border-0 shadow-lg h-full">
      <CardHeader className="pb-2 bg-gradient-to-r from-slate-900 to-slate-800">
        <CardTitle className="text-white text-lg font-semibold tracking-tight">
          Distribución de Rendimiento
        </CardTitle>
        <CardDescription className="text-slate-300">
          {course.courseName}
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" horizontal={true} vertical={false} />
              <XAxis 
                type="number" 
                domain={[0, total]} 
                tick={{ fill: '#64748B', fontSize: 11 }}
                tickLine={{ stroke: '#E2E8F0' }}
                axisLine={{ stroke: '#E2E8F0' }}
              />
              <YAxis 
                type="category" 
                dataKey="name" 
                tick={{ fill: '#1E293B', fontSize: 13, fontWeight: 600 }}
                tickLine={false}
                axisLine={false}
                width={60}
              />
              <Tooltip 
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-slate-900 text-white px-3 py-2 rounded-lg shadow-xl text-sm">
                        <p className="font-medium">{data.name} Rendimiento</p>
                        <p className="text-slate-300">{data.value} estudiantes ({data.percentage}%)</p>
                      </div>
                    );
                  }
                  return null;
                }}
                cursor={{ fill: '#F1F5F9' }}
              />
              <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={32}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
                <LabelList 
                  dataKey="percentage" 
                  position="right" 
                  formatter={(value: number) => `${value}%`}
                  style={{ fill: '#64748B', fontSize: 12, fontWeight: 600 }}
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        {showDetails && (
          <div className="grid grid-cols-3 gap-2 mt-4">
            {data.map((item) => (
              <div 
                key={item.name}
                className={cn(
                  "text-center p-2 rounded-lg border",
                  item.name === 'Alto' && "bg-accent/10 border-emerald-200",
                  item.name === 'Medio' && "bg-accent/10 border-accent/30",
                  item.name === 'Bajo' && "bg-red-50 border-red-200"
                )}
              >
                <div className="text-lg font-bold" style={{ color: item.color }}>
                  {item.percentage}%
                </div>
                <div className="text-xs text-slate-500">{item.name}</div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
