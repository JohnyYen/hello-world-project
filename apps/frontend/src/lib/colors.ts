/**
 * 🎨 Sistema de colores Tech Educativo
 * Colores HEX para uso en componentes y gráficos
 */

export const COLORS = {
  // Primarios
  primary: '#2563EB',
  primaryDark: '#1D4ED8',
  primaryLight: '#DBEAFE',
  
  // Secundarios
  secondary: '#10B981',
  secondaryDark: '#059669',
  secondaryLight: '#D1FAE5',
  
  // Estados semánticos
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',
  
  // Neutros
  background: '#F8FAFC',
  foreground: '#1E293B',
  muted: '#64748B',
  border: '#E2E8F0',
  card: '#FFFFFF',
  
  // Gráficos
  chart: {
    blue: '#2563EB',
    green: '#10B981',
    amber: '#F59E0B',
    red: '#EF4444',
    purple: '#8B5CF6',
    orange: '#F97316',
    cyan: '#06B6D4',
    pink: '#EC4899',
  }
} as const;

// Array para gráficos con múltiples series
export const CHART_COLORS_ARRAY = [
  COLORS.chart.blue,
  COLORS.chart.green,
  COLORS.chart.amber,
  COLORS.chart.red,
  COLORS.chart.purple,
  COLORS.chart.orange,
  COLORS.chart.cyan,
  COLORS.chart.pink,
];

// Colores para badges de estado usando clases de Tailwind
export const BADGE_VARIANTS = {
  success: 'bg-emerald-100 text-emerald-800 border-emerald-200 hover:bg-emerald-200',
  warning: 'bg-amber-100 text-amber-800 border-amber-200 hover:bg-amber-200',
  error: 'bg-red-100 text-red-800 border-red-200 hover:bg-red-200',
  info: 'bg-blue-100 text-blue-800 border-blue-200 hover:bg-blue-200',
  neutral: 'bg-slate-100 text-slate-800 border-slate-200 hover:bg-slate-200',
  primary: 'bg-blue-100 text-blue-800 border-blue-200 hover:bg-blue-200',
} as const;
