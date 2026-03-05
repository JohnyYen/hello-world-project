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
  }[];
  xAxisDataKey: string;
  title?: string;
  yAxisLabel?: string;
  height?: number;
  layout?: "horizontal" | "vertical";
}

export function BarChart<T>({
  data,
  bars,
  xAxisDataKey,
  title,
  yAxisLabel,
  height = 300,
  layout = "horizontal",
}: BarChartProps<T>) {
  return (
    <div className="rounded-lg border bg-card p-6 shadow-sm">
      {title && (
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart
          data={data}
          layout={layout}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
          {layout === "horizontal" ? (
            <>
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
            </>
          ) : (
            <>
              <XAxis
                type="number"
                tick={{ fill: COLORS.muted, fontSize: 12 }}
                axisLine={{ stroke: COLORS.border }}
              />
              <YAxis
                type="category"
                dataKey={xAxisDataKey}
                tick={{ fill: COLORS.muted, fontSize: 12 }}
                axisLine={{ stroke: COLORS.border }}
                width={100}
              />
            </>
          )}
          <Tooltip
            contentStyle={{
              backgroundColor: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: "8px",
            }}
          />
          <Legend />
          {bars.map((bar, index) => (
            <Bar
              key={bar.dataKey}
              dataKey={bar.dataKey}
              name={bar.name}
              fill={bar.color || CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length]}
              radius={[4, 4, 0, 0]}
            />
          ))}
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
}
