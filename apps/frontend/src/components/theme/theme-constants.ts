export type ColorThemeName = "Indigo" | "Violeta" | "Esmeralda" | "Azul" | "Rosa" | "Naranja";

export const COLOR_MAP: Record<ColorThemeName, Record<string, string>> = {
  Indigo: {
    "--theme-primary": "#6366f1",
    "--theme-accent": "#8b5cf6",
    "--theme-ring": "#6366f1",
    "--primary": "#6366f1",
    "--chart-1": "#6366f1",
  },
  Violeta: {
    "--theme-primary": "#8b5cf6",
    "--theme-accent": "#a855f7",
    "--theme-ring": "#8b5cf6",
    "--primary": "#8b5cf6",
    "--chart-1": "#8b5cf6",
  },
  Esmeralda: {
    "--theme-primary": "#10b981",
    "--theme-accent": "#34d399",
    "--theme-ring": "#10b981",
    "--primary": "#10b981",
    "--chart-1": "#10b981",
  },
  Azul: {
    "--theme-primary": "#3b82f6",
    "--theme-accent": "#60a5fa",
    "--theme-ring": "#3b82f6",
    "--primary": "#3b82f6",
    "--chart-1": "#3b82f6",
  },
  Rosa: {
    "--theme-primary": "#ec4899",
    "--theme-accent": "#f472b6",
    "--theme-ring": "#ec4899",
    "--primary": "#ec4899",
    "--chart-1": "#ec4899",
  },
  Naranja: {
    "--theme-primary": "#f97316",
    "--theme-accent": "#fb923c",
    "--theme-ring": "#f97316",
    "--primary": "#f97316",
    "--chart-1": "#f97316",
  },
};

export const DEFAULT_COLOR_THEME: ColorThemeName = "Indigo";