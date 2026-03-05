"use client";

import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { COLORS, CHART_COLORS_ARRAY } from "@/lib/colors";

interface LineChartProps<T> {
  data: T[];
  lines: {
    dataKey: string;
    name: string;
    color?: string;
    strokeWidth?: number;
  }[];
  xAxisDataKey: string;
  title?: string;
  yAxisLabel?: string;
  height?: number;
}

export function LineChart<T>({
  data,
  lines,
  xAxisDataKey,
  title,
  yAxisLabel,
  height = 300,
}: LineChartProps<T>) {
  return (
    <div className="rounded-lg border bg-card p-6 shadow-sm">
      {title && (
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsLineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
          <XAxis
            dataKey={xAxisDataKey}
            tick={{ fill: COLORS.muted, fontSize: 12 }}
            axisLine={{ stroke: COLORS.border }}
          />
          <YAxis
            tick={{ fill: COLORS.muted, fontSize: 12 }}
            axisLine={{ stroke: COLORS.border }}
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
          <Tooltip
            contentStyle={{
              backgroundColor: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: "8px",
            }}
          />
          <Legend />
          {lines.map((line, index) => (
            <Line
              key={line.dataKey}
              type="monotone"
              dataKey={line.dataKey}
              name={line.name}
              stroke={line.color || CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length]}
              strokeWidth={line.strokeWidth || 2}
              dot={{ fill: line.color || CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length], r: 4 }}
              activeDot={{ r: 6 }}
            />
          ))}
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  );
}
