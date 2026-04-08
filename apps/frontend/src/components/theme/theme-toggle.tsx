'use client'
import { useEffect } from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "@/components/theme/useTheme";
import { Button } from "@/components/ui/button";

interface ThemeToggleProps {
  initialTheme?: string;
}

export function ThemeToggle({ initialTheme }: ThemeToggleProps) {
  const { theme, setTheme } = useTheme();

  // Initialize theme from backend if provided
  useEffect(() => {
    if (initialTheme && (initialTheme === "light" || initialTheme === "dark")) {
      // Only set if different from current (to avoid unnecessary backend calls)
      if (theme !== initialTheme) {
        setTheme(initialTheme);
      }
    }
  }, [initialTheme]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
