"use client";

import { useState, useEffect } from "react";

interface StudentActivity {
  lastActiveAt: string | null;
  currentStreakDays: boolean;
  activeToday: boolean;
}

interface UseStudentActivityReturn {
  activity: StudentActivity | null;
  isLoading: boolean;
  error: string | null;
}

export function useStudentActivity(studentId: string): UseStudentActivityReturn {
  const [activity, setActivity] = useState<StudentActivity | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchActivity() {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/users/students/${studentId}`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );

        if (!response.ok) {
          throw new Error("Error al cargar datos de actividad");
        }

        const data = await response.json();

        setActivity({
          lastActiveAt: data.last_active_at,
          currentStreakDays: data.current_streak_days,
          activeToday: data.active_today,
        });
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Error al cargar datos de actividad");
        }
      } finally {
        setIsLoading(false);
      }
    }

    if (studentId) {
      fetchActivity();
    }
  }, [studentId]);

  return {
    activity,
    isLoading,
    error,
  };
}