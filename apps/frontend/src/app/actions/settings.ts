"use server";

import { z } from "zod";

const TeacherSettingsSchema = z.object({
  theme: z.enum(["light", "dark"]).optional(),
  notificationsEnabled: z.boolean().optional(),
  notificationFrequency: z.enum(["realtime", "daily", "weekly", "disabled"]).optional(),
  interfaceLanguage: z.enum(["es", "en"]).optional(),
  // Session
  autoLogout: z.boolean().optional(),
  sessionDurationMinutes: z.number().min(0).optional(),
  rememberLogin: z.boolean().optional(),
  // Appearance
  colorTheme: z.enum(["Indigo", "Violeta", "Esmeralda", "Azul", "Rosa", "Naranja"]).optional(),
  animationsEnabled: z.boolean().optional(),
  // Notifications (extended)
  emailNotifications: z.boolean().optional(),
  // Language (extended)
  dateFormat: z.enum(["ddmmyyyy", "mmddyyyy", "yyyymmdd"]).optional(),
  timezone: z.enum(["gmt-5", "gmt-6", "gmt-3", "gmt0", "gmt1"]).optional(),
});

export type TeacherSettingsFormData = z.infer<typeof TeacherSettingsSchema>;

export async function saveTeacherSettings(
  data: TeacherSettingsFormData
): Promise<{ success: boolean; message: string }> {
  // Validar con Zod
  const parsed = TeacherSettingsSchema.safeParse(data);

  if (!parsed.success) {
    const errors = parsed.error.issues.map((i) => i.message).join(", ");
    return {
      success: false,
      message: `Datos inválidos: ${errors}`,
    };
  }

  try {
    const { updateTeacherSettings } = await import("@/services/users");

    // Mapear camelCase → snake_case para el API
    const snakeCaseData = {
      theme: parsed.data.theme,
      notifications_enabled: parsed.data.notificationsEnabled,
      notification_frequency: parsed.data.notificationFrequency,
      interface_language: parsed.data.interfaceLanguage,
      auto_logout: parsed.data.autoLogout,
      session_duration_minutes: parsed.data.sessionDurationMinutes,
      remember_login: parsed.data.rememberLogin,
      color_theme: parsed.data.colorTheme,
      animations_enabled: parsed.data.animationsEnabled,
      email_notifications: parsed.data.emailNotifications,
      date_format: parsed.data.dateFormat,
      timezone: parsed.data.timezone,
    };

    // Filtrar campos undefined
    const filtered = Object.fromEntries(
      Object.entries(snakeCaseData).filter(([, v]) => v !== undefined)
    );

    await updateTeacherSettings(filtered);

    return {
      success: true,
      message: "Configuración guardada exitosamente",
    };
  } catch (error) {
    console.error("Error saving settings:", error);
    return {
      success: false,
      message: "Error al guardar la configuración",
    };
  }
}
