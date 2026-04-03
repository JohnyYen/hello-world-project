"use client"

import * as React from "react"
import { ChartAreaInteractive, SectionCards, DataTable } from "@/components/dashboard"
import { useDashboardStats } from "@/hooks/use-dashboard-stats"

import data from "./data.json"

export default function Page() {
  const [period, setPeriod] = React.useState<"7d" | "30d" | "3m">("30d")
  
  const { 
    kpis, 
    activityOverTime, 
    trends, 
    isLoading, 
    error, 
    refetch 
  } = useDashboardStats(period)

  const handlePeriodChange = (newPeriod: "7d" | "30d" | "3m") => {
    setPeriod(newPeriod)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Background pattern */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="container mx-auto py-12 px-6 relative z-10 space-y-8">
        {/* Page Header - Premium Design */}
        <div className="relative">
          <div className="absolute -left-4 top-0 bottom-0 w-1 bg-gradient-to-b from-indigo-500 via-violet-500 to-indigo-500 rounded-full opacity-60" />
          <div className="pl-6 space-y-2">
            <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-indigo-600 via-violet-600 to-indigo-600 dark:from-indigo-400 dark:via-violet-400 dark:to-indigo-400 bg-clip-text text-transparent">
              Dashboard
            </h1>
            <p className="text-muted-foreground text-lg max-w-xl">
              Resumen general del rendimiento y métricas clave de tu proyecto
            </p>
          </div>
          {/* Decorative elements */}
          <div className="absolute -right-20 -top-10 w-40 h-40 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -right-10 top-20 w-24 h-24 bg-violet-500/10 rounded-full blur-2xl pointer-events-none" />
        </div>

        {/* Error State */}
        {error && (
          <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4">
            <div className="flex items-center justify-between">
              <div className="text-sm text-red-600 dark:text-red-400">
                {error}
              </div>
              <button
                onClick={() => refetch()}
                className="text-sm font-medium text-red-600 dark:text-red-400 hover:underline"
              >
                Reintentar
              </button>
            </div>
          </div>
        )}

        <SectionCards 
          kpis={kpis || null} 
          trends={trends || null}
          isLoading={isLoading}
        />
        
        {/* Chart Section */}
        <div className="group relative rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white/60 dark:bg-slate-900/60 backdrop-blur-xl shadow-xl shadow-indigo-500/5 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-transparent to-violet-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          <ChartAreaInteractive 
            data={activityOverTime}
            period={period}
            onPeriodChange={handlePeriodChange}
            isLoading={isLoading}
          />
        </div>
        
        {/* Data Table Section */}
        <div className="group relative rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white/60 dark:bg-slate-900/60 backdrop-blur-xl shadow-xl shadow-indigo-500/5 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-transparent to-violet-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          <DataTable data={data} />
        </div>
      </div>
    </div>
  )
}
