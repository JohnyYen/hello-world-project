"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import {
  Bell,
  Globe,
  Lock,
  Activity,
  Palette,
  Database,
  Save,
  Check,
  Loader2,
} from "lucide-react";
import type { TeacherSettingsData } from "@/app/dashboard/settings/page";
import { saveTeacherSettings, type TeacherSettingsFormData } from "@/app/actions/settings";

interface SettingsSection {
  id: string;
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
}

const sections: SettingsSection[] = [
  { id: "session", title: "Sesión", description: "Configuración de sesión y autenticación", icon: Activity },
  { id: "appearance", title: "Apariencia", description: "Tema, colores y visualización", icon: Palette },
  { id: "notifications", title: "Notificaciones", description: "Cómo recibes tus notificaciones", icon: Bell },
  { id: "language", title: "Idioma", description: "Idioma y preferencias regionales", icon: Globe },
  { id: "security", title: "Seguridad", description: "Protección y privacidad de tu cuenta", icon: Lock },
  { id: "integrations", title: "Integraciones", description: "Conexión con servicios externos", icon: Database },
];

interface SettingsContentProps {
  initialSettings: TeacherSettingsData;
}

export function SettingsContent({ initialSettings }: SettingsContentProps) {
  const [activeSection, setActiveSection] = useState("session");
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<"idle" | "success" | "error">("idle");

  // Local state for all settings
  const [settings, setSettings] = useState<TeacherSettingsFormData>({
    theme: initialSettings.theme as "light" | "dark",
    notificationsEnabled: initialSettings.notificationsEnabled,
    notificationFrequency: initialSettings.notificationFrequency as "realtime" | "daily" | "weekly" | "disabled",
    interfaceLanguage: initialSettings.interfaceLanguage as "es" | "en",
    autoLogout: initialSettings.autoLogout,
    sessionDurationMinutes: initialSettings.sessionDurationMinutes,
    rememberLogin: initialSettings.rememberLogin,
    colorTheme: initialSettings.colorTheme as "Indigo" | "Violeta" | "Esmeralda" | "Azul" | "Rosa" | "Naranja",
    animationsEnabled: initialSettings.animationsEnabled,
    emailNotifications: initialSettings.emailNotifications,
    dateFormat: initialSettings.dateFormat as "ddmmyyyy" | "mmddyyyy" | "yyyymmdd",
    timezone: initialSettings.timezone as "gmt-5" | "gmt-6" | "gmt-3" | "gmt0" | "gmt1",
  });

  const updateSetting = <K extends keyof TeacherSettingsFormData>(
    key: K,
    value: TeacherSettingsFormData[K]
  ) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
    setSaveStatus("idle");
  };

  const handleSave = async () => {
    setIsSaving(true);
    setSaveStatus("idle");

    const result = await saveTeacherSettings(settings);

    setIsSaving(false);
    setSaveStatus(result.success ? "success" : "error");

    // Reset status after 3 seconds
    setTimeout(() => setSaveStatus("idle"), 3000);
  };

  const themeColors = ["Indigo", "Violeta", "Esmeralda", "Azul", "Rosa", "Naranja"];

  const colorMap: Record<string, string> = {
    Indigo: "bg-indigo-500",
    Violeta: "bg-violet-500",
    Esmeralda: "bg-emerald-500",
    Azul: "bg-blue-500",
    Rosa: "bg-pink-500",
    Naranja: "bg-orange-500",
  };

  const integrations = [
    { name: "Google Classroom", description: "Sincronizar estudiantes y clases", icon: "🎓", connected: false, color: "bg-blue-500" },
    { name: "Moodle", description: "Importar cursos y calificaciones", icon: "📚", connected: true, color: "bg-orange-500" },
    { name: "Canvas LMS", description: "Integración con Canvas", icon: "📖", connected: false, color: "bg-red-500" },
  ];

  const renderSectionContent = () => {
    switch (activeSection) {
      case "session":
        return (
          <Card className="border-border/50 shadow-lg shadow-primary/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5 text-primary" />
                Configuración de Sesión
              </CardTitle>
              <CardDescription>
                Gestiona las preferencias específicas de tu sesión actual
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                  <div className="space-y-1">
                    <Label className="text-base font-medium">Cierre Automático</Label>
                    <p className="text-sm text-muted-foreground">Cerrar sesión automáticamente después de inactividad</p>
                  </div>
                  <Switch
                    checked={settings.autoLogout}
                    onCheckedChange={(checked) => updateSetting("autoLogout", checked)}
                  />
                </div>
                <Separator />
                <div className="space-y-3">
                  <Label className="text-base font-medium">Duración de la Sesión</Label>
                  <Select
                    value={String(settings.sessionDurationMinutes)}
                    onValueChange={(value) => updateSetting("sessionDurationMinutes", parseInt(value))}
                  >
                    <SelectTrigger className="w-[200px] bg-muted/30">
                      <SelectValue placeholder="Seleccionar duración" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="15">15 minutos</SelectItem>
                      <SelectItem value="30">30 minutos</SelectItem>
                      <SelectItem value="60">1 hora</SelectItem>
                      <SelectItem value="120">2 horas</SelectItem>
                      <SelectItem value="0">Sesión permanente</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Separator />
                <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                  <div className="space-y-1">
                    <Label className="text-base font-medium">Recordar Inicio de Sesión</Label>
                    <p className="text-sm text-muted-foreground">Mantener sesión iniciada en este dispositivo</p>
                  </div>
                  <Switch
                    checked={settings.rememberLogin}
                    onCheckedChange={(checked) => updateSetting("rememberLogin", checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        );

      case "appearance":
        return (
          <Card className="border-border/50 shadow-lg shadow-primary/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Palette className="h-5 w-5 text-primary" />
                Apariencia
              </CardTitle>
              <CardDescription>
                Personaliza cómo se ve la plataforma
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                  <div className="space-y-1">
                    <Label className="text-base font-medium">Modo Oscuro</Label>
                    <p className="text-sm text-muted-foreground">Cambiar entre tema claro y oscuro</p>
                  </div>
                  <ThemeToggle initialTheme={settings.theme} />
                </div>
                <Separator />
                <div className="space-y-3">
                  <Label className="text-base font-medium">Tema de Color</Label>
                  <div className="grid grid-cols-3 gap-3">
                    {themeColors.map((color) => (
                      <button
                        key={color}
                        onClick={() => updateSetting("colorTheme", color as "Indigo" | "Violeta" | "Esmeralda" | "Azul" | "Rosa" | "Naranja")}
                        className={`p-4 rounded-xl border-2 transition-all ${
                          color === settings.colorTheme
                            ? "border-primary bg-primary/10"
                            : "border-border hover:border-primary/50"
                        }`}
                      >
                        <div className={`w-8 h-8 rounded-full mx-auto mb-2 ${colorMap[color]}`} />
                        <span className="text-xs font-medium">{color}</span>
                      </button>
                    ))}
                  </div>
                </div>
                <Separator />
                <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                  <div className="space-y-1">
                    <Label className="text-base font-medium">Animaciones</Label>
                    <p className="text-sm text-muted-foreground">Habilitar animaciones y transiciones</p>
                  </div>
                  <Switch
                    checked={settings.animationsEnabled}
                    onCheckedChange={(checked) => updateSetting("animationsEnabled", checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        );

      case "notifications":
        return (
          <Card className="border-border/50 shadow-lg shadow-primary/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-primary" />
                Notificaciones
              </CardTitle>
              <CardDescription>
                Configura cómo y cuándo recibes notificaciones
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                <div className="space-y-1">
                  <Label className="text-base font-medium">Notificaciones Push</Label>
                  <p className="text-sm text-muted-foreground">Recibir notificaciones en el navegador</p>
                </div>
                <Switch
                  checked={settings.notificationsEnabled}
                  onCheckedChange={(checked) => updateSetting("notificationsEnabled", checked)}
                />
              </div>
              <Separator />
              <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                <div className="space-y-1">
                  <Label className="text-base font-medium">Correo Electrónico</Label>
                  <p className="text-sm text-muted-foreground">Resumen diario por email</p>
                </div>
                <Switch
                  checked={settings.emailNotifications}
                  onCheckedChange={(checked) => updateSetting("emailNotifications", checked)}
                />
              </div>
              <Separator />
              <div className="space-y-3">
                <Label className="text-base font-medium">Frecuencia de Resumen</Label>
                <Select
                  value={settings.notificationFrequency}
                  onValueChange={(value) => updateSetting("notificationFrequency", value as "realtime" | "daily" | "weekly" | "disabled")}
                >
                  <SelectTrigger className="w-[200px] bg-muted/30">
                    <SelectValue placeholder="Seleccionar frecuencia" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="realtime">En tiempo real</SelectItem>
                    <SelectItem value="daily">Diario</SelectItem>
                    <SelectItem value="weekly">Semanal</SelectItem>
                    <SelectItem value="disabled">Desactivado</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        );

      case "language":
        return (
          <Card className="border-border/50 shadow-lg shadow-primary/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5 text-primary" />
                Idioma y Región
              </CardTitle>
              <CardDescription>
                Configura el idioma y las preferencias regionales
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <Label className="text-base font-medium">Idioma de la Interfaz</Label>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { code: "es", label: "Español", flag: "🇪🇸" },
                    { code: "en", label: "English", flag: "🇺🇸" },
                  ].map((lang) => (
                    <button
                      key={lang.code}
                      onClick={() => updateSetting("interfaceLanguage", lang.code as "es" | "en")}
                      className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${
                        lang.code === settings.interfaceLanguage
                          ? "border-primary bg-primary/10"
                          : "border-border hover:border-primary/50"
                      }`}
                    >
                      <span className="text-2xl">{lang.flag}</span>
                      <span className="font-medium">{lang.label}</span>
                    </button>
                  ))}
                </div>
              </div>
              <Separator />
              <div className="space-y-3">
                <Label className="text-base font-medium">Formato de Fecha</Label>
                <Select
                  value={settings.dateFormat}
                  onValueChange={(value) => updateSetting("dateFormat", value as "ddmmyyyy" | "mmddyyyy" | "yyyymmdd")}
                >
                  <SelectTrigger className="w-[200px] bg-muted/30">
                    <SelectValue placeholder="Seleccionar formato" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ddmmyyyy">DD/MM/YYYY</SelectItem>
                    <SelectItem value="mmddyyyy">MM/DD/YYYY</SelectItem>
                    <SelectItem value="yyyymmdd">YYYY/MM/DD</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Separator />
              <div className="space-y-3">
                <Label className="text-base font-medium">Zona Horaria</Label>
                <Select
                  value={settings.timezone}
                  onValueChange={(value) => updateSetting("timezone", value as "gmt-5" | "gmt-6" | "gmt-3" | "gmt0" | "gmt1")}
                >
                  <SelectTrigger className="w-[300px] bg-muted/30">
                    <SelectValue placeholder="Seleccionar zona horaria" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="gmt-5">GMT-5 (Colombia, Perú)</SelectItem>
                    <SelectItem value="gmt-6">GMT-6 (México)</SelectItem>
                    <SelectItem value="gmt-3">GMT-3 (Argentina)</SelectItem>
                    <SelectItem value="gmt0">GMT+0 (Londres)</SelectItem>
                    <SelectItem value="gmt1">GMT+1 (Madrid)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        );

      case "security":
        return (
          <Card className="border-border/50 shadow-lg shadow-primary/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lock className="h-5 w-5 text-primary" />
                Seguridad
              </CardTitle>
              <CardDescription>
                Protege tu cuenta y privacidad
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                  <div className="space-y-1">
                    <Label className="text-base font-medium">Autenticación de Dos Factores</Label>
                    <p className="text-sm text-muted-foreground">Añade una capa extra de seguridad</p>
                  </div>
                  <Switch />
                </div>
                <Separator />
                <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                  <div className="space-y-1">
                    <Label className="text-base font-medium">Notificaciones de Inicio de Sesión</Label>
                    <p className="text-sm text-muted-foreground">Recibir alertas de nuevos dispositivos</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator />
                <div className="p-4 rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/20">
                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <Label className="text-base font-medium text-amber-700 dark:text-amber-400">Cambiar Contraseña</Label>
                      <p className="text-sm text-amber-600 dark:text-amber-500">Actualiza tu contraseña regularmente</p>
                    </div>
                    <Button variant="outline" className="border-amber-300 text-amber-700 hover:bg-amber-100 dark:border-amber-700 dark:text-amber-400">
                      Actualizar
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        );

      case "integrations":
        return (
          <Card className="border-border/50 shadow-lg shadow-primary/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5 text-primary" />
                Integraciones
              </CardTitle>
              <CardDescription>
                Conecta con servicios externos
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {integrations.map((integration) => (
                <div key={integration.name} className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 ${integration.color} rounded-xl flex items-center justify-center text-white text-xl`}>
                      {integration.icon}
                    </div>
                    <div>
                      <h3 className="font-semibold">{integration.name}</h3>
                      <p className="text-sm text-muted-foreground">{integration.description}</p>
                    </div>
                  </div>
                  <Button variant={integration.connected ? "outline" : "default"}>
                    {integration.connected ? "Configurar" : "Conectar"}
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>
        );

      default:
        return null;
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div className="lg:col-span-1">
        <div className="sticky top-6 space-y-2">
          {sections.map((section) => {
            const IconComponent = section.icon;
            return (
              <Button
                key={section.id}
                variant={activeSection === section.id ? "secondary" : "ghost"}
                className={`w-full justify-start h-auto py-3 px-4 ${
                  activeSection === section.id
                    ? "bg-primary/10 text-primary border-l-2 border-primary"
                    : "hover:bg-muted"
                }`}
                onClick={() => setActiveSection(section.id)}
              >
                <IconComponent className="h-4 w-4 mr-3 flex-shrink-0" />
                <div className="text-left">
                  <div className="font-medium">{section.title}</div>
                  <div className="text-xs text-muted-foreground hidden lg:block">{section.description}</div>
                </div>
              </Button>
            );
          })}
        </div>
      </div>

      <div className="lg:col-span-3">
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-300">
          {renderSectionContent()}
        </div>

        <div className="flex justify-end mt-6">
          <Button
            onClick={handleSave}
            disabled={isSaving}
            className={`flex items-center gap-2 shadow-lg transition-all ${
              saveStatus === "success"
                ? "bg-green-600 hover:bg-green-700 shadow-green-500/25"
                : saveStatus === "error"
                ? "bg-red-600 hover:bg-red-700 shadow-red-500/25"
                : "bg-indigo-600 hover:bg-indigo-700 shadow-indigo-500/25"
            } text-white`}
          >
            {isSaving ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : saveStatus === "success" ? (
              <Check className="h-4 w-4" />
            ) : (
              <Save className="h-4 w-4" />
            )}
            {isSaving
              ? "Guardando..."
              : saveStatus === "success"
              ? "Guardado exitosamente"
              : saveStatus === "error"
              ? "Error al guardar"
              : "Guardar Cambios"}
          </Button>
        </div>
      </div>
    </div>
  );
}
