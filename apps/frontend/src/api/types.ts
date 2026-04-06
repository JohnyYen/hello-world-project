/**
 * API types for the backend services.
 * All ID fields are strings (UUIDs serialized as strings).
 */

// ─── Shared ────────────────────────────────────────────────────────────────

export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T | null;
  error?: T | null;
}

// ─── Auth ──────────────────────────────────────────────────────────────────

export interface UserLoginRequest {
  username?: string;
  email?: string;
  password: string;
}

export interface UserCreateRequest {
  username: string;
  email: string;
  name: string;
  lastname?: string;
  password: string;
}

export interface UserChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

export interface UserRoleResponse {
  id: string;
  name: string;
}

export interface UserResponse {
  id: string;
  username: string;
  email: string;
  name: string;
  lastname: string | null;
  is_active: boolean;
  role: UserRoleResponse | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface UserLoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: UserResponse;
}

export type SingleUserResponse = ApiResponse<UserResponse>;
export type UserListResponse = ApiResponse<UserResponse[]>;

// ─── Teacher ───────────────────────────────────────────────────────────────

export interface TeacherProfileResponse {
  id: string;
  username: string;
  name: string;
  lastname: string;
  email: string;
  department: string;
  contact_phone: string | null;
  avatar_url: string | null;
  is_active: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface TeacherProfileUpdate {
  name?: string;
  lastname?: string;
  email?: string;
  department?: string;
  contact_phone?: string;
  avatar_url?: string;
}

export type TeacherProfileResponseSchema = ApiResponse<TeacherProfileResponse>;
export type TeacherUpdateResponseSchema = ApiResponse<TeacherProfileResponse>;

export interface TeacherSettingsResponse {
  theme?: "light" | "dark";
  notifications_enabled?: boolean;
  notification_frequency?: "realtime" | "daily" | "weekly" | "disabled";
  interface_language?: "es" | "en";
  auto_logout?: boolean;
  remember_login?: boolean;
  animations_enabled?: boolean;
  email_notifications?: boolean;
  session_duration_minutes?: number;
  color_theme?: "Indigo" | "Violeta" | "Esmeralda" | "Azul" | "Rosa" | "Naranja";
  date_format?: "ddmmyyyy" | "mmddyyyy" | "yyyymmdd";
  timezone?: "gmt-5" | "gmt-6" | "gmt-3" | "gmt0" | "gmt1";
}

export type TeacherSettingsResponseSchema = ApiResponse<TeacherSettingsResponse>;

export interface TeacherSettingsUpdate {
  theme?: "light" | "dark";
  notifications_enabled?: boolean;
  notification_frequency?: "realtime" | "daily" | "weekly" | "disabled";
  interface_language?: "es" | "en";
  auto_logout?: boolean;
  remember_login?: boolean;
  animations_enabled?: boolean;
  email_notifications?: boolean;
  session_duration_minutes?: number;
  color_theme?: "Indigo" | "Violeta" | "Esmeralda" | "Azul" | "Rosa" | "Naranja";
  date_format?: "ddmmyyyy" | "mmddyyyy" | "yyyymmdd";
  timezone?: "gmt-5" | "gmt-6" | "gmt-3" | "gmt0" | "gmt1";
}

// ─── Student ───────────────────────────────────────────────────────────────

export interface StudentResponse {
  id: string;
  username: string;
  email: string;
  name: string;
  lastname: string;
  is_active: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface StudentCreate {
  username: string;
  email: string;
  name: string;
  lastname: string;
  password: string;
  is_active?: boolean;
}

export interface StudentUpdate {
  username?: string;
  email?: string;
  name?: string;
  lastname?: string;
  is_active?: boolean;
}

export type StudentListResponse = ApiResponse<StudentResponse[]>;
export type StudentProgressResponse = ApiResponse<Record<string, unknown>>;
export type StudentReportsResponse = ApiResponse<Record<string, unknown>>;

// ─── Game ──────────────────────────────────────────────────────────────────

export interface GameBase {
  title: string;
  description?: string;
  creator?: string;
  subject?: string;
  publication_status?: string;
}

export interface GameResponse extends GameBase {
  id: string;
  created_at: string;
  updated_at: string | null;
  is_deleted: boolean;
}

export interface GameDetailResponse extends GameResponse {
  levels_count: number;
}

export interface GameCreate extends GameBase {}

export interface GameUpdate {
  title?: string;
  description?: string;
  creator?: string;
  subject?: string;
  publication_status?: string;
}

export type GameListResponse = ApiResponse<GameResponse[]> & {
  total?: number;
  skip?: number;
  limit?: number;
};

export type SingleGameResponse = ApiResponse<GameDetailResponse>;
export type GameCreateResponse = ApiResponse<GameResponse>;
export type GameUpdateResponse = ApiResponse<GameResponse>;
export type GameDeleteResponse = { success: boolean; message: string };

// ─── Level ─────────────────────────────────────────────────────────────────

export interface LevelBase {
  level_number: number;
  title: string;
  description?: string;
  goal?: string;
}

export interface LevelResponse extends LevelBase {
  id: string;
  game_id: string;
  created_at: string;
  updated_at: string | null;
  is_deleted: boolean;
}

export interface LevelDetailResponse extends LevelResponse {
  segments_count: number;
}

export interface LevelCreate extends LevelBase {
  game_id?: string;
}

export interface LevelUpdate {
  level_number?: number;
  title?: string;
  description?: string;
  goal?: string;
}

export type LevelListResponse = ApiResponse<LevelResponse[]> & { total?: number };
export type SingleLevelResponse = ApiResponse<LevelDetailResponse>;
export type LevelCreateResponse = ApiResponse<LevelResponse>;
export type LevelUpdateResponse = ApiResponse<LevelResponse>;
export type LevelDeleteResponse = { success: boolean; message: string };

// ─── Game Instance ─────────────────────────────────────────────────────────

export interface GameInstanceResponse {
  id: string;
  game_id: string;
  student_id: string;
  status: string;
  started_at: string;
  ended_at: string | null;
  created_at: string;
  updated_at: string | null;
  is_deleted: boolean;
}

export interface GameInstanceCreate {
  game_id?: string;
  student_id: string;
  status?: string;
}

export interface GameInstanceEnd {
  status?: string;
}

export type GameInstanceListResponse = ApiResponse<GameInstanceResponse[]>;
export type SingleGameInstanceResponse = ApiResponse<GameInstanceResponse & {
  game_title?: string;
  student_username?: string;
}>;
export type GameInstanceCreateResponse = ApiResponse<GameInstanceResponse>;
export type GameInstanceEndResponse = ApiResponse<GameInstanceResponse>;

// ─── Segment Level ─────────────────────────────────────────────────────────

export interface SegmentLevelResponse {
  id: string;
  level_id: string;
  configuration: Record<string, unknown> | null;
  created_at: string;
  updated_at: string | null;
  is_deleted: boolean;
}

export interface SegmentLevelCreate {
  level_id?: string;
  configuration?: Record<string, unknown>;
}

export interface SegmentLevelUpdate {
  configuration?: Record<string, unknown>;
}

export type SegmentLevelListResponse = ApiResponse<SegmentLevelResponse[]>;
export type SegmentLevelCreateResponse = ApiResponse<SegmentLevelResponse>;
export type SegmentLevelUpdateResponse = ApiResponse<SegmentLevelResponse>;
export type SegmentLevelDeleteResponse = { success: boolean; message: string };

// ─── LMS ───────────────────────────────────────────────────────────────────

export interface LMSCredentialCreate {
  user_id: string;
  lms_url: string;
  lms_email: string;
  lms_password: string;
  lms_provider: string;
}

export interface LMSCredentialResponse {
  id: string;
  user_id: string;
  lms_url: string | null;
  lms_email: string;
  lms_provider: string;
  access_token: string | null;
  expire_at: string | null;
  created_at: string;
  updated_at: string | null;
}

export type LMSCredentialListResponse = ApiResponse<LMSCredentialResponse[]>;

export interface SyncResultResponse {
  success: boolean;
  message: string;
  data?: Record<string, unknown>;
}

// ─── Sync ──────────────────────────────────────────────────────────────────

export interface SyncSessionCreate {
  instance_id: string;
}

export interface SyncSessionSchema {
  id: string;
  instance_id: string;
  is_active: boolean;
  start_time: string;
  end_time: string | null;
}

export interface SyncEventCreate {
  sync_session_id: string;
  event_type: string;
  payload?: Record<string, unknown>;
  timestamp: string;
  status?: string;
}

export interface SyncEventSchema {
  id: string;
  sync_session_id: string;
  event_type: string;
  payload: Record<string, unknown> | null;
  timestamp: string;
  status: string | null;
}

export type SyncSessionListResponse = ApiResponse<SyncSessionSchema[]>;
export type SyncEventListResponse = ApiResponse<SyncEventSchema[]>;

// ─── Dashboard / Overview ──────────────────────────────────────────────────

export interface OverviewKPIs {
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
  levelName: string;
  completionRate: number;
  averageAttempts: number;
  averageTimeMinutes: number;
}

export interface OverviewTrends {
  studentsChangePercent: number;
  activityChangePercent: number;
  scoreChangePercent: number;
}

export interface OverviewResponse {
  kpis: OverviewKPIs;
  activity_over_time: ActivityOverTimeItem[];
  level_performance: LevelPerformanceItem[];
  trends: OverviewTrends;
}

// ─── Student Reports ───────────────────────────────────────────────────────

export interface StudentReportKPIs {
  totalLevelsCompleted: number;
  totalGamesPlayed: number;
  totalPlayTime: number;
  averageScore: number;
  currentStreak: number;
  lastActivity: string;
}

export interface ProgressOverTimeItem {
  date: string;
  level: number;
  score: number;
  timeSpent: number;
}

export interface LevelPerformance {
  levelName: string;
  score: number;
  attempts: number;
  timeSpent: number;
  completed: boolean;
}

export interface ActivityDistributionItem {
  gameName: string;
  timeSpent: number;
  sessions: number;
}

export interface StudentProgressReport {
  student_id: string;
  kpis: StudentReportKPIs;
  progress_over_time: ProgressOverTimeItem[];
  level_performance: LevelPerformance[];
  activity_distribution: ActivityDistributionItem[];
}
