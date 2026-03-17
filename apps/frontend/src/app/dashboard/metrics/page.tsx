import { MetricsPageClient } from "./metrics-page-client";
import { MetricsKPIServer } from "./metrics-kpi-server";
import { StudentProgressServer } from "./student-progress-server";
import { CourseCompletionServer } from "./course-completion-server";
import { EngagementServer } from "./engagement-server";
import { ActivityPerformanceServer } from "./activity-performance-server";
import { MetricTypesServer } from "./metric-types-server";

export default async function MetricsPage() {
  return (
    <MetricsPageClient
      kpis={<MetricsKPIServer />}
      studentProgress={<StudentProgressServer />}
      courseCompletion={<CourseCompletionServer />}
      engagement={<EngagementServer />}
      activityPerformance={<ActivityPerformanceServer />}
      metricTypes={<MetricTypesServer />}
    />
  );
}
