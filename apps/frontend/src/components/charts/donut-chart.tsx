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
  subtitle?: string;
  height?: number;
  innerRadius?: number;
  outerRadius?: number;
  showPercentage?: boolean;
  showAnimation?: boolean;
  tooltipFormatter?: (value: number, name: string) => string;
}

export function DonutChart({
  data,
  title,
  subtitle,
  height = 300,
  innerRadius = 60,
  outerRadius = 100,
  showPercentage = true,
  showAnimation = true,
  tooltipFormatter,
}: DonutChartProps) {
  const COLORS_ARRAY = CHART_COLORS_ARRAY;

  const total = data.reduce((sum, item) => sum + item.value, 0);

  const renderCustomLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
  }: {
    cx: number;
    cy: number;
    midAngle: number;
    innerRadius: number;
    outerRadius: number;
    percent: number;
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

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ name: string; value: number; payload: DataPoint }> }) => {
    if (!active || !payload || !payload.length) return null;
    
    const entry = payload[0];
    const percentage = total > 0 ? ((entry.value / total) * 100).toFixed(1) : 0;
    
    return (
      <div className="rounded-lg border bg-card p-3 shadow-lg">
        <div className="flex items-center gap-2 text-sm">
          <div 
            className="w-3 h-3 rounded-full" 
            style={{ backgroundColor: COLORS_ARRAY[data.findIndex(d => d.name === entry.name) % COLORS_ARRAY.length] }}
          />
          <span className="font-medium">{entry.name}</span>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          {tooltipFormatter ? tooltipFormatter(entry.value, entry.name) : `${entry.value} (${percentage}%)`}
        </p>
      </div>
    );
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const renderLegend = (props: any) => {
    const { payload } = props;
    if (!payload) return null;

    return (
      <div className="flex flex-wrap justify-center gap-4 mt-4">
        {payload.map((entry: { value: string; color: string | undefined }, index: number) => {
          const item = data[index];
          const percentage = total > 0 ? ((item.value / total) * 100).toFixed(1) : 0;
          
          return (
            <div key={index} className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: entry.color || COLORS_ARRAY[index % COLORS_ARRAY.length] }}
              />
              <span className="text-sm text-foreground">{entry.value}</span>
              <span className="text-xs text-muted-foreground">({percentage}%)</span>
            </div>
          );
        })}
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
            animationDuration={1000}
            animationEasing="ease-out"
          >
            {data.map((_entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS_ARRAY[index % COLORS_ARRAY.length]}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend content={renderLegend} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
