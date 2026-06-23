"use client";

import { useRef, useMemo, useState, useEffect } from "react";

interface BarChartProps<T> {
  data: T[];
  bars: {
    dataKey: string;
    name: string;
    color?: string;
  }[];
  xAxisDataKey: string;
  title?: string;
  subtitle?: string;
  yAxisLabel?: string;
  height?: number;
  layout?: "horizontal" | "vertical";
  yAxisDomain?: [number, number];
  tooltipFormatter?: (value: number, name: string) => string;
  tooltipLabelFormatter?: (label: string, item: T) => string;
  /** Optional function to compute fill color per data point. */
  barFill?: (entry: T, index: number) => string;
  hideLegend?: boolean;
  /** Passthrough */
  xAxisLabel?: string;
  showAnimation?: boolean;
  showGrid?: boolean;
  stacked?: boolean;
}

function useContainerWidth(ref: React.RefObject<HTMLDivElement | null>): number {
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const measure = () => { const w = el.clientWidth; if (w > 0) setWidth(w); };
    measure();
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const w = entry.contentRect.width;
        if (w > 0) setWidth(w);
      }
    });
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  return width;
}

export function BarChart<T>({
  data,
  bars,
  xAxisDataKey,
  title,
  subtitle,
  yAxisLabel,
  height = 300,
  layout = "horizontal",
  yAxisDomain,
  tooltipFormatter,
  tooltipLabelFormatter,
  barFill,
  hideLegend = false,
}: BarChartProps<T>) {
  const outerRef = useRef<HTMLDivElement>(null);
  const chartWidth = useContainerWidth(outerRef);

  // Extraer valores numéricos
  const numericDataKey = bars[0]?.dataKey ?? "";

  const maxVal = yAxisDomain?.[1] ?? 100;
  const minVal = yAxisDomain?.[0] ?? 0;
  const range = maxVal - minVal;

  // Padding
  const margin = { top: 20, right: 20, bottom: layout === "horizontal" ? 80 : 30, left: layout === "vertical" ? 160 : 60 };
  const plotW = Math.max(100, chartWidth - margin.left - margin.right);
  const plotH = Math.max(50, height - margin.top - margin.bottom);

  return (
    <div ref={outerRef} className="rounded-lg border bg-card p-6 shadow-sm w-full" style={{ minWidth: 0 }}>
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="text-lg font-semibold">{title}</h3>}
          {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
        </div>
      )}

      {chartWidth > 0 && data.length > 0 ? (
        <svg width={chartWidth} height={height} viewBox={`0 0 ${chartWidth} ${height}`}>
          {/* Y-axis label */}
          {yAxisLabel && layout === "vertical" && (
            <text
              x={12}
              y={margin.top + plotH / 2}
              textAnchor="middle"
              fill="#94a3b8"
              fontSize={11}
              transform={`rotate(-90, 12, ${margin.top + plotH / 2})`}
            >
              {yAxisLabel}
            </text>
          )}

          {layout === "vertical" ? (
            <>
              {/* Y-axis (category labels) */}
              {data.map((d, i) => {
                const val = (d as Record<string, unknown>)[xAxisDataKey] as string;
                if (!val) return null;
                const y = margin.top + (i + 0.5) * (plotH / data.length);
                return (
                  <text
                    key={i}
                    x={margin.left - 8}
                    y={y}
                    textAnchor="end"
                    dominantBaseline="middle"
                    fill="#64748b"
                    fontSize={12}
                  >
                    {val}
                  </text>
                );
              })}

              {/* Grid + X-axis (number) */}
              {[0, 0.25, 0.5, 0.75, 1].map((frac) => {
                const x = margin.left + frac * plotW;
                const label = Math.round(minVal + frac * range);
                return (
                  <g key={frac}>
                    <line x1={x} y1={margin.top} x2={x} y2={margin.top + plotH} stroke="#e2e8f0" strokeDasharray="3 3" />
                    <text x={x} y={margin.top + plotH + 16} textAnchor="middle" fill="#94a3b8" fontSize={11}>{label}</text>
                  </g>
                );
              })}

              {/* Horizontal zero line */}
              <line x1={margin.left} y1={margin.top + plotH} x2={margin.left + plotW} y2={margin.top + plotH} stroke="#cbd5e1" />

              {/* Bars */}
              {data.map((d, i) => {
                const val = (d as Record<string, unknown>)[numericDataKey] as number ?? 0;
                const frac = Math.max(0, (val - minVal) / range);
                const barH = Math.max(6, plotH / data.length * 0.6);
                const y = margin.top + (i + 0.5) * (plotH / data.length) - barH / 2;
                const barW = frac * plotW;
                const fill = barFill ? barFill(d, i) : bar.color || "#2563EB";
                return (
                  <g key={i}>
                    <rect
                      x={margin.left}
                      y={y}
                      width={Math.max(2, barW)}
                      height={barH}
                      fill={fill}
                      rx={4}
                    />
                    <text
                      x={margin.left + barW + 6}
                      y={y + barH / 2}
                      dominantBaseline="middle"
                      fill="#64748b"
                      fontSize={11}
                    >
                      {tooltipFormatter ? tooltipFormatter(val, bars[0]?.name) : val}
                    </text>
                  </g>
                );
              })}
            </>
          ) : (
            /* layout horizontal: categorías en X, valores en Y */
            <>
              {/* Y-axis */}
              {[0, 0.25, 0.5, 0.75, 1].map((frac) => {
                const y = margin.top + (1 - frac) * plotH;
                const label = Math.round(minVal + frac * range);
                return (
                  <g key={frac}>
                    <line x1={margin.left} y1={y} x2={margin.left + plotW} y2={y} stroke="#e2e8f0" strokeDasharray="3 3" />
                    <text x={margin.left - 8} y={y} textAnchor="end" dominantBaseline="middle" fill="#94a3b8" fontSize={11}>{label}</text>
                  </g>
                );
              })}

              {/* Y-axis label */}
              {yAxisLabel && (
                <text
                  x={12}
                  y={margin.top + plotH / 2}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize={11}
                  transform={`rotate(-90, 12, ${margin.top + plotH / 2})`}
                >
                  {yAxisLabel}
                </text>
              )}

              {/* X-axis (categories) */}
              {data.map((d, i) => {
                const name = (d as Record<string, unknown>)[xAxisDataKey] as string;
                if (!name) return null;
                const x = margin.left + (i + 0.5) * (plotW / data.length);
                return (
                  <text
                    key={i}
                    x={x}
                    y={margin.top + plotH + 16}
                    textAnchor="end"
                    fill="#64748b"
                    fontSize={11}
                    transform={`rotate(-30, ${x}, ${margin.top + plotH + 16})`}
                  >
                    {name}
                  </text>
                );
              })}

              {/* Bars */}
              {data.map((d, i) => {
                const val = (d as Record<string, unknown>)[numericDataKey] as number ?? 0;
                const frac = Math.max(0, (val - minVal) / range);
                const barW = Math.max(6, plotW / data.length * 0.6);
                const x = margin.left + (i + 0.5) * (plotW / data.length) - barW / 2;
                const barH = frac * plotH;
                const fill = barFill ? barFill(d, i) : bar.color || "#2563EB";
                return (
                  <rect
                    key={i}
                    x={x}
                    y={margin.top + plotH - barH}
                    width={barW}
                    height={Math.max(2, barH)}
                    fill={fill}
                    rx={4}
                  />
                );
              })}
            </>
          )}
        </svg>
      ) : (
        <div style={{ height: `${height}px` }} className="flex items-center justify-center text-muted-foreground text-sm">
          {data.length === 0 ? "Sin datos para mostrar" : "Preparando gráfico..."}
        </div>
      )}
    </div>
  );
}
