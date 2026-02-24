'use client';

import { useState, useEffect, useRef } from 'react';
import { 
  getMetricSummary, 
  getStudentProgress, 
  getCourseCompletion, 
  getDailyActivity, 
  getActivityPerformance
} from '@/components/metrics/metrics-data-provider';
import MetricsSummary from '@/components/metrics/metrics-summary';
import StudentProgressChart from '@/components/metrics/student-progress-chart';
import CourseCompletionChart from '@/components/metrics/course-completion-chart';
import EngagementMetrics from '@/components/metrics/engagement-metrics';
import ActivityPerformanceChart from '@/components/metrics/activity-performance-chart';
import { LoadingState } from '@/components/ui/loading-state';

// Types for data - defined outside component to prevent re-creation
 type MetricSummary = {
  totalStudents: number;
  activeStudents: number;
  avgCompletionRate: number;
  avgScore: number;
  totalCourses: number;
  activeCourses: number;
};

 type StudentProgress = {
  id: string;
  name: string;
  progress: number;
  score: number;
  lastActivity: string;
};

 type CourseCompletion = {
  courseId: string;
  courseName: string;
  completionRate: number;
  enrolled: number;
  completed: number;
};

 type DailyActivity = {
  date: string;
  activityCount: number;
  avgTimeSpent: number;
};

 type ActivityPerformance = {
  activityId: string;
  name: string;
  avgScore: number;
  completionRate: number;
  difficulty: number;
};

export default function MetricsPage() {
  const [loading, setLoading] = useState<boolean>(true);
  const [metricSummary, setMetricSummary] = useState<MetricSummary | null>(null);
  const [studentProgress, setStudentProgress] = useState<StudentProgress[]>([]);
  const [courseCompletion, setCourseCompletion] = useState<CourseCompletion[]>([]);
  const [dailyActivity, setDailyActivity] = useState<DailyActivity[]>([]);
  const [activityPerformance, setActivityPerformance] = useState<ActivityPerformance[]>([]);
  
  // Use ref to prevent state updates if component unmounts
  const isMounted = useRef(true);

  useEffect(() => {
    // Set mounted flag
    isMounted.current = true;
    
    const loadMetricsData = async () => {
      // Prevent multiple simultaneous loads
      if (!loading) return;
      
      try {
        // Fetch all metrics data in parallel
        const [
          summary,
          studentProgressData,
          courseCompletionData,
          dailyActivityData,
          activityPerformanceData
        ] = await Promise.all([
          getMetricSummary(),
          getStudentProgress(),
          getCourseCompletion(),
          getDailyActivity(),
          getActivityPerformance()
        ]);
        
        // Only update state if component is still mounted
        if (isMounted.current) {
          setMetricSummary(summary);
          setStudentProgress(studentProgressData);
          setCourseCompletion(courseCompletionData);
          setDailyActivity(dailyActivityData);
          setActivityPerformance(activityPerformanceData);
          setLoading(false);
        }
      } catch (error) {
        // eslint-disable-next-line no-console -- Log error for debugging metrics loading
        console.error('Error loading metrics data:', error);
        if (isMounted.current) {
          setLoading(false);
        }
      }
    };

    loadMetricsData();
    
    // Cleanup function to prevent state updates after unmount
    return () => {
      isMounted.current = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty dependency array - only run once on mount

  if (loading || !metricSummary) {
    return (
      <div className="container mx-auto py-10">
        <LoadingState message="Cargando métricas..." size="lg" />
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Métricas del Sistema</h1>
        <p className="text-muted-foreground">Visualización y análisis del rendimiento del sistema educativo</p>
      </div>

      <MetricsSummary 
        totalStudents={metricSummary.totalStudents}
        activeStudents={metricSummary.activeStudents}
        avgCompletionRate={metricSummary.avgCompletionRate}
        avgScore={metricSummary.avgScore}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <StudentProgressChart students={studentProgress} />
        <CourseCompletionChart courses={courseCompletion} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <EngagementMetrics dailyActivity={dailyActivity} />
        <ActivityPerformanceChart activities={activityPerformance} />
      </div>
    </div>
  );
}