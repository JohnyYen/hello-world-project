import * as React from "react"
import { IconTrendingDown, IconTrendingUp, IconUsers, IconCurrencyDollar, IconActivity, IconChartBar } from "@tabler/icons-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardAction,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface CardData {
  title: string
  value: string
  change: number
  trend: "up" | "down"
  description: string
  icon: React.ReactNode
  gradient: string
}

const cardsData: CardData[] = [
  {
    title: "Ingresos Totales",
    value: "$1,250.00",
    change: 12.5,
    trend: "up",
    description: "Tendencia al alza este mes",
    icon: <IconCurrencyDollar className="w-4 h-4" />,
    gradient: "from-emerald-500 to-teal-600",
  },
  {
    title: "Nuevos Clientes",
    value: "1,234",
    change: -20,
    trend: "down",
    description: "La adquisición necesita atención",
    icon: <IconUsers className="w-4 h-4" />,
    gradient: "from-rose-500 to-orange-500",
  },
  {
    title: "Cuentas Activas",
    value: "45,678",
    change: 12.5,
    trend: "up",
    description: "Fuerte retención de usuarios",
    icon: <IconActivity className="w-4 h-4" />,
    gradient: "from-indigo-500 to-violet-600",
  },
  {
    title: "Tasa de Crecimiento",
    value: "4.5%",
    change: 4.5,
    trend: "up",
    description: "Aumento constante del rendimiento",
    icon: <IconChartBar className="w-4 h-4" />,
    gradient: "from-amber-500 to-yellow-500",
  },
]

export function SectionCards() {
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
              Visitantes en los últimos 6 meses
            </div>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}
