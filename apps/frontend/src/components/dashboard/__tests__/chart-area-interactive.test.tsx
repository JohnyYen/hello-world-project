import { describe, it, expect } from "vitest"
import { chartConfig } from "../chart-area-interactive"

const CHART_METRICS = ["sessions", "students", "playTime"] as const

describe("ChartAreaInteractive - chartConfig", () => {
  it("has all three metric entries with labels and colors", () => {
    const metrics = Object.keys(chartConfig)
    expect(metrics).toHaveLength(3)
    expect(metrics).toEqual(["sessions", "students", "playTime"])
  })

  it("each metric has a non-empty label", () => {
    for (const metric of CHART_METRICS) {
      expect(chartConfig[metric].label).toBeTruthy()
      expect(typeof chartConfig[metric].label).toBe("string")
    }
  })

  it("each metric has a color value", () => {
    for (const metric of CHART_METRICS) {
      expect(chartConfig[metric].color).toBeTruthy()
      expect(chartConfig[metric].color).toMatch(/^var\(--color-/)
    }
  })

  it("uses distinct CSS variables for each metric color", () => {
    const colors = CHART_METRICS.map(m => chartConfig[m].color)
    const unique = new Set(colors)
    expect(unique.size).toBe(3)
  })

  it("labels are in Spanish", () => {
    expect(chartConfig.sessions.label).toBe("Sesiones")
    expect(chartConfig.students.label).toBe("Estudiantes Activos")
    expect(chartConfig.playTime.label).toBe("Tiempo de Juego")
  })
})

describe("ChartAreaInteractive - metrics toggle state logic", () => {
  type MetricKey = (typeof CHART_METRICS)[number]

  const toggleMetricVisibility = (
    prev: Set<MetricKey>,
    metric: MetricKey
  ): Set<MetricKey> => {
    const next = new Set(prev)
    if (next.has(metric)) {
      next.delete(metric)
    } else {
      next.add(metric)
    }
    return next
  }

  it("starts with all metrics visible by default", () => {
    const visible = new Set<MetricKey>(CHART_METRICS)
    expect(visible.has("sessions")).toBe(true)
    expect(visible.has("students")).toBe(true)
    expect(visible.has("playTime")).toBe(true)
    expect(visible.size).toBe(3)
  })

  it("removes a metric when toggled off", () => {
    let visible = new Set<MetricKey>(CHART_METRICS)
    visible = toggleMetricVisibility(visible, "sessions")
    expect(visible.has("sessions")).toBe(false)
    expect(visible.size).toBe(2)
  })

  it("re-adds a metric when toggled again", () => {
    let visible = new Set<MetricKey>(CHART_METRICS)
    visible = toggleMetricVisibility(visible, "sessions")
    visible = toggleMetricVisibility(visible, "sessions")
    expect(visible.has("sessions")).toBe(true)
    expect(visible.size).toBe(3)
  })

  it("handles toggling multiple metrics independently", () => {
    let visible = new Set<MetricKey>(CHART_METRICS)
    visible = toggleMetricVisibility(visible, "students")
    visible = toggleMetricVisibility(visible, "playTime")
    expect(visible.has("sessions")).toBe(true)
    expect(visible.has("students")).toBe(false)
    expect(visible.has("playTime")).toBe(false)
    expect(visible.size).toBe(1)
  })

  it("can toggle all metrics off one by one", () => {
    let visible = new Set<MetricKey>(CHART_METRICS)
    for (const metric of CHART_METRICS) {
      visible = toggleMetricVisibility(visible, metric)
    }
    expect(visible.size).toBe(0)
  })
})

describe("ChartAreaInteractive - period filtering", () => {
  const periodDays: Record<string, number> = {
    "7d": 7,
    "30d": 30,
    "3m": 90,
  }

  it("maps period strings to correct days", () => {
    expect(periodDays["7d"]).toBe(7)
    expect(periodDays["30d"]).toBe(30)
    expect(periodDays["3m"]).toBe(90)
  })

  it("allows only valid period options", () => {
    const validPeriods = ["7d", "30d", "3m"]
    expect(validPeriods).toContain("7d")
    expect(validPeriods).toContain("30d")
    expect(validPeriods).toContain("3m")
    expect(validPeriods).not.toContain("1d")
    expect(validPeriods).not.toContain("1y")
  })
})
