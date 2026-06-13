"use client"

import * as React from "react"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"
import { toast } from "sonner"

import { useIsMobile } from "@/hooks/use-mobile"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@/components/ui/toggle-group"
import { Skeleton } from "@/components/ui/skeleton"

export const description = "An interactive area chart showing sessions, active students, and play time"

// Available metrics for the chart
const CHART_METRICS = ["sessions", "students", "playTime"] as const
type MetricKey = (typeof CHART_METRICS)[number]

export interface ActivityData {
  date: string
  sessions: number
  activeStudents: number
  playTimeMinutes: number
}

export interface ChartAreaInteractiveProps {
  data?: ActivityData[]
  period?: "7d" | "30d" | "3m"
  onPeriodChange?: (period: "7d" | "30d" | "3m") => void
  isLoading?: boolean
}

// Fallback data when no props provided
const fallbackData = [
  { date: "2024-04-01", sessions: 222, students: 150, playTime: 45 },
  { date: "2024-04-02", sessions: 97, students: 180, playTime: 38 },
  { date: "2024-04-03", sessions: 167, students: 120, playTime: 52 },
  { date: "2024-04-04", sessions: 242, students: 260, playTime: 61 },
  { date: "2024-04-05", sessions: 373, students: 290, playTime: 73 },
  { date: "2024-04-06", sessions: 301, students: 340, playTime: 85 },
  { date: "2024-04-07", sessions: 245, students: 180, playTime: 42 },
  { date: "2024-04-08", sessions: 409, students: 320, playTime: 91 },
  { date: "2024-04-09", sessions: 59, students: 110, playTime: 28 },
  { date: "2024-04-10", sessions: 261, students: 190, playTime: 56 },
  { date: "2024-04-11", sessions: 327, students: 350, playTime: 68 },
  { date: "2024-04-12", sessions: 292, students: 210, playTime: 41 },
  { date: "2024-04-13", sessions: 342, students: 380, playTime: 75 },
  { date: "2024-04-14", sessions: 137, students: 220, playTime: 33 },
  { date: "2024-04-15", sessions: 120, students: 170, playTime: 29 },
  { date: "2024-04-16", sessions: 138, students: 190, playTime: 35 },
  { date: "2024-04-17", sessions: 446, students: 360, playTime: 82 },
  { date: "2024-04-18", sessions: 364, students: 410, playTime: 94 },
  { date: "2024-04-19", sessions: 243, students: 180, playTime: 51 },
  { date: "2024-04-20", sessions: 89, students: 150, playTime: 22 },
]

export const chartConfig = {
  sessions: {
    label: "Sesiones",
    color: "var(--color-primary)",
  },
  students: {
    label: "Estudiantes Activos",
    color: "var(--color-secondary)",
  },
  playTime: {
    label: "Tiempo de Juego",
    color: "var(--color-accent)",
  },
} satisfies ChartConfig

function LoadingSkeleton() {
  return (
    <Card className="@container/card">
      <CardHeader>
        <CardTitle>Actividad</CardTitle>
        <CardDescription>
          <span className="hidden @[540px]/card:block">
            Actividad de estudiantes
          </span>
          <span className="@[540px]/card:hidden">Última actividad</span>
        </CardDescription>
        <CardAction>
          <Skeleton className="h-8 w-32 rounded-md" />
        </CardAction>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <Skeleton className="aspect-auto h-[250px] w-full rounded-lg" />
      </CardContent>
    </Card>
  )
}

function EmptyState() {
  return (
    <Card className="@container/card">
      <CardHeader>
        <CardTitle>Actividad</CardTitle>
        <CardDescription>
          No hay datos de actividad en este período
        </CardDescription>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <div className="flex h-[250px] w-full items-center justify-center text-muted-foreground">
          No hay datos disponibles
        </div>
      </CardContent>
    </Card>
  )
}

