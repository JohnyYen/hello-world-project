"use client";

import { useState, useEffect } from "react";
import {
  OverviewKPIs,
  ActivityOverTimeItem,
  LevelPerformanceItem,
  OverviewTrends,
} from "@/types/api";

interface UseDashboardStatsReturn {
  kpis: OverviewKPIs | null;
  activityOverTime: ActivityOverTimeItem[];
  levelPerformance: LevelPerformanceItem[];
  trends: OverviewTrends | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => void;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function useDashboardStats(
  period: "7d" | "30d" | "3m" = "30d"
): UseDashboardStatsReturn {
  const [kpis, setKpis] = useState<OverviewKPIs | null>(null);
  const [activityOverTime, setActivityOverTime] = useState<ActivityOverTimeItem[]>([]);
  const [levelPerformance, setLevelPerformance] = useState<LevelPerformanceItem[]>([]);
  const [trends, setTrends] = useState<OverviewTrends | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/statistic/overview?period=${period}`,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("No autorizado");
        }
        throw new Error("Error al cargar las estadísticas");
      }

      const data = await response.json();

      setKpis({
        totalStudents: data.kpis.total_students,
        activeStudentsThisWeek: data.kpis.active_students_this_week,
        activeStudentsThisMonth: data.kpis.active_students_this_month,
        totalLevelsCompleted: data.kpis.total_levels_completed,
        totalPlayTimeMinutes: data.kpis.total_play_time_minutes,
        averageScore: data.kpis.average_score,
      });

      setActivityOverTime(
        data.activity_over_time.map((item: { date: string; sessions: number; active_students: number; play_time_minutes: number }) => ({
          date: item.date,
          sessions: item.sessions,
          activeStudents: item.active_students,
          playTimeMinutes: item.play_time_minutes,
        }))
      );

      setLevelPerformance(
        data.level_performance.map((item: { level_name: string; completion_rate: number; average_attempts: number; average_time_minutes: number }) => ({
          levelName: item.level_name,
          completionRate: item.completion_rate,
          averageAttempts: item.average_attempts,
          averageTimeMinutes: item.average_time_minutes,
        }))
      );

      setTrends({
        studentsChangePercent: data.trends.students_change_percent,
        activityChangePercent: data.trends.activity_change_percent,
        scoreChangePercent: data.trends.score_change_percent,
      });
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Error al cargar las estadísticas del dashboard");
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [period]);

  return {
    kpis,
    activityOverTime,
    levelPerformance,
    trends,
    isLoading,
    error,
    refetch: fetchData,
  };
}
