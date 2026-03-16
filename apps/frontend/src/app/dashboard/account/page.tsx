'use client';

import { ChangePasswordForm } from "@/components/auth";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Camera, User, Mail, Calendar, BookOpen, TrendingUp } from "lucide-react";
import Link from "next/link";

// Mock user data - in a real app, this would come from an API
const mockUser = {
  id: "1",
  name: "Dr. María Rodríguez",
  email: "maria.rodriguez@educacion.com",
  role: "teacher",
  avatar: "/placeholder-avatar.jpg",
  username: "mrodriguez",
  createdAt: "2024-01-15",
  coursesCount: 5,
  studentsCount: 127,
};

export default function AccountPage() {
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
              <User className="h-6 w-6" />
            </div>
            <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
              Cuenta
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400 bg-clip-text text-transparent">
            Mi Perfil
          </h1>
          <p className="text-muted-foreground text-lg">
            Gestiona tu información personal y seguridad de tu cuenta
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Card - Avatar & Basic Info */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="border-border/50 shadow-lg shadow-primary/5 overflow-hidden">
              <div className="h-24 bg-gradient-to-r from-primary via-accent to-primary relative">
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
              </div>
              <CardHeader className="items-center -mt-12 relative">
                <Avatar className="h-28 w-28 ring-4 ring-background shadow-xl">
                  <AvatarImage src={mockUser.avatar} alt={mockUser.name} />
                  <AvatarFallback className="text-2xl bg-gradient-to-br from-primary to-accent text-white">
                    {mockUser.name.split(" ").map((n) => n[0]).join("")}
                  </AvatarFallback>
                </Avatar>
                <div className="text-center mt-3">
                  <h2 className="text-xl font-bold flex items-center justify-center gap-2">
                    {mockUser.name}
                  </h2>
                  <p className="text-sm text-muted-foreground mt-1">@{mockUser.username}</p>
                  <Badge variant="secondary" className="mt-2 bg-primary/10 text-primary border-primary/20">
                    {mockUser.role === "teacher" ? "👨‍🏫 Docente" : "🎓 Estudiante"}
                  </Badge>
                </div>
              </CardHeader>
              <CardHeader className="pt-0">
                <Button variant="outline" className="w-full flex items-center gap-2 hover:bg-primary/10 hover:text-primary hover:border-primary/30 transition-all">
                  <Camera className="h-4 w-4" />
                  Cambiar Foto
                </Button>
              </CardHeader>
            </Card>

            {/* Quick Stats */}
            <Card className="border-border/50 shadow-lg shadow-primary/5">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  Estadísticas
                </CardTitle>
              </CardHeader>
              <div className="px-6 pb-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-primary/10">
                      <Calendar className="h-4 w-4 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Miembro desde</p>
                      <p className="font-medium">{mockUser.createdAt}</p>
                    </div>
                  </div>
                </div>
                <Separator />
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-emerald-500/10">
                      <BookOpen className="h-4 w-4 text-emerald-500" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Cursos activos</p>
                      <p className="font-medium">{mockUser.coursesCount}</p>
                    </div>
                  </div>
                </div>
                <Separator />
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-violet-500/10">
                      <User className="h-4 w-4 text-violet-500" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Estudiantes</p>
                      <p className="font-medium">{mockUser.studentsCount}</p>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          {/* Account Details - Editable Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Personal Information */}
            <Card className="border-border/50 shadow-lg shadow-primary/5">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5 text-primary" />
                  Información Personal
                </CardTitle>
                <CardDescription>
                  Actualiza tu información de perfil
                </CardDescription>
              </CardHeader>
              <div className="px-6 pb-6 space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="name">Nombre Completo</Label>
                    <Input id="name" defaultValue={mockUser.name} className="bg-muted/30" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="username">Nombre de Usuario</Label>
                    <div className="relative">
                      <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">@</span>
                      <Input id="username" defaultValue={mockUser.username} className="pl-7 bg-muted/30" />
                    </div>
                  </div>
                  <div className="space-y-2 md:col-span-2">
                    <Label htmlFor="email">Correo Electrónico</Label>
                    <Input id="email" type="email" defaultValue={mockUser.email} className="bg-muted/30" />
                  </div>
                </div>
                <div className="flex justify-end">
                  <Button className="bg-indigo-600 hover:bg-indigo-700">
                    Guardar Cambios
                  </Button>
                </div>
              </div>
            </Card>

            {/* Change Password */}
            <ChangePasswordForm />

            {/* Link to Settings */}
            <Card className="border-border/50 shadow-lg shadow-primary/5">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <svg className="h-5 w-5 text-primary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  Configuración Adicional
                </CardTitle>
                <CardDescription>
                  Otras opciones de personalización
                </CardDescription>
              </CardHeader>
              <div className="px-6 pb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Link 
                    href="/dashboard/settings" 
                    className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30 hover:border-primary/30 hover:bg-primary/5 transition-all group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-indigo-500/10 group-hover:bg-indigo-500/20 transition-colors">
                        <svg className="h-5 w-5 text-indigo-500" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-medium">Configuración</h3>
                        <p className="text-sm text-muted-foreground">Tema, idioma y más</p>
                      </div>
                    </div>
                    <span className="text-muted-foreground group-hover:translate-x-1 transition-transform">→</span>
                  </Link>

                  <Link 
                    href="/dashboard/notifications" 
                    className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border/30 hover:border-primary/30 hover:bg-primary/5 transition-all group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-amber-500/10 group-hover:bg-amber-500/20 transition-colors">
                        <svg className="h-5 w-5 text-amber-500" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                          <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-medium">Notificaciones</h3>
                        <p className="text-sm text-muted-foreground">Centro de alertas</p>
                      </div>
                    </div>
                    <span className="text-muted-foreground group-hover:translate-x-1 transition-transform">→</span>
                  </Link>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
