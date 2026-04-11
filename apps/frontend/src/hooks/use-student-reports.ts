"use client";

import { useState, useEffect } from "react";
import {
  StudentReportKPIs,
  ProgressOverTime,
  LevelPerformance,
  ActivityDistribution,
} from "@/types/api";

interface UseStudentReportsReturn {
  kpis: StudentReportKPIs | null;
  progressOverTime: ProgressOverTime[];
  levelPerformance: LevelPerformance[];
  activityDistribution: ActivityDistribution[];
  isLoading: boolean;
  error: string | null;
}

export function useStudentReports(studentId: string): UseStudentReportsReturn {
  const [kpis, setKpis] = useState<StudentReportKPIs | null>(null);
  const [progressOverTime, setProgressOverTime] = useState<ProgressOverTime[]>([]);
  const [levelPerformance, setLevelPerformance] = useState<LevelPerformance[]>([]);
  const [activityDistribution, setActivityDistribution] = useState<ActivityDistribution[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      setIsLoading(true);
      setError(null);

      try {
        // Use local API route which proxies to backend with auth token
        const response = await fetch(
          `/api/statistic/students/${studentId}/progress`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );

        if (!response.ok) {
          if (response.status === 404) {
            throw new Error("No se encontró progreso para este estudiante");
          }
          if (response.status === 401) {
            throw new Error("No autorizado");
          }
          throw new Error("Error al cargar los datos del reporte");
        }

        const data = await response.json();

        setKpis({
          totalLevelsCompleted: data.kpis.total_levels_completed,
          totalGamesPlayed: data.kpis.total_games_played,
          totalPlayTime: data.kpis.total_play_time,
          averageScore: data.kpis.average_score,
          currentStreak: data.kpis.current_streak,
          lastActivity: data.kpis.last_activity,
        });

        setProgressOverTime(
          data.progress_over_time.map((item: { date: string; level: number; score: number; time_spent: number }) => ({
            date: item.date,
            level: item.level,
            score: item.score,
            timeSpent: item.time_spent,
          }))
        );

        setLevelPerformance(
          data.level_performance.map((item: { level_name: string; score: number; attempts: number; time_spent: number; completed: boolean }) => ({
            levelName: item.level_name,
            score: item.score,
            attempts: item.attempts,
            timeSpent: item.time_spent,
            completed: item.completed,
          }))
        );

        setActivityDistribution(
          data.activity_distribution.map((item: { game_name: string; time_spent: number; sessions: number }) => ({
            gameName: item.game_name,
            timeSpent: item.time_spent,
            sessions: item.sessions,
          }))
        );
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Error al cargar los datos del reporte");
        }
      } finally {
        setIsLoading(false);
      }
    }

    if (studentId) {
      fetchData();
    }
  }, [studentId]);

  return {
    kpis,
    progressOverTime,
    levelPerformance,
    activityDistribution,
    isLoading,
    error,
  };
}
