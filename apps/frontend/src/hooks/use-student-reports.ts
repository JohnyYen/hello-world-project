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

// Mock data temporal - reemplazar con llamada real a API
const MOCK_KPIS: StudentReportKPIs = {
  totalLevelsCompleted: 12,
  totalGamesPlayed: 28,
  totalPlayTime: 1840,
  averageScore: 85,
  currentStreak: 5,
  lastActivity: "2026-02-25T14:30:00Z",
};

const MOCK_PROGRESS_OVER_TIME: ProgressOverTime[] = [
  { date: "Ene 1", level: 1, score: 75, timeSpent: 120 },
  { date: "Ene 8", level: 2, score: 82, timeSpent: 145 },
  { date: "Ene 15", level: 3, score: 78, timeSpent: 130 },
  { date: "Ene 22", level: 4, score: 90, timeSpent: 110 },
  { date: "Ene 29", level: 5, score: 88, timeSpent: 125 },
  { date: "Feb 5", level: 6, score: 92, timeSpent: 95 },
  { date: "Feb 12", level: 7, score: 85, timeSpent: 140 },
  { date: "Feb 19", level: 8, score: 95, timeSpent: 85 },
  { date: "Feb 26", level: 9, score: 87, timeSpent: 130 },
];

const MOCK_LEVEL_PERFORMANCE: LevelPerformance[] = [
  { levelName: "Nivel 1 - Introducción", score: 85, attempts: 2, timeSpent: 120, completed: true },
  { levelName: "Nivel 2 - Variables", score: 78, attempts: 3, timeSpent: 180, completed: true },
  { levelName: "Nivel 3 - Condicionales", score: 92, attempts: 1, timeSpent: 90, completed: true },
  { levelName: "Nivel 4 - Ciclos", score: 88, attempts: 2, timeSpent: 150, completed: true },
  { levelName: "Nivel 5 - Funciones", score: 75, attempts: 4, timeSpent: 240, completed: true },
  { levelName: "Nivel 6 - Arrays", score: 95, attempts: 1, timeSpent: 85, completed: true },
];

const MOCK_ACTIVITY_DISTRIBUTION: ActivityDistribution[] = [
  { gameName: "Hello World", timeSpent: 720, sessions: 12 },
  { gameName: "Blockly Puzzles", timeSpent: 480, sessions: 8 },
  { gameName: "Code Runner", timeSpent: 360, sessions: 5 },
  { gameName: "Debug Master", timeSpent: 280, sessions: 3 },
];

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
        // Simular llamada a API
        // En producción, usar:
        // const response = await fetch(`/api/v1/users/students/${studentId}/reports`);
        // const data = await response.json();

        // Mock data
        await new Promise((resolve) => setTimeout(resolve, 500));

        setKpis(MOCK_KPIS);
        setProgressOverTime(MOCK_PROGRESS_OVER_TIME);
        setLevelPerformance(MOCK_LEVEL_PERFORMANCE);
        setActivityDistribution(MOCK_ACTIVITY_DISTRIBUTION);
      } catch (err) {
        setError("Error al cargar los datos del reporte");
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