export function ChartAreaInteractive({ 
  data, 
  period: initialPeriod, 
  onPeriodChange,
  isLoading 
}: ChartAreaInteractiveProps) {
  const isMobile = useIsMobile()
  const [internalPeriod, setInternalPeriod] = React.useState<"7d" | "30d" | "3m">(
    initialPeriod || "30d"
  )
  
  // Metric visibility state for legend toggle
  const [visibleMetrics, setVisibleMetrics] = React.useState<Set<MetricKey>>(
    new Set(CHART_METRICS)
  )
  
  // Use external period if provided, otherwise use internal
  const period = initialPeriod || internalPeriod

  // Determine if we should use external handler or internal
  const handlePeriodChange = (value: string) => {
    const newPeriod = value as "7d" | "30d" | "3m"
    if (onPeriodChange) {
      onPeriodChange(newPeriod)
    } else {
      setInternalPeriod(newPeriod)
    }
  }

  const toggleMetricVisibility = (metric: MetricKey) => {
    setVisibleMetrics(prev => {
      const next = new Set(prev)
      if (next.has(metric)) {
        next.delete(metric)
      } else {
        next.add(metric)
      }
      return next
    })
  }

  React.useEffect(() => {
    if (isMobile && !initialPeriod) {
      handlePeriodChange("7d")
    }
  }, [isMobile, initialPeriod])

  // Use API data if available, otherwise fallback
  const sourceData = data && data.length > 0 
    ? data.map(item => ({
        date: item.date,
        sessions: item.sessions,
        students: item.activeStudents,
        playTime: item.playTimeMinutes,
      }))
    : fallbackData

  // Filter data based on period
  const periodDays: Record<"7d" | "30d" | "3m", number> = {
    "7d": 7,
    "30d": 30,
    "3m": 90,
  }

  // React Compiler handles memoization automatically - no useMemo needed
  const filteredData = (() => {
    const daysToSubtract = periodDays[period]
    const referenceDate = new Date()
    const startDate = new Date(referenceDate)
    startDate.setDate(startDate.getDate() - daysToSubtract)

    return sourceData.filter((item) => {
      const itemDate = new Date(item.date)
      return itemDate >= startDate
    })
  })()

  // Show loading state
  if (isLoading) {
    return <LoadingSkeleton />
  }

  // Show empty state if no data after filter
  if (!data || data.length === 0) {
    return <EmptyState />
  }

  return (
    <Card className="@container/card">
      <CardHeader>
        <CardTitle>Actividad de Estudiantes</CardTitle>
        <CardDescription>
          <span className="hidden @[540px]/card:block">
            Sesiones, estudiantes activos y tiempo de juego
          </span>
          <span className="@[540px]/card:hidden">Última actividad</span>
        </CardDescription>
        <CardAction>
          <ToggleGroup
            type="single"
            value={period}
            onValueChange={handlePeriodChange}
            variant="outline"
            className="hidden *:data-[slot=toggle-group-item]:!px-4 @[767px]/card:flex"
          >
            <ToggleGroupItem value="3m">3 meses</ToggleGroupItem>
            <ToggleGroupItem value="30d">30 días</ToggleGroupItem>
            <ToggleGroupItem value="7d">7 días</ToggleGroupItem>
          </ToggleGroup>
          <Select value={period} onValueChange={handlePeriodChange}>
            <SelectTrigger
              className="flex w-32 **:data-[slot=select-value]:block **:data-[slot=select-value]:truncate @[767px]/card:hidden"
              size="sm"
              aria-label="Seleccionar período"
            >
              <SelectValue placeholder="Período" />
            </SelectTrigger>
            <SelectContent className="rounded-xl">
              <SelectItem value="3m" className="rounded-lg">
                3 meses
              </SelectItem>
              <SelectItem value="30d" className="rounded-lg">
                30 días
              </SelectItem>
              <SelectItem value="7d" className="rounded-lg">
                7 días
              </SelectItem>
            </SelectContent>
          </Select>
        </CardAction>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[250px] w-full"
        >
          <AreaChart data={filteredData}>
            <defs>
              <linearGradient id="fillSessions" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-primary)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-primary)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillStudents" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-secondary)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-secondary)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillPlayTime" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-accent)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-accent)"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={(value) => {
                const date = new Date(value)
                return date.toLocaleDateString("es-ES", {
                  month: "short",
                  day: "numeric",
                })
              }}
            />
            <YAxis 
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value) => value.toLocaleString()}
            />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  labelFormatter={(value) => {
                    return new Date(value).toLocaleDateString("es-ES", {
                      month: "short",
                      day: "numeric",
                    })
                  }}
                  indicator="dot"
                />
              }
            />
            {visibleMetrics.has("sessions") && (
              <Area
                dataKey="sessions"
                type="natural"
                fill="url(#fillSessions)"
                stroke="var(--color-primary)"
              />
            )}
            {visibleMetrics.has("students") && (
              <Area
                dataKey="students"
                type="natural"
                fill="url(#fillStudents)"
                stroke="var(--color-secondary)"
              />
            )}
            {visibleMetrics.has("playTime") && (
              <Area
                dataKey="playTime"
                type="natural"
                fill="url(#fillPlayTime)"
                stroke="var(--color-accent)"
              />
            )}
          </AreaChart>
        </ChartContainer>
        {/* Custom Legend with Checkboxes */}
        <div className="flex flex-wrap gap-4 pt-4 px-4 justify-center">
          {CHART_METRICS.map(metric => (
            <label 
              key={metric}
              className="flex items-center gap-2 text-xs cursor-pointer hover:text-foreground transition-colors"
            >
              <Checkbox
                checked={visibleMetrics.has(metric)}
                onCheckedChange={() => toggleMetricVisibility(metric)}
                className="data-[state=checked]:bg-primary data-[state=checked]:border-primary"
              />
              <span className="text-muted-foreground">
                {chartConfig[metric].label}
              </span>
            </label>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}