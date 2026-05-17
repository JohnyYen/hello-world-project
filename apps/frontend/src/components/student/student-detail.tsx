'use client';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Mail, MessageCircle, ChevronLeft, User } from "lucide-react";
import Link from "next/link";
import { Student } from "@/types/index";

type StudentDetailProps = {
  student: Student;
  studentId: string;
};

export default function StudentDetail({ student, studentId }: StudentDetailProps) {
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
        {/* Back Button and Header */}
        <div className="mb-6">
          <Link href="/dashboard/students">
            <Button variant="outline" className="mb-4 border-indigo-200 dark:border-indigo-800 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/30">
              <ChevronLeft className="h-4 w-4 mr-2" />
              Volver a la lista de estudiantes
            </Button>
          </Link>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400">
                  <User className="h-6 w-6" />
                </div>
                <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                  Estudiante
                </span>
              </div>
              <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400 bg-clip-text text-transparent">
                {student.name}
              </h1>
              <p className="text-muted-foreground text-lg">
                Perfil del estudiante
              </p>
            </div>
            <div className="flex space-x-2">
              <Link href={`/dashboard/students/${studentId}/reports`}>
                <Button variant="default" className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/25">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Ver Reportes
                </Button>
              </Link>
              <Button
                variant="outline"
                onClick={() => window.location.href = `mailto:${student.email}`}
                className="border-indigo-200 dark:border-indigo-800"
              >
                <Mail className="h-4 w-4 mr-2" />
                Contactar
              </Button>
              <Button
                variant="outline"
                onClick={() => alert(`Redirigiendo para enviar feedback a ${student.name}`)}
                className="border-indigo-200 dark:border-indigo-800"
              >
                <MessageCircle className="h-4 w-4 mr-2" />
                Feedback
              </Button>
            </div>
          </div>
        </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Student Info Card */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Información del Estudiante</CardTitle>
              <CardDescription>Detalles del perfil del estudiante</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Nombre</p>
                <p className="font-medium">{student.name}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Correo Electrónico</p>
                <p className="font-medium">{student.email}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Estado</p>
                <div>
                  {student.status === "active" ? (
                    <Badge variant="default" className="bg-green-600 text-white">
                      Activo
                    </Badge>
                  ) : student.status === "inactive" ? (
                    <Badge variant="secondary" className="bg-red-600 text-white">
                      Inactivo
                    </Badge>
                  ) : (
                    <Badge variant="outline" className="border-orange-600 text-orange-600">
                      Pendiente
                    </Badge>
                  )}
                </div>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Nivel Máximo</p>
                <p className="font-medium">
                  <span className="inline-flex items-center rounded-full bg-primary/20 px-2.5 py-0.5 text-xs font-medium text-primary">
                    Nivel {student.maxLevel}
                  </span>
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Fecha de Registro</p>
                <p className="font-medium">{new Date(student.registrationDate).toLocaleDateString('es-ES')}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Última Actividad</p>
                <p className="font-medium">{new Date(student.lastActivity).toLocaleDateString('es-ES')}</p>
              </div>
            </CardContent>
          </Card>

          {/* Progress Section */}
          <Card>
            <CardHeader>
              <CardTitle>Progreso del Estudiante</CardTitle>
              <CardDescription>Detalles de avance en el curso</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span>Lecciones Completadas</span>
                  <span className="font-medium">{student.completedLessons} / {student.totalLessons}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    className="bg-primary h-2.5 rounded-full"
                    style={{ width: `${student.progress}%` }}
                  ></div>
                </div>
                <div className="text-right text-sm text-muted-foreground">
                  {student.progress}% completado
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Achievements and Stats */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Logros</CardTitle>
              <CardDescription>Reconocimientos del estudiante</CardDescription>
            </CardHeader>
            <CardContent>
              {student.achievements.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {student.achievements.map((achievement, index) => (
                    <Badge key={index} variant="secondary" className="px-3 py-1">
                      {achievement}
                    </Badge>
                  ))}
                </div>
              ) : (
                <p className="text-muted-foreground">No hay logros registrados</p>
              )}
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle>Estadísticas</CardTitle>
              <CardDescription>Resumen de actividad</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-2xl font-bold">{student.completedLessons}</p>
                <p className="text-sm text-muted-foreground">Lecciones</p>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-2xl font-bold">{student.maxLevel}</p>
                <p className="text-sm text-muted-foreground">Nivel</p>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-2xl font-bold">{student.achievements.length}</p>
                <p className="text-sm text-muted-foreground">Logros</p>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <p className="text-2xl font-bold">{student.progress}%</p>
                <p className="text-sm text-muted-foreground">Progreso</p>
              </div>
            </CardContent>
          </Card>
        </div>
        </div>
      </div>
    </div>
  );
}