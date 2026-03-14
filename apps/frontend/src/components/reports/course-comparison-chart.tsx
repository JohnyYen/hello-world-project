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
  Cell 
} from 'recharts';
import { cn } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import type { CourseMetrics } from '@/types/course-report.interface';

interface CourseComparisonChartProps {
  courses: CourseMetrics[];
  metric: 'averageProgress' | 'averageGrade' | 'completionRate' | 'averageActiveTime' | 'dailyActiveUsers';
  title: string;
  description?: string;
  unit?: string;
}

const COLORS = [
  '#1E3A5F', // deep navy
  '#3B82F6', // blue
  '#10B981', // emerald
  '#F59E0B', // amber
  '#EF4444', // red
];

export function CourseComparisonChart({
  courses,
  metric,
  title,
  description,
  unit = '%'
}: CourseComparisonChartProps) {
  const data = courses.map((course, index) => ({
    name: course.courseName.length > 15 
      ? course.courseName.substring(0, 15) + '...' 
      : course.courseName,
    fullName: course.courseName,
    value: course[metric] as number,
    color: COLORS[index % COLORS.length],
  }));

  const maxValue = Math.max(...data.map(d => d.value));
  
  // Calcular trend
  const firstValue = data[0]?.value || 0;
  const lastValue = data[data.length - 1]?.value || 0;
  const trend = ((lastValue - firstValue) / (firstValue || 1)) * 100;

  return (
    <Card className="overflow-hidden border-0 shadow-lg">
      <CardHeader className="pb-2 bg-gradient-to-r from-slate-900 to-slate-800">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-white text-lg font-semibold tracking-tight">{title}</CardTitle>
            {description && (
              <CardDescription className="text-slate-300">{description}</CardDescription>
            )}
          </div>
          <div className={cn(
            "flex items-center gap-1 text-sm font-medium px-2 py-1 rounded-full",
            trend > 0 ? "bg-emerald-500/20 text-emerald-400" :
            trend < 0 ? "bg-red-500/20 text-red-400" :
            "bg-slate-500/20 text-slate-300"
          )}>
            {trend > 0 ? <TrendingUp className="w-3 h-3" /> :
             trend < 0 ? <TrendingDown className="w-3 h-3" /> :
             <Minus className="w-3 h-3" />}
            <span>{Math.abs(trend).toFixed(1)}%</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" horizontal={true} vertical={false} />
              <XAxis 
                type="number" 
                domain={[0, maxValue * 1.1]} 
                tick={{ fill: '#64748B', fontSize: 12 }}
                tickLine={{ stroke: '#E2E8F0' }}
                axisLine={{ stroke: '#E2E8F0' }}
              />
              <YAxis 
                type="category" 
                dataKey="name" 
                tick={{ fill: '#1E293B', fontSize: 12, fontWeight: 500 }}
                tickLine={false}
                axisLine={false}
                width={75}
              />
              <Tooltip 
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-slate-900 text-white px-3 py-2 rounded-lg shadow-xl text-sm">
                        <p className="font-medium">{data.fullName}</p>
                        <p className="text-slate-300">{data.value}{unit}</p>
                      </div>
                    );
                  }
                  return null;
                }}
                cursor={{ fill: '#F1F5F9' }}
              />
              <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={28}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
