import { describe, it, expect } from "vitest"
import { completionRateFilterFn } from "../data-table"

// Mock Row object for testing filterFn
// Backend sends completionRate on 0-1 scale, tests use 0-1 values
function createMockRow(completionRate: number) {
  return {
    getValue: (columnId: string) => {
      if (columnId === "completionRate") return completionRate
      return undefined
    },
    original: { completionRate },
  } as any
}

describe("completionRateFilterFn", () => {
  describe("high completion (> 80%)", () => {
    it("returns true for rates above 0.8", () => {
      const row = createMockRow(0.85)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(true)
    })

    it("returns false for rate exactly 0.8 (boundary)", () => {
      const row = createMockRow(0.8)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(false)
    })

    it("returns false for rates below 0.8", () => {
      const row = createMockRow(0.45)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(false)
    })
  })

  describe("medium completion (50-80%)", () => {
    it("returns true for rate 0.65 (within range)", () => {
      const row = createMockRow(0.65)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(true)
    })

    it("returns true for rate exactly 0.8 (upper boundary)", () => {
      const row = createMockRow(0.8)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(true)
    })

    it("returns true for rate exactly 0.5 (lower boundary)", () => {
      const row = createMockRow(0.5)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(true)
    })

    it("returns false for rate 0.49 (below lower boundary)", () => {
      const row = createMockRow(0.49)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(false)
    })

    it("returns false for rate 0.81 (above upper boundary)", () => {
      const row = createMockRow(0.81)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(false)
    })
  })

  describe("low completion (< 50%)", () => {
    it("returns true for rate 0.3", () => {
      const row = createMockRow(0.3)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(true)
    })

    it("returns true for rate 0.49", () => {
      const row = createMockRow(0.49)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(true)
    })

    it("returns false for rate exactly 0.5 (boundary)", () => {
      const row = createMockRow(0.5)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(false)
    })

    it("returns false for rate 0.8", () => {
      const row = createMockRow(0.8)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(false)
    })
  })

  describe("unknown filter value", () => {
    it("returns true for unknown filter string (passthrough)", () => {
      const row = createMockRow(0.5)
      expect(completionRateFilterFn(row, "completionRate", "unknown")).toBe(true)
    })

    it("returns true for empty string", () => {
      const row = createMockRow(0.5)
      expect(completionRateFilterFn(row, "completionRate", "")).toBe(true)
    })
  })

  describe("edge cases", () => {
    it("handles 0% completion rate", () => {
      const row = createMockRow(0)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(true)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(false)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(false)
    })

    it("handles 100% completion rate", () => {
      const row = createMockRow(1.0)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(true)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(false)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(false)
    })
  })
})
