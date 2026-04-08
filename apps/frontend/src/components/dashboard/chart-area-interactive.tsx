"use client"

import * as React from "react"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"

import { useIsMobile } from "@/hooks/use-mobile"
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

export const description = "An interactive area chart"

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
  { date: "2024-04-01", sessions: 222, students: 150 },
  { date: "2024-04-02", sessions: 97, students: 180 },
  { date: "2024-04-03", sessions: 167, students: 120 },
  { date: "2024-04-04", sessions: 242, students: 260 },
  { date: "2024-04-05", sessions: 373, students: 290 },
  { date: "2024-04-06", sessions: 301, students: 340 },
  { date: "2024-04-07", sessions: 245, students: 180 },
  { date: "2024-04-08", sessions: 409, students: 320 },
  { date: "2024-04-09", sessions: 59, students: 110 },
  { date: "2024-04-10", sessions: 261, students: 190 },
  { date: "2024-04-11", sessions: 327, students: 350 },
  { date: "2024-04-12", sessions: 292, students: 210 },
  { date: "2024-04-13", sessions: 342, students: 380 },
  { date: "2024-04-14", sessions: 137, students: 220 },
  { date: "2024-04-15", sessions: 120, students: 170 },
  { date: "2024-04-16", sessions: 138, students: 190 },
  { date: "2024-04-17", sessions: 446, students: 360 },
  { date: "2024-04-18", sessions: 364, students: 410 },
  { date: "2024-04-19", sessions: 243, students: 180 },
  { date: "2024-04-20", sessions: 89, students: 150 },
  { date: "2024-04-21", sessions: 137, students: 200 },
  { date: "2024-04-22", sessions: 224, students: 170 },
  { date: "2024-04-23", sessions: 138, students: 230 },
  { date: "2024-04-24", sessions: 387, students: 290 },
  { date: "2024-04-25", sessions: 215, students: 250 },
  { date: "2024-04-26", sessions: 75, students: 130 },
  { date: "2024-04-27", sessions: 383, students: 420 },
  { date: "2024-04-28", sessions: 122, students: 180 },
  { date: "2024-04-29", sessions: 315, students: 240 },
  { date: "2024-04-30", sessions: 454, students: 380 },
]

const chartConfig = {
  sessions: {
    label: "Sesiones",
  },
  students: {
    label: "Estudiantes",
    color: "var(--primary)",
  },
  playTime: {
    label: "Tiempo de juego",
    color: "var(--primary)",
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
  
  const filteredData = React.useMemo(() => {
    const daysToSubtract = periodDays[period]
    const referenceDate = new Date()
    const startDate = new Date(referenceDate)
    startDate.setDate(startDate.getDate() - daysToSubtract)
    
    return sourceData.filter((item) => {
      const itemDate = new Date(item.date)
      return itemDate >= startDate
    })
  }, [sourceData, period])

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
            Sesiones y estudiantes activos
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
            <Area
              dataKey="sessions"
              type="natural"
              fill="url(#fillSessions)"
              stroke="var(--color-primary)"
              stackId="a"
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
