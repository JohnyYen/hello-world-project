"use client";

import {
  AreaChart as RechartsAreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { COLORS, CHART_COLORS_ARRAY } from "@/lib/colors";

interface AreaChartProps<T> {
  data: T[];
  areas: {
    dataKey: string;
    name: string;
    color?: string;
    stackId?: string;
    yAxisId?: string;
  }[];
  xAxisDataKey: string;
  title?: string;
  subtitle?: string;
  yAxisLabel?: string;
  yAxisLabels?: {
    left?: string;
    right?: string;
  };
  xAxisLabel?: string;
  height?: number;
  stacked?: boolean;
  showAnimation?: boolean;
  showGrid?: boolean;
  yAxisDomain?: [number, number];
  yAxisDomains?: {
    left?: [number, number];
    right?: [number, number];
  };
  tooltipFormatter?: (value: number, name: string) => string;
}

export function AreaChart<T>({
  data,
  areas,
  xAxisDataKey,
  title,
  subtitle,
  yAxisLabel,
  yAxisLabels,
  xAxisLabel,
  height = 300,
  stacked = false,
  showAnimation = true,
  showGrid = true,
  yAxisDomain,
  yAxisDomains,
  tooltipFormatter,
}: AreaChartProps<T>) {
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
        <RechartsAreaChart data={data} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />}
          <XAxis
            dataKey={xAxisDataKey}
            tick={{ fill: COLORS.muted, fontSize: 12 }}
            axisLine={{ stroke: COLORS.border }}
            tickLine={{ stroke: COLORS.border }}
            label={
              xAxisLabel
                ? {
                    value: xAxisLabel,
                    position: "insideBottom",
                    offset: -5,
                    fill: COLORS.muted,
                    fontSize: 12,
                  }
                : undefined
            }
          />
          <YAxis
            yAxisId="left"
            tick={{ fill: COLORS.muted, fontSize: 12 }}
            axisLine={{ stroke: COLORS.border }}
            tickLine={{ stroke: COLORS.border }}
            domain={yAxisDomains?.left || yAxisDomain || [0, "dataMax"]}
            label={
              yAxisLabels?.left || yAxisLabel
                ? {
                    value: yAxisLabels?.left || yAxisLabel || "",
                    angle: -90,
                    position: "insideLeft",
                    fill: COLORS.muted,
                    fontSize: 12,
                  }
                : undefined
            }
          />
          {yAxisLabels?.right && (
            <YAxis
              yAxisId="right"
              orientation="right"
              tick={{ fill: COLORS.muted, fontSize: 12 }}
              axisLine={{ stroke: COLORS.border }}
              tickLine={{ stroke: COLORS.border }}
              domain={yAxisDomains?.right || yAxisDomain || [0, "dataMax"]}
              label={{
                value: yAxisLabels.right,
                angle: 90,
                position: "insideRight",
                fill: COLORS.muted,
                fontSize: 12,
              }}
            />
          )}
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ paddingTop: "10px" }}
            formatter={(value) => <span style={{ color: COLORS.foreground, fontSize: 12 }}>{value}</span>}
          />
          {areas.map((area, index) => (
            <Area
              key={area.dataKey}
              type="monotone"
              dataKey={area.dataKey}
              name={area.name}
              yAxisId={area.yAxisId || "left"}
              stackId={stacked ? area.stackId || "stack" : undefined}
              stroke={area.color || CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length]}
              fill={area.color || CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length]}
              fillOpacity={0.3}
              strokeWidth={2}
              animationDuration={1000}
              animationEasing="ease-out"
            />
          ))}
        </RechartsAreaChart>
      </ResponsiveContainer>
    </div>
  );
}
