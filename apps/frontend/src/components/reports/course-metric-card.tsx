'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus, Clock, Users, Target, Award } from 'lucide-react';
import type { CourseMetrics } from '@/types/course-report.interface';

interface CourseMetricCardProps {
  course: CourseMetrics;
  metric: keyof CourseMetrics;
  label: string;
  icon: 'progress' | 'grade' | 'completion' | 'engagement' | 'activeTime' | 'sessions';
  format?: 'percentage' | 'number' | 'minutes';
}

const ICONS = {
  progress: Target,
  grade: Award,
  completion: TrendingUp,
  engagement: Users,
  activeTime: Clock,
  sessions: Users,
};

const TREND_ICONS = {
  progress: TrendingUp,
  grade: TrendingUp,
  completion: TrendingUp,
  engagement: TrendingUp,
  activeTime: TrendingUp,
  sessions: TrendingUp,
};

export function CourseMetricCard({
  course,
  metric,
  label,
  icon,
  format = 'percentage'
}: CourseMetricCardProps) {
  const Icon = ICONS[icon];
  const TrendIcon = TREND_ICONS[icon];
  
  const value = course[metric] as number;
  const trendKey = `${metric}Trend` as keyof CourseMetrics;
  const trend = course[trendKey] as number;
  
  const formatValue = (val: number) => {
    switch (format) {
      case 'minutes':
        return `${Math.round(val)} min`;
      case 'number':
        return val.toString();
      default:
        return `${Math.round(val)}%`;
    }
  };

  const getTrendColor = (t: number) => {
    if (t > 0) return 'text-accent bg-accent/10';
    if (t < 0) return 'text-red-600 bg-red-50';
    return 'text-slate-500 bg-slate-50';
  };

  return (
    <Card className="border-0 shadow-md hover:shadow-lg transition-shadow duration-200">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium text-slate-600">
            {label}
          </CardTitle>
          <Icon className="h-4 w-4 text-slate-400" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-end justify-between">
          <div className="text-3xl font-bold text-slate-900">
            {formatValue(value)}
          </div>
          <div className={cn(
            "flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full",
            getTrendColor(trend)
          )}>
            {trend > 0 ? <TrendingUp className="w-3 h-3" /> :
             trend < 0 ? <TrendingDown className="w-3 h-3" /> :
             <Minus className="w-3 h-3" />}
            <span>{Math.abs(trend).toFixed(1)}%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

interface CourseMetricsGridProps {
  course: CourseMetrics;
}

export function CourseMetricsGrid({ course }: CourseMetricsGridProps) {
  const metrics = [
    { key: 'averageProgress' as const, label: 'Progreso Promedio', icon: 'progress' as const },
    { key: 'averageGrade' as const, label: 'Calificación Promedio', icon: 'grade' as const },
    { key: 'completionRate' as const, label: 'Tasa de Completado', icon: 'completion' as const },
    { key: 'dailyActiveUsers' as const, label: 'Usuarios Activos/Día', icon: 'engagement' as const, format: 'number' as const },
    { key: 'averageActiveTime' as const, label: 'Tiempo Activo Promedio', icon: 'activeTime' as const, format: 'minutes' as const },
    { key: 'averageSessionsPerStudent' as const, label: 'Sesiones/Estudiante', icon: 'sessions' as const, format: 'number' as const },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      {metrics.map((m) => (
        <CourseMetricCard
          key={m.key}
          course={course}
          metric={m.key}
          label={m.label}
          icon={m.icon}
          format={m.format}
        />
      ))}
    </div>
  );
}
