"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { Settings, Loader2 } from "lucide-react";
import { SettingsContent } from "@/components/settings";

export interface TeacherSettingsData {
  theme: string;
  notificationsEnabled: boolean;
  notificationFrequency: string;
  interfaceLanguage: string;
  autoLogout: boolean;
  sessionDurationMinutes: number;
  rememberLogin: boolean;
  colorTheme: string;
  animationsEnabled: boolean;
  emailNotifications: boolean;
  dateFormat: string;
  timezone: string;
}

const DEFAULT_SETTINGS: TeacherSettingsData = {
  theme: "light",
  notificationsEnabled: true,
  notificationFrequency: "realtime",
  interfaceLanguage: "es",
  autoLogout: false,
  sessionDurationMinutes: 60,
  rememberLogin: true,
  colorTheme: "Indigo",
  animationsEnabled: true,
  emailNotifications: false,
  dateFormat: "ddmmyyyy",
  timezone: "gmt-5",
};

export default function SettingsPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const [settings, setSettings] = useState<TeacherSettingsData>(DEFAULT_SETTINGS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
      return;
    }

    if (isAuthenticated) {
      // Try to fetch settings from API via Next.js proxy route
      fetch("/api/users/professors/settings")
        .then((res) => {
          if (!res.ok) return;
          return res.json();
        })
        .then((s) => {
          if (s) {
            setSettings({
              theme: s.theme ?? "light",
              notificationsEnabled: s.notifications_enabled ?? true,
              notificationFrequency: s.notification_frequency ?? "realtime",
              interfaceLanguage: s.interface_language ?? "es",
              autoLogout: s.auto_logout ?? false,
              sessionDurationMinutes: s.session_duration_minutes ?? 60,
              rememberLogin: s.remember_login ?? true,
              colorTheme: s.color_theme ?? "Indigo",
              animationsEnabled: s.animations_enabled ?? true,
              emailNotifications: s.email_notifications ?? false,
              dateFormat: s.date_format ?? "ddmmyyyy",
              timezone: s.timezone ?? "gmt-5",
            });
          }
        })
        .catch(() => {
          // Use defaults if API fails
        })
        .finally(() => setLoading(false));
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground">Cargando configuración...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="container mx-auto py-10 px-6 relative z-10">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400">
              <Settings className="h-6 w-6" />
            </div>
            <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
              Configuración
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400 bg-clip-text text-transparent">
            Configuración
          </h1>
          <p className="text-muted-foreground text-lg">
            Personaliza tu experiencia en la plataforma
          </p>
        </div>

        <SettingsContent initialSettings={settings} />
      </div>
    </div>
  );
}
