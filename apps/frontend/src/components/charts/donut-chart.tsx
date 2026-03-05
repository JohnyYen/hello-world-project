"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { COLORS, CHART_COLORS_ARRAY } from "@/lib/colors";

interface DataPoint {
  name: string;
  value: number;
}

interface DonutChartProps {
  data: DataPoint[];
  title?: string;
  height?: number;
  innerRadius?: number;
  outerRadius?: number;
  showPercentage?: boolean;
}

export function DonutChart({
  data,
  title,
  height = 300,
  innerRadius = 60,
  outerRadius = 100,
  showPercentage = true,
}: DonutChartProps) {
  const COLORS_ARRAY = CHART_COLORS_ARRAY;

  const renderCustomLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
    name,
  }: {
    cx: number;
    cy: number;
    midAngle: number;
    innerRadius: number;
    outerRadius: number;
    percent: number;
    name: string;
  }) => {
    if (!showPercentage || percent < 0.05) return null;
    
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor="middle"
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="rounded-lg border bg-card p-6 shadow-sm">
      {title && (
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomLabel}
            innerRadius={innerRadius}
            outerRadius={outerRadius}
            fill="#8884d8"
            dataKey="value"
            stroke={COLORS.card}
            strokeWidth={2}
          >
            {data.map((_entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS_ARRAY[index % COLORS_ARRAY.length]}
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: "8px",
            }}
            formatter={(value: number) => [`${value}`, "Valor"]}
          />
          <Legend
            formatter={(value) => (
              <span style={{ color: COLORS.foreground, fontSize: 12 }}>
                {value}
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
