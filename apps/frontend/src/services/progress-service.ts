import { apiClient, APIClient } from "@/lib/api-client";
import type { ApiResponse } from "@/types/api";

// ─── Backend response types (snake_case, matches Pydantic schema) ─────────

export interface ProgressKPI {
  total_levels_completed: number;
  total_games_played: number;
  total_play_time: number;
  average_score: number;
  current_streak: number;
  last_activity: string | null;
}

export interface ProgressOverTimeEntry {
  date: string;
  level: number;
  score: number;
  time_spent: number;
}

export interface LevelPerformanceEntry {
  level_name: string;
  score: number;
  attempts: number;
  time_spent: number;
  completed: boolean;
}

export interface ActivityDistributionEntry {
  game_name: string;
  time_spent: number;
  sessions: number;
}

export interface StudentProgressResponse {
  student_id: string;
  kpis: ProgressKPI;
  progress_over_time: ProgressOverTimeEntry[];
  level_performance: LevelPerformanceEntry[];
  activity_distribution: ActivityDistributionEntry[];
}

// ─── Service ────────────────────────────────────────────────────────────

export class ProgressService {
  constructor(private _client: APIClient) {}

  private getBaseUrl(studentId: string): string {
    if (typeof window !== "undefined") {
      return `/api/statistic/students/${studentId}/progress`;
    }
    return `${this._client["baseURL"]}/api/v1/statistic/students/${studentId}/progress`;
  }

  async getStudentProgress(studentId: string): Promise<ApiResponse<StudentProgressResponse>> {
    return this._client.get<StudentProgressResponse>(this.getBaseUrl(studentId), {
      next: { revalidate: 1800 },
    });
  }
}

export const progressService = new ProgressService(apiClient);
