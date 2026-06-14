"use client";

import { useState, useEffect } from "react";
import type { StudentGameItem } from "@/api/types";

interface UseStudentGamesReturn {
  games: StudentGameItem[];
  isLoading: boolean;
  error: string | null;
}

export function useStudentGames(studentId: string): UseStudentGamesReturn {
  const [games, setGames] = useState<StudentGameItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchGames() {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/statistic/students/${studentId}/games`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          },
        );

        if (!response.ok) {
          if (response.status === 401) {
            throw new Error("No autorizado");
          }
          if (response.status === 403) {
            throw new Error("Sin permisos para ver juegos");
          }
          throw new Error("Error al cargar los juegos");
        }

        const data = await response.json();
        setGames(data.games ?? []);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Error al cargar los juegos");
        }
      } finally {
        setIsLoading(false);
      }
    }

    if (studentId) {
      fetchGames();
    }
  }, [studentId]);

  return { games, isLoading, error };
}
