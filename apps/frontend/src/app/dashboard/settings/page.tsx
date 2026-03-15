'use client';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { 
  Settings, 
  Bell, 
  Globe, 
  Lock, 
  Activity, 
  Mail, 
  Calendar,
  Monitor,
  Palette,
  Database,
  Server
} from "lucide-react";
import { useState } from "react";

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("session");

  // Define sections and their corresponding icons
  const sections = [
    { id: "session", title: "Sesión", icon: Activity },
    { id: "general", title: "General", icon: Monitor },
    { id: "appearance", title: "Apariencia", icon: Palette },
    { id: "notifications", title: "Notificaciones", icon: Bell },
    { id: "security", title: "Seguridad", icon: Lock },
    { id: "emails", title: "Correos", icon: Mail },
    { id: "language", title: "Idioma", icon: Globe },
    { id: "integrations", title: "Integraciones", icon: Database },
    { id: "scheduling", title: "Planificación", icon: Calendar },
    { id: "advanced", title: "Avanzado", icon: Server },
  ];

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
            Configuración de la Plataforma
          </h1>
          <p className="text-muted-foreground text-lg">
            Gestiona las configuraciones de la plataforma y tu experiencia de usuario
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Sidebar Navigation */}
        <div className="lg:col-span-1 space-y-2">
          {sections.map((section) => {
            const IconComponent = section.icon;
            return (
              <Button
                key={section.id}
                variant={activeSection === section.id ? "secondary" : "ghost"}
                className="w-full justify-start"
                onClick={() => setActiveSection(section.id)}
              >
                <IconComponent className="h-4 w-4 mr-2" />
                {section.title}
              </Button>
            );
          })}
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3 space-y-6">
          {/* Session Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Configuración de Sesión</CardTitle>
              <CardDescription>
                Gestiona las preferencias específicas de tu sesión actual
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Auto-logout</Label>
                    <p className="text-sm text-muted-foreground">Cerrar sesión automáticamente después de inactividad</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator />
                <div className="space-y-2">
                  <Label>Duración de la Sesión</Label>
                  <Select>
                    <SelectTrigger className="w-[200px]">
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
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Recordar Inicio de Sesión</Label>
                    <p className="text-sm text-muted-foreground">Mantener sesión iniciada en este dispositivo</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator />
                <div className="space-y-2">
                  <Label>Notificaciones de Sesión</Label>
                  <div className="flex space-x-2">
                    <Button variant="outline" size="sm">Sesión por expirar</Button>
                    <Button variant="outline" size="sm">Sesión cerrada</Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* General Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Configuración General</CardTitle>
              <CardDescription>
                Configura las preferencias generales de la plataforma
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Modo Oscuro</Label>
                    <p className="text-sm text-muted-foreground">Cambiar entre temas claro y oscuro</p>
                  </div>
                  <Switch />
                </div>
                <Separator />
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Notificaciones Push</Label>
                    <p className="text-sm text-muted-foreground">Recibir notificaciones en el navegador</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator />
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Modo para Docentes</Label>
                    <p className="text-sm text-muted-foreground">Mostrar herramientas avanzadas para docentes</p>
                  </div>
                  <Switch defaultChecked />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Notification Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Configuración de Notificaciones</CardTitle>
              <CardDescription>
                Personaliza qué notificaciones recibes y cómo
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label>Nuevas Actividades de Estudiantes</Label>
                  <p className="text-sm text-muted-foreground">Recibir notificaciones cuando los estudiantes completan niveles</p>
                </div>
                <Switch defaultChecked />
              </div>
              <Separator />
              <div className="flex items-center justify-between">
                <div>
                  <Label>Comentarios de Estudiantes</Label>
                  <p className="text-sm text-muted-foreground">Notificaciones cuando los estudiantes envían comentarios</p>
                </div>
                <Switch />
              </div>
              <Separator />
              <div className="flex items-center justify-between">
                <div>
                  <Label>Reportes de Progreso Semanales</Label>
                  <p className="text-sm text-muted-foreground">Resumen semanal de progreso de estudiantes</p>
                </div>
                <Switch />
              </div>
              <Separator />
              <div className="flex items-center justify-between">
                <div>
                  <Label>Alertas de Seguridad</Label>
                  <p className="text-sm text-muted-foreground">Alertas importantes sobre la seguridad de la cuenta</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>

          {/* Integration Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Integraciones de Plataforma</CardTitle>
              <CardDescription>
                Conecta con otras plataformas educativas
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-primary p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-school text-white">
                      <path d="M14 22v-4a2 2 0 1 0-4 0v4"></path>
                      <path d="M18 8h-6"></path>
                      <path d="M10 8H4"></path>
                      <path d="M18 12H4"></path>
                      <path d="m8 16-3 3 3 3"></path>
                      <path d="m16 19-3-3 3-3"></path>
                      <path d="M16 16c-2 0-3 1-3 3 0 1 1 3 3 3 2 0 3-1 3-3 0-2-1-3-3-3Z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold">Google Classroom</h3>
                    <p className="text-sm text-muted-foreground">Integración para sincronizar estudiantes y clases</p>
                  </div>
                </div>
                <Button variant="outline">Configurar</Button>
              </div>
              
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-green-600 p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-languages text-white">
                      <path d="m5 8 6 6"></path>
                      <path d="m4 14 6-6 2-3"></path>
                      <path d="M2 5h12"></path>
                      <path d="M7 2h1"></path>
                      <path d="m22 22-5-10-5 10"></path>
                      <path d="M14 18h6"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold">Moodle</h3>
                    <p className="text-sm text-muted-foreground">Sincronización de cursos y calificaciones</p>
                  </div>
                </div>
                <Button variant="outline">Configurar</Button>
              </div>
              
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-primary p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-book-open text-white">
                      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold">Canvas LMS</h3>
                    <p className="text-sm text-muted-foreground">Integración para plataformas educativas Canvas</p>
                  </div>
                </div>
                <Button variant="outline">Configurar</Button>
              </div>
            </CardContent>
          </Card>

          {/* Advanced Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Configuración Avanzada</CardTitle>
              <CardDescription>
                Opciones avanzadas para usuarios experimentados
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Idioma de la Interfaz</Label>
                <Select>
                  <SelectTrigger className="w-[200px]">
                    <SelectValue placeholder="Seleccionar idioma" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="es">Español</SelectItem>
                    <SelectItem value="en">English</SelectItem>
                    <SelectItem value="fr">Français</SelectItem>
                    <SelectItem value="de">Deutsch</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label>Formato de Fecha</Label>
                <Select>
                  <SelectTrigger className="w-[200px]">
                    <SelectValue placeholder="Seleccionar formato" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ddmmyyyy">DD/MM/YYYY</SelectItem>
                    <SelectItem value="mmddyyyy">MM/DD/YYYY</SelectItem>
                    <SelectItem value="yyyymmdd">YYYY/MM/DD</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label>Zona Horaria</Label>
                <Select>
                  <SelectTrigger className="w-[300px]">
                    <SelectValue placeholder="Seleccionar zona horaria" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="gmt-5">GMT-5 (Colombia)</SelectItem>
                    <SelectItem value="gmt-6">GMT-6 (México)</SelectItem>
                    <SelectItem value="gmt-8">GMT-8 (Estados Unidos)</SelectItem>
                    <SelectItem value="gmt0">GMT+0 (Reino Unido)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="flex items-center justify-between pt-4">
                <div>
                  <Label>Modo Desarrollador</Label>
                  <p className="text-sm text-muted-foreground">Mostrar herramientas de depuración y desarrollo</p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>

          {/* Save Button */}
          <div className="flex justify-end">
            <Button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/25">
              <SaveButtonIcon />
              Guardar Cambios
            </Button>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}

// Helper component for the save button icon
function SaveButtonIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-save">
      <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
      <polyline points="17 21 17 13 7 13 7 21"></polyline>
      <polyline points="7 3 7 8 15 8"></polyline>
    </svg>
  );
}