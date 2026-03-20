import { getServerUser } from "@/lib/auth-server";
import { Settings } from "lucide-react";
import { SettingsContent } from "@/components/settings";

export interface TeacherSettingsData {
  theme: string;
  notificationsEnabled: boolean;
  notificationFrequency: string;
  interfaceLanguage: string;
}

async function fetchTeacherSettings(): Promise<TeacherSettingsData> {
  // Intentar obtener settings del servidor
  try {
    const { getTeacherSettings } = await import("@/services/users");
    const settings = await getTeacherSettings();
    return {
      theme: settings.theme ?? "light",
      notificationsEnabled: settings.notificationsEnabled ?? true,
      notificationFrequency: settings.notificationFrequency ?? "daily",
      interfaceLanguage: settings.interfaceLanguage ?? "es",
    };
  } catch {
    // Si falla (usuario sin perfil de profesor), usar valores por defecto
    return {
      theme: "light",
      notificationsEnabled: true,
      notificationFrequency: "daily",
      interfaceLanguage: "es",
    };
  }
}

export default async function SettingsPage() {
  // Verificar que el usuario esté autenticado
  const { user } = await getServerUser();
  
  if (!user) {
    // Si no hay usuario, redirigir al login
    const { redirect } = await import("next/navigation");
    redirect("/login");
  }

  const settings = await fetchTeacherSettings();

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
