"use client";

import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { CHART_COLORS_ARRAY, useChartThemeColors } from "@/lib/colors";

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
  /** Formatea el label del tooltip (recibe el label y el item de datos completo) */
  tooltipLabelFormatter?: (label: string, item: T) => string;
  /** Función para asignar color por punto de dato. Activa Cells dinámicos en la primera barra. */
  barFill?: (entry: T, index: number) => string;
  hideLegend?: boolean;
  xAxisLabel?: string;
  showAnimation?: boolean;
  showGrid?: boolean;
  stacked?: boolean;
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
  showAnimation = true,
  showGrid = true,
  stacked = false,
  xAxisLabel,
}: BarChartProps<T>) {
  const themeColors = useChartThemeColors();

  const CustomTooltip = ({
    active,
    payload,
    label,
  }: {
    active?: boolean;
    payload?: Array<{ name: string; value: number; color: string; payload: Record<string, unknown> }>;
    label?: string;
  }) => {
    if (!active || !payload || !payload.length) return null;

    const item = payload[0]?.payload;
    // Usar xAxisDataKey para obtener el label real del item, en vez de confiar en Recharts
    const resolvedLabel = item ? String(item[xAxisDataKey] ?? label ?? '') : (label ?? '');
    const displayLabel =
      tooltipLabelFormatter && item
        ? tooltipLabelFormatter(resolvedLabel, item as T)
        : resolvedLabel;

    return (
      <div className="rounded-lg border bg-card p-3 shadow-lg">
        <p className="text-sm font-medium text-foreground mb-2">
          {displayLabel}
        </p>
        <div className="space-y-1">
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center gap-2 text-sm">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: entry.color }}
              />
              <span className="text-muted-foreground">{entry.name}:</span>
              <span className="font-medium">
                {tooltipFormatter
                  ? tooltipFormatter(entry.value, entry.name)
                  : entry.value}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="rounded-lg border bg-card p-6 shadow-sm">
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="text-lg font-semibold">{title}</h3>}
          {subtitle && (
            <p className="text-sm text-muted-foreground">{subtitle}</p>
          )}
        </div>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart
          data={data}
          layout={layout}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          barCategoryGap={layout === "horizontal" ? "20%" : undefined}
        >
          {showGrid && (
            <CartesianGrid
              strokeDasharray="3 3"
              stroke={themeColors.border}
            />
          )}

          {layout === "horizontal" ? (
            <>
              <XAxis
                // Sin dataKey — Recharts usa el índice. Con tickFormatter extraemos del array.
                tickFormatter={(value) => {
                  const item = data[value as number];
                  return item ? String((item as Record<string, unknown>)[xAxisDataKey] ?? '') : String(value);
                }}
                tick={{ fill: themeColors.text, fontSize: 12 }}
                axisLine={{ stroke: themeColors.border }}
                tickLine={{ stroke: themeColors.border }}
                label={
                  xAxisLabel
                    ? {
                        value: xAxisLabel,
                        position: "insideBottom",
                        offset: -5,
                        fill: themeColors.text,
                        fontSize: 12,
                      }
                    : undefined
                }
              />
              <YAxis
                tick={{ fill: themeColors.text, fontSize: 12 }}
                axisLine={{ stroke: themeColors.border }}
                tickLine={{ stroke: themeColors.border }}
                domain={yAxisDomain ?? [0, "auto"]}
                label={
                  yAxisLabel
                    ? {
                        value: yAxisLabel,
                        angle: -90,
                        position: "insideLeft",
                        fill: themeColors.text,
                        fontSize: 12,
                      }
                    : undefined
                }
              />
            </>
          ) : (
            <>
              <XAxis
                type="number"
                tick={{ fill: themeColors.text, fontSize: 12 }}
                axisLine={{ stroke: themeColors.border }}
                tickLine={{ stroke: themeColors.border }}
                domain={yAxisDomain ?? [0, "auto"]}
                label={
                  yAxisLabel
                    ? {
                        value: yAxisLabel,
                        position: "insideBottom",
                        offset: -5,
                        fill: themeColors.text,
                        fontSize: 12,
                      }
                    : undefined
                }
              />
              <YAxis
                type="category"
                tickFormatter={(value) => {
                  const item = data[value as number];
                  return item ? String((item as Record<string, unknown>)[xAxisDataKey] ?? '') : String(value);
                }}
                tick={{ fill: themeColors.text, fontSize: 12 }}
                axisLine={{ stroke: themeColors.border }}
                tickLine={{ stroke: themeColors.border }}
                width={160}
              />
            </>
          )}

          <Tooltip content={<CustomTooltip />} />

          {!hideLegend && (
            <Legend
              wrapperStyle={{ paddingTop: "10px" }}
              formatter={(value) => (
                <span style={{ color: themeColors.foreground, fontSize: 12 }}>
                  {value}
                </span>
              )}
            />
          )}

          {bars.map((bar, index) => {
            // Si barFill está presente, usar Cells dinámicos en la primera barra
            if (barFill && index === 0) {
              return (
                <Bar
                  key={bar.dataKey}
                  dataKey={bar.dataKey}
                  name={bar.name}
                  stackId={stacked ? "stack" : undefined}
                  radius={
                    layout === "horizontal"
                      ? [4, 4, 0, 0]
                      : [0, 4, 4, 0]
                  }
                  isAnimationActive={showAnimation}
                  animationDuration={1000}
                  animationEasing="ease-out"
                >
                  {data.map((entry, i) => (
                    <Cell key={`cell-${i}`} fill={barFill(entry, i)} />
                  ))}
                </Bar>
              );
            }

            return (
              <Bar
                key={bar.dataKey}
                dataKey={bar.dataKey}
                name={bar.name}
                fill={
                  bar.color ||
                  CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length]
                }
                stackId={stacked ? "stack" : undefined}
                radius={
                  layout === "horizontal"
                    ? [4, 4, 0, 0]
                    : [0, 4, 4, 0]
                }
                isAnimationActive={showAnimation}
                animationDuration={1000}
                animationEasing="ease-out"
              />
            );
          })}
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
}
