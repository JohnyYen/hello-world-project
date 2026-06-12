"use client";

import { useState, useEffect } from "react";

interface HeatMapDataPoint {
  day: string;
  hour: number;
  value: number;
}

interface HeatMapData {
  student_id: string;
  days: number;
  data: HeatMapDataPoint[];
  total_activities: number;
}

interface UseStudentHeatmapReturn {
  heatmapData: HeatMapData | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * Detecta la zona horaria del navegador en formato IANA.
 *
 * Ejemplos: ``America/Caracas``, ``Europe/Madrid``, ``America/Argentina/Buenos_Aires``
 */
function detectBrowserTimezone(): string {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  } catch {
    // Fallback: calcular offset UTC
    const offset = -new Date().getTimezoneOffset();
    const hours = Math.floor(Math.abs(offset) / 60);
    const minutes = Math.abs(offset) % 60;
    const sign = offset >= 0 ? "+" : "-";
    return `${sign}${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}`;
  }
}

export function useStudentHeatmap(studentId: string, days: number = 30): UseStudentHeatmapReturn {
  const [heatmapData, setHeatmapData] = useState<HeatMapData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchHeatmap() {
      setIsLoading(true);
      setError(null);

      try {
        const timezone = encodeURIComponent(detectBrowserTimezone());
        const response = await fetch(
          `/api/users/students/${studentId}/activity/heatmap?days=${days}&timezone=${timezone}`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );

        if (!response.ok) {
          throw new Error("Error al cargar datos del heatmap");
        }

        const data = await response.json();
        setHeatmapData(data);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Error al cargar datos del heatmap");
        }
      } finally {
        setIsLoading(false);
      }
    }

    if (studentId) {
      fetchHeatmap();
    }
  }, [studentId, days]);

  return {
    heatmapData,
    isLoading,
    error,
  };
}