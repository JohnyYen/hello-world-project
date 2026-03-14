'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend,
  Area,
  ComposedChart 
} from 'recharts';
import type { CourseProgressOverTime, CourseMetrics } from '@/types/course-report.interface';

interface ProgressTrendChartProps {
  data: Record<string, CourseProgressOverTime[]>;
  courses: CourseMetrics[];
  title?: string;
  description?: string;
}

const COLORS = [
  '#1E3A5F', // deep navy
  '#3B82F6', // blue
  '#10B981', // emerald
  '#F59E0B', // amber
  '#EF4444', // red
];

export function ProgressTrendChart({
  data,
  courses,
  title = 'Tendencia de Progreso',
  description = 'Evolución del promedio a lo largo del período'
}: ProgressTrendChartProps) {
  // Combinar datos de múltiples cursos
  const courseKeys = Object.keys(data);
  const months = data[courseKeys[0]]?.map(d => d.date) || [];
  
  // Crear datos combinados
  const combinedData = months.map((month, monthIndex) => {
    const point: Record<string, string | number> = { name: month };
    
    courseKeys.forEach((courseId, courseIndex) => {
      const courseData = data[courseId];
      if (courseData && courseData[monthIndex]) {
        point[courseId] = courseData[monthIndex].averageProgress;
      }
    });
    
    return point;
  });

  return (
    <Card className="overflow-hidden border-0 shadow-lg">
      <CardHeader className="pb-2 bg-gradient-to-r from-slate-900 to-slate-800">
        <CardTitle className="text-white text-lg font-semibold tracking-tight">{title}</CardTitle>
        <CardDescription className="text-slate-300">{description}</CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={combinedData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                {courseKeys.map((courseId, index) => (
                  <linearGradient key={courseId} id={`gradient-${courseId}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={COLORS[index % COLORS.length]} stopOpacity={0.3}/>
                    <stop offset="95%" stopColor={COLORS[index % COLORS.length]} stopOpacity={0}/>
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
              <XAxis 
                dataKey="name" 
                tick={{ fill: '#64748B', fontSize: 12 }}
                tickLine={{ stroke: '#E2E8F0' }}
                axisLine={{ stroke: '#E2E8F0' }}
              />
              <YAxis 
                domain={[0, 100]} 
                tick={{ fill: '#64748B', fontSize: 12 }}
                tickLine={{ stroke: '#E2E8F0' }}
                axisLine={false}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1E293B', 
                  border: 'none', 
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
                labelStyle={{ color: '#F8FAFC', fontWeight: 600, marginBottom: '4px' }}
                itemStyle={{ color: '#CBD5E1', fontSize: '13px' }}
              />
              <Legend 
                verticalAlign="top" 
                height={36}
                iconType="circle"
                formatter={(value) => {
                  const course = courses.find(c => c.courseId === value);
                  return <span style={{ color: '#334155', fontSize: '13px', fontWeight: 500 }}>{course?.courseName}</span>;
                }}
              />
              {courseKeys.map((courseId, index) => (
                <Area
                  key={courseId}
                  type="monotone"
                  dataKey={courseId}
                  stroke={COLORS[index % COLORS.length]}
                  strokeWidth={2.5}
                  fill={`url(#gradient-${courseId})`}
                  dot={{ fill: COLORS[index % COLORS.length], strokeWidth: 0, r: 4 }}
                  activeDot={{ r: 6, strokeWidth: 0 }}
                />
              ))}
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
