'use client';

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import { 
  Settings, 
  Bell, 
  Globe, 
  Lock, 
  Activity, 
  Palette,
  Database,
  Save
} from "lucide-react";

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

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("session");

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
                  <Switch defaultChecked />
                </div>
                <Separator />
                <div className="space-y-3">
                  <Label className="text-base font-medium">Duración de la Sesión</Label>
                  <Select defaultValue="60">
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
                  <Switch defaultChecked />
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
                  <ThemeToggle />
                </div>
                <Separator />
                <div className="space-y-3">
                  <Label className="text-base font-medium">Tema de Color</Label>
                  <div className="grid grid-cols-3 gap-3">
                    {["Indigo", "Violeta", "Esmeralda", "Azul", "Rosa", "Naranja"].map((color) => (
                      <button
                        key={color}
                        className={`p-4 rounded-xl border-2 transition-all ${
                          color === "Indigo" 
                            ? "border-primary bg-primary/10" 
                            : "border-border hover:border-primary/50"
                        }`}
                      >
                        <div className={`w-8 h-8 rounded-full mx-auto mb-2 ${
                          color === "Indigo" ? "bg-indigo-500" :
                          color === "Violeta" ? "bg-violet-500" :
                          color === "Esmeralda" ? "bg-emerald-500" :
                          color === "Azul" ? "bg-blue-500" :
                          color === "Rosa" ? "bg-pink-500" : "bg-orange-500"
                        }`} />
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
                  <Switch defaultChecked />
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
                <Switch defaultChecked />
              </div>
              <Separator />
              <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
                <div className="space-y-1">
                  <Label className="text-base font-medium">Correo Electrónico</Label>
                  <p className="text-sm text-muted-foreground">Resumen diario por email</p>
                </div>
                <Switch defaultChecked />
              </div>
              <Separator />
              <div className="space-y-3">
                <Label className="text-base font-medium">Notificaciones de Actividad</Label>
                {[
                  { label: "Nuevas actividades de estudiantes", description: "Cuando completan niveles", enabled: true },
                  { label: "Comentarios de estudiantes", description: "Cuando envían comentarios", enabled: false },
                  { label: "Reportes semanales", description: "Resumen de progreso", enabled: true },
                  { label: "Alertas de seguridad", description: "Avisos importantes de cuenta", enabled: true },
                ].map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/30 transition-colors">
                    <div>
                      <p className="font-medium text-sm">{item.label}</p>
                      <p className="text-xs text-muted-foreground">{item.description}</p>
                    </div>
                    <Switch defaultChecked={item.enabled} />
                  </div>
                ))}
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
                      className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${
                        lang.code === "es" 
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
                <Select defaultValue="ddmmyyyy">
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
                <Select defaultValue="gmt-5">
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
              {[
                { name: "Google Classroom", description: "Sincronizar estudiantes y clases", icon: "🎓", connected: false, color: "bg-blue-500" },
                { name: "Moodle", description: "Importar cursos y calificaciones", icon: "📚", connected: true, color: "bg-orange-500" },
                { name: "Canvas LMS", description: "Integración con Canvas", icon: "📖", connected: false, color: "bg-red-500" },
              ].map((integration, index) => (
                <div key={index} className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30">
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Grid Pattern Overlay */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="container mx-auto py-10 px-6 relative z-10">
        {/* Header */}
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

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
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

          {/* Main Content */}
          <div className="lg:col-span-3">
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-300">
              {renderSectionContent()}
            </div>

            {/* Save Button */}
            <div className="flex justify-end mt-6">
              <Button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/25">
                <Save className="h-4 w-4" />
                Guardar Cambios
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
