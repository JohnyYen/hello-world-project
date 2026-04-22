import type { TeacherSettingsResponse } from "@/api/types";

export interface AppearanceSettings extends Pick<TeacherSettingsResponse, "theme" | "color_theme" | "animations_enabled"> {
  colorTheme: TeacherSettingsResponse["color_theme"];
  animationsEnabled: TeacherSettingsResponse["animations_enabled"];
}

export type ThemeMode = "light" | "dark";
export type ColorThemeName = "Indigo" | "Violeta" | "Esmeralda" | "Azul" | "Rosa" | "Naranja";