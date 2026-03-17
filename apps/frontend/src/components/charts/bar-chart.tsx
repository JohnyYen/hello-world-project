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
} from "recharts";
import { COLORS, CHART_COLORS_ARRAY } from "@/lib/colors";

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
  height?: number;
  layout?: "horizontal" | "vertical";
  stacked?: boolean;
  showAnimation?: boolean;
  showGrid?: boolean;
  yAxisDomain?: [number, number];
  tooltipFormatter?: (value: number, name: string) => string;
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
  stacked = false,
  showAnimation = true,
  showGrid = true,
  yAxisDomain,
  tooltipFormatter,
}: BarChartProps<T>) {
  const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: Array<{ name: string; value: number; color: string }>; label?: string }) => {
    if (!active || !payload || !payload.length) return null;
    
    return (
      <div className="rounded-lg border bg-card p-3 shadow-lg">
        <p className="text-sm font-medium text-foreground mb-2">{label}</p>
        <div className="space-y-1">
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center gap-2 text-sm">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: entry.color }}
              />
              <span className="text-muted-foreground">{entry.name}:</span>
              <span className="font-medium">
                {tooltipFormatter ? tooltipFormatter(entry.value, entry.name) : entry.value}
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
          {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
        </div>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart
          data={data}
          layout={layout}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />}
          {layout === "horizontal" ? (
            <>
              <XAxis
                dataKey={xAxisDataKey}
                tick={{ fill: COLORS.muted, fontSize: 12 }}
                axisLine={{ stroke: COLORS.border }}
                tickLine={{ stroke: COLORS.border }}
                interval={0}
                angle={-15}
                textAnchor="end"
                height={60}
              />
              <YAxis
                tick={{ fill: COLORS.muted, fontSize: 12 }}
                axisLine={{ stroke: COLORS.border }}
                tickLine={{ stroke: COLORS.border }}
                domain={yAxisDomain}
                label={
                  yAxisLabel
                    ? {
                        value: yAxisLabel,
                        angle: -90,
                        position: "insideLeft",
                        fill: COLORS.muted,
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
                tick={{ fill: COLORS.muted, fontSize: 12 }}
                axisLine={{ stroke: COLORS.border }}
                tickLine={{ stroke: COLORS.border }}
                domain={yAxisDomain}
              />
              <YAxis
                type="category"
                dataKey={xAxisDataKey}
                tick={{ fill: COLORS.muted, fontSize: 12 }}
                axisLine={{ stroke: COLORS.border }}
                tickLine={{ stroke: COLORS.border }}
                width={100}
              />
            </>
          )}
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ paddingTop: "10px" }}
            formatter={(value) => <span style={{ color: COLORS.foreground, fontSize: 12 }}>{value}</span>}
          />
          {bars.map((bar, index) => (
            <Bar
              key={bar.dataKey}
              dataKey={bar.dataKey}
              name={bar.name}
              fill={bar.color || CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length]}
              stackId={stacked ? bar.stackId || "stack" : undefined}
              radius={stacked ? [0, 0, 0, 0] : [4, 4, 0, 0]}
              animationDuration={1000}
              animationEasing="ease-out"
            />
          ))}
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
}
