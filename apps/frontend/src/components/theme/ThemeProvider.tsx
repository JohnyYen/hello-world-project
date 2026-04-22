'use client';

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import type { ThemeProviderProps } from "next-themes";
import { useEffect, useState } from "react";
import { COLOR_MAP, DEFAULT_COLOR_THEME, type ColorThemeName } from "./theme-constants";

interface ExtendedThemeProviderProps extends ThemeProviderProps {
  storageKey?: string;
  initialTheme?: "light" | "dark";
  initialColorTheme?: ColorThemeName;
  initialAnimationsEnabled?: boolean;
}

function getStoredTheme(storageKey?: string): "light" | "dark" | undefined {
  if (typeof window === "undefined") return undefined;
  
  const key = storageKey || "theme";
  try {
    const stored = localStorage.getItem(key);
    if (stored === "light" || stored === "dark") {
      return stored;
    }
  } catch {
    // localStorage not available
  }
  return undefined;
}

export function ThemeProvider({ 
  children, 
  storageKey, 
  initialTheme, 
  initialColorTheme,
  initialAnimationsEnabled,
  ...props 
}: ExtendedThemeProviderProps) {
  const [mounted, setMounted] = useState(false);
  const [settings, setSettings] = useState<{
    theme: "light" | "dark" | undefined;
    colorTheme: ColorThemeName | undefined;
    animationsEnabled: boolean;
  }>({ 
    theme: initialTheme || getStoredTheme(storageKey), 
    colorTheme: initialColorTheme || DEFAULT_COLOR_THEME,
    animationsEnabled: initialAnimationsEnabled ?? true,
  });

  useEffect(() => {
    setMounted(true);

    if (initialColorTheme && COLOR_MAP[initialColorTheme]) {
      applyColorTheme(initialColorTheme);
    }

    if (initialAnimationsEnabled !== undefined) {
      applyAnimations(initialAnimationsEnabled);
    }
  }, [initialColorTheme, initialAnimationsEnabled]);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const token = getAuthToken();
        if (!token) return;

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/professors/settings`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          if (data.data) {
            const theme = data.data.theme;
            const colorTheme = data.data.color_theme as ColorThemeName | undefined;
            const animationsEnabled = data.data.animations_enabled ?? true;
            
            setSettings(prev => ({
              theme: theme || prev.theme,
              colorTheme: colorTheme || DEFAULT_COLOR_THEME,
              animationsEnabled,
            }));

            if (colorTheme && COLOR_MAP[colorTheme]) {
              applyColorTheme(colorTheme);
            }

            applyAnimations(animationsEnabled);
          }
        }
      } catch (error) {
        console.error("Failed to load theme settings:", error);
      }
    };

    loadSettings();
  }, []);

  const applyColorTheme = (themeName: ColorThemeName) => {
    const colors = COLOR_MAP[themeName] || COLOR_MAP[DEFAULT_COLOR_THEME];
    const root = document.documentElement;
    
    Object.entries(colors).forEach(([cssVar, value]) => {
      root.style.setProperty(cssVar, value);
    });
  };

  const applyAnimations = (enabled: boolean) => {
    const root = document.documentElement;
    if (enabled) {
      root.style.removeProperty("--animation-duration");
      root.style.removeProperty("--animation-speed");
    } else {
      root.style.setProperty("--animation-duration", "0s");
      root.style.setProperty("--animation-speed", "0s");
    }
  };

  const forcedTheme = mounted && settings.theme ? settings.theme : undefined;

  return (
    <NextThemesProvider
      {...props}
      forcedTheme={forcedTheme}
      storageKey={storageKey}
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange={false}
    >
      {children}
    </NextThemesProvider>
  );
}

function getAuthToken(): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(/(?:^|; )auth_token=([^;]+)/);
  return match ? match[1] : null;
}