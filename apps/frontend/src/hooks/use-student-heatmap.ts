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

export function useStudentHeatmap(studentId: string, days: number = 30): UseStudentHeatmapReturn {
  const [heatmapData, setHeatmapData] = useState<HeatMapData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchHeatmap() {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/users/students/${studentId}/activity/heatmap?days=${days}`,
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