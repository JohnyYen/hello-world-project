import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { useStudentReports } from "../use-student-reports";

const mockApiResponse = {
  kpis: {
    total_levels_completed: 5,
    total_games_played: 3,
    total_play_time: 120,
    average_score: 85,
    current_streak: 3,
    last_activity: "2026-06-01",
  },
  progress_over_time: [
    { date: "2026-06-01", level: 1, score: 85, time_spent: 30 },
  ],
  level_performance: [
    {
      level_name: "Nivel 1",
      score: 85,
      attempts: 2,
      time_spent: 30,
      completed: true,
    },
  ],
  activity_distribution: [
    { game_name: "Juego 1", time_spent: 30, sessions: 2 },
  ],
  games_progress: [
    {
      game_title: "Matemáticas Básicas",
      confidence_levels_completed: 3,
      total_confidence_levels: 5,
      completion_percentage: 60,
    },
    {
      game_title: "Física Divertida",
      confidence_levels_completed: 2,
      total_confidence_levels: 4,
      completion_percentage: 50,
    },
  ],
};

describe("useStudentReports", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("fetches data with correct URL based on studentId", async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockApiResponse),
    });

    const { result } = renderHook(() => useStudentReports("student-123"));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(global.fetch).toHaveBeenCalledWith(
      "/api/statistic/students/student-123/progress",
      expect.objectContaining({
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      }),
    );
  });

  it("maps snake_case games_progress to camelCase gamesProgress", async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockApiResponse),
    });

    const { result } = renderHook(() => useStudentReports("test-id"));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.gamesProgress).toHaveLength(2);
    expect(result.current.gamesProgress[0]).toEqual({
      gameTitle: "Matemáticas Básicas",
      confidenceLevelsCompleted: 3,
      totalConfidenceLevels: 5,
      completionPercentage: 60,
    });
    expect(result.current.gamesProgress[1]).toEqual({
      gameTitle: "Física Divertida",
      confidenceLevelsCompleted: 2,
      totalConfidenceLevels: 4,
      completionPercentage: 50,
    });
  });

  it("returns empty array when games_progress is null", async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({ ...mockApiResponse, games_progress: null }),
    });

    const { result } = renderHook(() => useStudentReports("test-id"));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.gamesProgress).toEqual([]);
  });

  it("returns empty array when games_progress is missing from response", async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });

    const { result } = renderHook(() => useStudentReports("test-id"));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.gamesProgress).toEqual([]);
  });

  it("sets error message on 404 response", async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 404,
      json: () => Promise.resolve({}),
    });

    const { result } = renderHook(() => useStudentReports("test-id"));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBe(
      "No se encontró progreso para este estudiante",
    );
  });

  it("sets error message on fetch failure", async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValue(
      new Error("Network error"),
    );

    const { result } = renderHook(() => useStudentReports("test-id"));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBe("Network error");
  });
});
