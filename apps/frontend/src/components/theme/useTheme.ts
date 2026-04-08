"use client"

import { useCallback, useRef } from "react"
import { useTheme as useNextTheme } from "next-themes"
import { updateTheme } from "@/app/actions/settings"

export const useTheme = () => {
  const { theme, setTheme: setNextTheme, resolvedTheme, systemTheme } = useNextTheme()
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const syncTimeoutRef = useRef(500) // 500ms debounce

  const setTheme = useCallback((newTheme: string) => {
    // Update locally immediately (via next-themes)
    setNextTheme(newTheme)

    // Debounced backend sync
    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }

    debounceRef.current = setTimeout(async () => {
      if (newTheme === "light" || newTheme === "dark") {
        await updateTheme(newTheme as "light" | "dark")
      }
    }, syncTimeoutRef.current)
  }, [setNextTheme])
  
  return {
    theme,
    setTheme,
    resolvedTheme,
    systemTheme,
  }
}
