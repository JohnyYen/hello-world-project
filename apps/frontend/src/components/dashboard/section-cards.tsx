import * as React from "react"
import { IconTrendingDown, IconTrendingUp, IconUsers, IconCurrencyDollar, IconActivity, IconChartBar, IconSchool, IconClock, IconTarget } from "@tabler/icons-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardAction,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export interface KPIsData {
  totalStudents: number
  activeStudentsThisWeek: number
  activeStudentsThisMonth: number
  totalLevelsCompleted: number
  totalPlayTimeMinutes: number
  averageScore: number
}

export interface TrendsData {
  studentsChangePercent: number
  activityChangePercent: number
  scoreChangePercent: number
}

export interface SectionCardsProps {
  kpis?: KPIsData | null
  trends?: TrendsData | null
  isLoading?: boolean
}

interface CardData {
  title: string
  value: string
  change: number
  trend: "up" | "down"
  description: string
  icon: React.ReactNode
  gradient: string
}

// Fallback data for when no props provided (educational platform context)
const fallbackCardsData: CardData[] = [
  {
    title: "Estudiantes Totales",
    value: "0",
    change: 0,
    trend: "up",
    description: "Total de estudiantes registrados",
    icon: <IconSchool className="w-4 h-4" />,
    gradient: "from-emerald-500 to-teal-600",
  },
  {
    title: "Estudiantes Activos",
    value: "0",
    change: 0,
    trend: "up",
    description: "Activos en los últimos 30 días",
    icon: <IconUsers className="w-4 h-4" />,
    gradient: "from-rose-500 to-orange-500",
  },
  {
    title: "Niveles Completados",
    value: "0",
    change: 0,
    trend: "up",
    description: "Total de niveles completados",
    icon: <IconTarget className="w-4 h-4" />,
    gradient: "from-indigo-500 to-violet-600",
  },
  {
    title: "Tiempo de Juego",
    value: "0m",
    change: 0,
    trend: "up",
    description: "Tiempo total de juego",
    icon: <IconClock className="w-4 h-4" />,
    gradient: "from-amber-500 to-yellow-500",
  },
]

// Transform API data to card data format
function transformKPIsToCards(kpis: KPIsData, trends: TrendsData): CardData[] {
  const formatNumber = (num: number): string => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + "M"
    if (num >= 1000) return (num / 1000).toFixed(1) + "K"
    return num.toString()
  }

  const formatTime = (minutes: number): string => {
    if (minutes >= 60) {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      return `${hours}h ${mins}m`
    }
    return `${minutes}m`
  }

  return [
    {
      title: "Estudiantes Totales",
      value: formatNumber(kpis.totalStudents),
      change: trends.studentsChangePercent,
      trend: trends.studentsChangePercent >= 0 ? "up" : "down",
      description: trends.studentsChangePercent >= 0 ? "Crecimiento positivo" : "Necesita atención",
      icon: <IconSchool className="w-4 h-4" />,
      gradient: "from-emerald-500 to-teal-600",
    },
    {
      title: "Estudiantes Activos",
      value: formatNumber(kpis.activeStudentsThisMonth),
      change: trends.activityChangePercent,
      trend: trends.activityChangePercent >= 0 ? "up" : "down",
      description: "En los últimos 30 días",
      icon: <IconUsers className="w-4 h-4" />,
      gradient: "from-rose-500 to-orange-500",
    },
    {
    title: "Niveles Completados",
      value: formatNumber(kpis.totalLevelsCompleted),
      change: trends.activityChangePercent,
      trend: trends.activityChangePercent >= 0 ? "up" : "down",
      description: "Total de niveles",
      icon: <IconTarget className="w-4 h-4" />,
      gradient: "from-indigo-500 to-violet-600",
    },
    {
      title: "Tiempo de Juego",
      value: formatTime(kpis.totalPlayTimeMinutes),
      change: trends.scoreChangePercent,
      trend: trends.scoreChangePercent >= 0 ? "up" : "down",
      description: `Promedio: ${kpis.averageScore.toFixed(0)}%`,
      icon: <IconClock className="w-4 h-4" />,
      gradient: "from-amber-500 to-yellow-500",
    },
  ]
}

function LoadingSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-4 px-4 lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      {[...Array(4)].map((_, i) => (
        <Card 
          key={i}
          className="@container/card group relative overflow-hidden border-slate-200/60 dark:border-slate-800/60 bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm"
        >
          <CardHeader className="relative pb-2">
            <CardDescription className="flex items-center gap-2">
              <Skeleton className="h-5 w-5 rounded-lg" />
              <Skeleton className="h-4 w-24" />
            </CardDescription>
            <CardTitle className="text-2xl">
              <Skeleton className="h-8 w-20" />
            </CardTitle>
            <CardAction>
              <Skeleton className="h-6 w-16 rounded-full" />
            </CardAction>
          </CardHeader>
          <CardFooter className="flex-col items-start gap-1.5 text-sm pt-0">
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-3 w-24" />
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}

export function SectionCards({ kpis, trends, isLoading }: SectionCardsProps) {
  // Use API data if available, otherwise fallback
  const cardsData = kpis && trends 
    ? transformKPIsToCards(kpis, trends)
    : fallbackCardsData

  if (isLoading) {
    return <LoadingSkeleton />
  }

  return (
    <div className="grid grid-cols-1 gap-4 px-4 lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      {cardsData.map((card, index) => (
        <Card 
          key={card.title} 
          className="@container/card group relative overflow-hidden border-slate-200/60 dark:border-slate-800/60 bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/10 hover:-translate-y-1"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {/* Gradient Background */}
          <div className={`absolute inset-0 bg-gradient-to-br ${card.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`} />
          
          {/* Corner Accent */}
          <div className={`absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl ${card.gradient} opacity-10 group-hover:opacity-20 transition-opacity duration-300 rounded-bl-full`} />
          
          <CardHeader className="relative pb-2">
            <CardDescription className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <span className={`p-1.5 rounded-lg bg-gradient-to-br ${card.gradient} bg-opacity-10`}>
                {React.cloneElement(card.icon as React.ReactElement<{ className?: string }>, { 
                  className: `w-3.5 h-3.5 bg-gradient-to-br ${card.gradient} bg-clip-text text-transparent` 
                })}
              </span>
              {card.title}
            </CardDescription>
            <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl text-slate-800 dark:text-slate-200">
              {card.value}
            </CardTitle>
            <CardAction className="relative">
              <Badge 
                variant="outline" 
                className={`${
                  card.trend === "up" 
                    ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20" 
                    : "bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20"
                }`}
              >
                {card.trend === "up" ? <IconTrendingUp /> : <IconTrendingDown />}
                {Math.abs(card.change)}%
              </Badge>
            </CardAction>
          </CardHeader>
          <CardFooter className="relative flex-col items-start gap-1.5 text-sm pt-0">
            <div className="line-clamp-1 flex gap-2 font-medium text-slate-700 dark:text-slate-300">
              {card.description}
              {card.trend === "up" ? (
                <IconTrendingUp className="size-4 text-emerald-500" />
              ) : (
                <IconTrendingDown className="size-4 text-red-500" />
              )}
            </div>
            <div className="text-muted-foreground text-xs">
              {kpis ? "Datos del período seleccionado" : "Datos de ejemplo"}
            </div>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}
