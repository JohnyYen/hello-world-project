import { describe, it, expect } from "vitest"
import { completionRateFilterFn } from "../data-table"

// Mock Row object for testing filterFn
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
    it("returns true for rates above 80", () => {
      const row = createMockRow(85)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(true)
    })

    it("returns false for rate exactly 80 (boundary)", () => {
      const row = createMockRow(80)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(false)
    })

    it("returns false for rates below 80", () => {
      const row = createMockRow(45)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(false)
    })
  })

  describe("medium completion (50-80%)", () => {
    it("returns true for rate 65 (within range)", () => {
      const row = createMockRow(65)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(true)
    })

    it("returns true for rate exactly 80 (upper boundary)", () => {
      const row = createMockRow(80)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(true)
    })

    it("returns true for rate exactly 50 (lower boundary)", () => {
      const row = createMockRow(50)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(true)
    })

    it("returns false for rate 49 (below lower boundary)", () => {
      const row = createMockRow(49)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(false)
    })

    it("returns false for rate 81 (above upper boundary)", () => {
      const row = createMockRow(81)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(false)
    })
  })

  describe("low completion (< 50%)", () => {
    it("returns true for rate 30", () => {
      const row = createMockRow(30)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(true)
    })

    it("returns true for rate 49", () => {
      const row = createMockRow(49)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(true)
    })

    it("returns false for rate exactly 50 (boundary)", () => {
      const row = createMockRow(50)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(false)
    })

    it("returns false for rate 80", () => {
      const row = createMockRow(80)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(false)
    })
  })

  describe("unknown filter value", () => {
    it("returns true for unknown filter string (passthrough)", () => {
      const row = createMockRow(50)
      expect(completionRateFilterFn(row, "completionRate", "unknown")).toBe(true)
    })

    it("returns true for empty string", () => {
      const row = createMockRow(50)
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
      const row = createMockRow(100)
      expect(completionRateFilterFn(row, "completionRate", "high")).toBe(true)
      expect(completionRateFilterFn(row, "completionRate", "medium")).toBe(false)
      expect(completionRateFilterFn(row, "completionRate", "low")).toBe(false)
    })
  })
})
