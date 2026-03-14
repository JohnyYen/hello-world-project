"use client";

import { useMemo, useState } from "react";

interface HeatMapData {
  day: string;
  hour: number;
  value: number;
}

interface HeatMapProps {
  data: HeatMapData[];
  title?: string;
  subtitle?: string;
  height?: number;
  colorScale?: string[];
  showTooltip?: boolean;
  tooltipFormatter?: (value: number, day: string, hour: number) => string;
}

const DEFAULT_COLOR_SCALE = [
  "#F1F5F9", // 0 - No activity (slate-100)
  "#BBF7D0", // 1-20 (green-200)
  "#86EFAC", // 21-40 (green-300)
  "#4ADE80", // 41-60 (green-400)
  "#22C55E", // 61-80 (green-500)
  "#16A34A", // 81-100 (green-600)
  "#15803D", // 101+ (green-700)
];

const DAYS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];
const HOURS = Array.from({ length: 24 }, (_, i) => i);

export function HeatMap({
  data,
  title,
  subtitle,
  height = 320,
  colorScale = DEFAULT_COLOR_SCALE,
  showTooltip = true,
  tooltipFormatter,
}: HeatMapProps) {
  const [hoveredCell, setHoveredCell] = useState<{ day: string; hour: number; value: number } | null>(null);

  const dataMap = useMemo(() => {
    const map = new Map<string, number>();
    data.forEach((item) => {
      map.set(`${item.day}-${item.hour}`, item.value);
    });
    return map;
  }, [data]);

  const maxValue = useMemo(() => {
    return Math.max(...data.map((d) => d.value), 1);
  }, [data]);

  const getColor = (value: number): string => {
    if (value === 0) return colorScale[0];
    const ratio = Math.min(value / maxValue, 1);
    const index = Math.min(Math.floor(ratio * (colorScale.length - 1)) + 1, colorScale.length - 1);
    return colorScale[index];
  };

  const formatHour = (hour: number): string => {
    if (hour === 0) return "12am";
    if (hour === 12) return "12pm";
    return hour < 12 ? `${hour}am` : `${hour - 12}pm`;
  };

  return (
    <div className="rounded-lg border bg-card p-6 shadow-sm">
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="text-lg font-semibold">{title}</h3>}
          {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
        </div>
      )}

      {/* Hour labels */}
      <div className="flex">
        <div className="w-10 flex-shrink-0" />
        <div 
          className="flex-1 grid gap-1" 
          style={{ gridTemplateColumns: `repeat(24, minmax(0, 1fr))` }}
        >
          {HOURS.filter((h) => h % 3 === 0).map((hour) => (
            <div 
              key={hour} 
              className="text-xs text-muted-foreground text-center"
              style={{ gridColumn: "span 3" }}
            >
              {formatHour(hour)}
            </div>
          ))}
        </div>
      </div>

      {/* Grid */}
      <div 
        className="flex flex-col gap-1" 
        style={{ height: Math.max(height - 60, 200) }}
      >
        {DAYS.map((day) => (
          <div key={day} className="flex items-center gap-1">
            {/* Day label */}
            <div className="w-10 flex-shrink-0 text-xs text-muted-foreground">
              {day}
            </div>
            
            {/* Heat cells */}
            <div 
              className="flex-1 grid gap-1" 
              style={{ gridTemplateColumns: "repeat(24, minmax(0, 1fr))" }}
            >
              {HOURS.map((hour) => {
                const key = `${day}-${hour}`;
                const value = dataMap.get(key) || 0;
                const isHovered = hoveredCell?.day === day && hoveredCell?.hour === hour;
                
                return (
                  <div
                    key={key}
                    className="relative rounded-sm transition-all duration-200 cursor-pointer"
                    style={{ 
                      backgroundColor: getColor(value),
                      aspectRatio: "1",
                      transform: isHovered ? "scale(1.2)" : "scale(1)",
                      zIndex: isHovered ? 10 : 1,
                    }}
                    onMouseEnter={() => showTooltip && setHoveredCell({ day, hour, value })}
                    onMouseLeave={() => setHoveredCell(null)}
                  >
                    {isHovered && showTooltip && (
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50">
                        <div className="rounded-lg border bg-card px-3 py-2 shadow-lg text-sm whitespace-nowrap">
                          <p className="font-medium">{day} {formatHour(hour)}</p>
                          <p className="text-muted-foreground">
                            {tooltipFormatter ? tooltipFormatter(value, day, hour) : `${value} minutos`}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex items-center justify-end gap-2 mt-4">
        <span className="text-xs text-muted-foreground">Menos</span>
        <div className="flex gap-1">
          {colorScale.map((color, index) => (
            <div
              key={index}
              className="w-4 h-4 rounded-sm"
              style={{ backgroundColor: color }}
            />
          ))}
        </div>
        <span className="text-xs text-muted-foreground">Más</span>
      </div>
    </div>
  );
}

// Helper to generate mock heatmap data
export function generateHeatMapData(
  days: string[] = DAYS,
  hours: number[] = HOURS
): HeatMapData[] {
  const result: HeatMapData[] = [];
  
  days.forEach((day) => {
    hours.forEach((hour) => {
      // Simulate more activity during school hours (9am-5pm) and weekdays
      const isWeekday = day !== "Sáb" && day !== "Dom";
      const isSchoolHour = hour >= 9 && hour <= 17;
      const isEvening = hour >= 18 && hour <= 21;
      
      let baseValue = 0;
      if (isWeekday && isSchoolHour) {
        baseValue = Math.random() * 60 + 20;
      } else if (isWeekday && isEvening) {
        baseValue = Math.random() * 40 + 10;
      } else if (!isWeekday) {
        baseValue = Math.random() * 30;
      }
      
      // Add some randomness
      const value = Math.round(baseValue + Math.random() * 20);
      
      result.push({ day, hour, value: Math.max(0, value) });
    });
  });
  
  return result;
}
