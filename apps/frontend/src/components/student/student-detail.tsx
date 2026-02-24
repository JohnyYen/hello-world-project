'use client';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Mail, MessageCircle, ChevronLeft } from "lucide-react";
import Link from "next/link";
import { Student } from "@/types/index";

type StudentDetailProps = {
  student: Student;
  studentId: string;
};

export default function StudentDetail({ student, studentId }: StudentDetailProps) {
  return (
    <div className="container mx-auto py-10">
      <div className="mb-6">
        <Link href="/dashboard/students">
          <Button variant="outline" className="mb-4">
            <ChevronLeft className="h-4 w-4 mr-2" />
            Volver a la lista de estudiantes
          </Button>
        </Link>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">{student.name}</h1>
            <p className="text-muted-foreground">Perfil del estudiante</p>
          </div>
          <div className="flex space-x-2">
            <Link href={`/dashboard/students/${studentId}/reports`}>
              <Button variant="default">
                <MessageCircle className="h-4 w-4 mr-2" />
                Ver Reportes
              </Button>
            </Link>
            <Button
              variant="outline"
              onClick={() => window.location.href = `mailto:${student.email}`}
            >
              <Mail className="h-4 w-4 mr-2" />
              Contactar
            </Button>
            <Button
              variant="outline"
              onClick={() => alert(`Redirigiendo para enviar feedback a ${student.name}`)}
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
                    <Badge variant="secondary" className="bg-yellow-600 text-white">
                      Inactivo
                    </Badge>
                  ) : (
                    <Badge variant="outline" className="border-red-600 text-red-600">
                      No Registrado
                    </Badge>
                  )}
                </div>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Nivel Máximo</p>
                <p className="font-medium">
                  <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
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
                    className="bg-blue-600 h-2.5 rounded-full"
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
  );
}