/**
 * Server-side data fetcher for metrics overview.
 * Uses cookies() from next/headers to authenticate, calls the backend directly.
 * This avoids the extra hop through the Next.js API proxy route.
 *
 * All server components in /dashboard/metrics use this to fetch real data.
 */

import "server-only";
import { cookies } from "next/headers";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// ─── Raw Backend Types (snake_case) ─────────────────────────────────────────

interface RawKPIs {
  total_students: number;
  active_students_this_week: number;
  active_students_this_month: number;
  total_levels_completed: number;
  total_play_time_minutes: number;
  average_score: number;
}

interface RawActivityOverTimeItem {
  date: string;
  sessions: number;
  active_students: number;
  play_time_minutes: number;
}

interface RawLevelPerformanceItem {
  game_name: string;
  level_name: string;
  completion_rate: number;
  average_attempts: number;
  average_time_minutes: number;
}

interface RawTrends {
  students_change_percent: number;
  activity_change_percent: number;
  score_change_percent: number;
}

interface RawOverviewResponse {
  kpis: RawKPIs;
  activity_over_time: RawActivityOverTimeItem[];
  level_performance: RawLevelPerformanceItem[];
  trends: RawTrends;
}

// ─── Mapped Types (camelCase) ───────────────────────────────────────────────

export interface MetricsKPIs {
  totalStudents: number;
  activeStudentsThisWeek: number;
  activeStudentsThisMonth: number;
  totalLevelsCompleted: number;
  totalPlayTimeMinutes: number;
  averageScore: number;
}

export interface ActivityOverTimeItem {
  date: string;
  sessions: number;
  activeStudents: number;
  playTimeMinutes: number;
}

export interface LevelPerformanceItem {
  gameName: string;
  levelName: string;
  completionRate: number; // 0-1
  averageAttempts: number;
  averageTimeMinutes: number;
}

export interface Trends {
  studentsChangePercent: number;
  activityChangePercent: number;
  scoreChangePercent: number;
}

export interface MetricsOverview {
  kpis: MetricsKPIs;
  activityOverTime: ActivityOverTimeItem[];
  levelPerformance: LevelPerformanceItem[];
  trends: Trends;
}

// ─── Mapping ────────────────────────────────────────────────────────────────

function mapOverview(raw: RawOverviewResponse): MetricsOverview {
  return {
    kpis: {
      totalStudents: raw.kpis.total_students,
      activeStudentsThisWeek: raw.kpis.active_students_this_week,
      activeStudentsThisMonth: raw.kpis.active_students_this_month,
      totalLevelsCompleted: raw.kpis.total_levels_completed,
      totalPlayTimeMinutes: raw.kpis.total_play_time_minutes,
      averageScore: raw.kpis.average_score,
    },
    activityOverTime: raw.activity_over_time.map((item) => ({
      date: item.date,
      sessions: item.sessions,
      activeStudents: item.active_students,
      playTimeMinutes: item.play_time_minutes,
    })),
    levelPerformance: raw.level_performance.map((item) => ({
      gameName: item.game_name,
      levelName: item.level_name,
      completionRate: item.completion_rate,
      averageAttempts: item.average_attempts,
      averageTimeMinutes: item.average_time_minutes,
    })),
    trends: {
      studentsChangePercent: raw.trends.students_change_percent,
      activityChangePercent: raw.trends.activity_change_percent,
      scoreChangePercent: raw.trends.score_change_percent,
    },
  };
}

// ─── Public API ─────────────────────────────────────────────────────────────

/**
 * Fetch metrics overview from the backend.
 * Called from Server Components — uses cookies for auth.
 * Cached with Next.js fetch cache (revalidate: 300s = 5 min).
 */
export async function getMetricsOverview(
  period: "7d" | "30d" | "3m" = "30d"
): Promise<MetricsOverview> {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;

  if (!token) {
    throw new Error("No autorizado");
  }

  const res = await fetch(
    `${API_BASE_URL}/api/v1/statistic/overview?period=${period}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      next: { revalidate: 300, tags: ["metrics-overview"] },
    }
  );

  if (!res.ok) {
    if (res.status === 401) {
      throw new Error("No autorizado. Por favor, inicia sesión.");
    }
    throw new Error(`Error al cargar métricas: ${res.status}`);
  }

  const raw: RawOverviewResponse = await res.json();
  return mapOverview(raw);
}
