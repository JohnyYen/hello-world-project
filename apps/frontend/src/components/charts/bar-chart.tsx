"use client";

import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell,
} from "recharts";
import { COLORS, CHART_COLORS_ARRAY, useChartThemeColors } from "@/lib/colors";
import { cn } from "@/lib/utils";

interface BarChartProps<T> {
  data: T[];
  bars: {
    dataKey: string;
    name: string;
    color?: string;
    stackId?: string;
  }[];
  xAxisDataKey: string;
  title?: string;
  subtitle?: string;
  yAxisLabel?: string;
  xAxisLabel?: string;
  height?: number;
  layout?: "horizontal" | "vertical";
  stacked?: boolean;
  showAnimation?: boolean;
  showGrid?: boolean;
  yAxisDomain?: [number, number];
  tooltipFormatter?: (value: number, name: string) => string;
  tooltipLabelFormatter?: (label: string, item: T) => string;
  /** Optional function to compute fill color per data point. Receives the datum and its index, returns a color string. */
  barFill?: (entry: T, index: number) => string;
  /** When true, the Legend component is not rendered */
  hideLegend?: boolean;
}

export function BarChart<T>({
  data,
  bars,
  xAxisDataKey,
  title,
  subtitle,
  yAxisLabel,
  xAxisLabel,
  height = 300,
  layout = "horizontal",
  stacked = false,
  showAnimation = true,
  showGrid = true,
  yAxisDomain,
  tooltipFormatter,
  tooltipLabelFormatter,
  barFill,
  hideLegend = false,
}: BarChartProps<T>) {
  const themeColors = useChartThemeColors();

  const CustomTooltip = ({
    active,
    payload,
    label,
  }: {
    active?: boolean;
    payload?: Array<{
      name: string;
      value: number;
      color: string;
      payload?: T;
    }>;
    label?: string;
  }) => {
    if (!active || !payload || !payload.length) return null;

    // Find the item in data that matches the label
    const item = data.find((d) => {
      const itemAsRecord = d as Record<string, unknown>;
      return String(itemAsRecord[xAxisDataKey]) === String(label);
    }) as T | undefined;

    const displayLabel =
      item && tooltipLabelFormatter
        ? tooltipLabelFormatter(label || "", item)
        : label;

    return (
      <div className="rounded-lg border bg-card p-3 shadow-lg">
        {displayLabel && (
          <p className="text-sm font-medium text-foreground mb-2">
            {displayLabel}
          </p>
        )}
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
        >
          {showGrid && (
            <CartesianGrid strokeDasharray="3 3" stroke={themeColors.border} />
          )}
          {layout === "horizontal" ? (
            <>
              <XAxis
                dataKey={xAxisDataKey}
                tick={{ fill: themeColors.text, fontSize: 12 }}
                axisLine={{ stroke: themeColors.border }}
                tickLine={{ stroke: themeColors.border }}
                interval={0}
                angle={-15}
                textAnchor="end"
                height={60}
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
                domain={yAxisDomain}
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
                domain={yAxisDomain}
                label={
                  xAxisLabel
                    ? {
                        value: xAxisLabel,
                        angle: 90,
                        position: "insideBottom",
                        offset: 5,
                        fill: themeColors.text,
                        fontSize: 12,
                      }
                    : undefined
                }
              />
              <YAxis
                type="category"
                dataKey={xAxisDataKey}
                tick={{ fill: themeColors.text, fontSize: 12 }}
                axisLine={{ stroke: themeColors.border }}
                tickLine={{ stroke: themeColors.border }}
                width={120}
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
          {bars.map((bar, index) => (
            <Bar
              key={bar.dataKey}
              dataKey={bar.dataKey}
              name={bar.name}
              fill={
                barFill
                  ? undefined
                  : bar.color ||
                    CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length]
              }
              stackId={stacked ? bar.stackId || "stack" : undefined}
              radius={stacked ? [0, 0, 0, 0] : [4, 4, 0, 0]}
              animationDuration={1000}
              animationEasing="ease-out"
            >
              {barFill &&
                data.map((entry, cellIndex) => (
                  <Cell
                    key={`cell-${cellIndex}`}
                    fill={barFill(entry, cellIndex)}
                  />
                ))}
            </Bar>
          ))}
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
}