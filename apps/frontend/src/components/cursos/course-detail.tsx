"use client";

import { useState } from "react";
import Link from "next/link";
import { useNotifications } from "@/hooks/use-notifications";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  ArrowLeft,
  Calendar,
  BookOpen,
  Users,
  GraduationCap,
  Search,
  UserPlus,
  X,
} from "lucide-react";
import {
  enrollStudents,
  unenrollStudent,
} from "@/app/dashboard/cursos/actions";
import type { CourseDetail, StudentEnrollment } from "@/types/course.interface";
import type { UserResponse } from "@/api/types";
import { cn } from "@/lib/utils";

interface CourseDetailViewProps {
  course: CourseDetail;
  allStudents: UserResponse[];
}

export default function CourseDetailView({
  course,
  allStudents,
}: CourseDetailViewProps) {
  const notifications = useNotifications();
  const [students, setStudents] = useState<StudentEnrollment[]>(
    course.students
  );
  const [enrollDialogOpen, setEnrollDialogOpen] = useState(false);
  const [selectedNewStudents, setSelectedNewStudents] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [unenrollTarget, setUnenrollTarget] = useState<StudentEnrollment | null>(null);
  const [unenrollDialogOpen, setUnenrollDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const enrolledIds = new Set(students.map((s) => s.studentId));

  const availableStudents = allStudents.filter((s) => !enrolledIds.has(s.id));

  const filteredAvailable = availableStudents.filter(
    (s) =>
      s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEnroll = async () => {
    if (selectedNewStudents.length === 0) return;
    setLoading(true);
    const result = await enrollStudents(course.id, selectedNewStudents);
    setLoading(false);
    if (result.success) {
      notifications.success("Estudiantes asignados correctamente");
      setEnrollDialogOpen(false);
      setSelectedNewStudents([]);
      setSearchTerm("");
    } else {
      notifications.error(result.message || "Error al asignar estudiantes");
    }
  };

  const handleUnenroll = async () => {
    if (!unenrollTarget) return;
    setLoading(true);
    const result = await unenrollStudent(course.id, unenrollTarget.studentId);
    setLoading(false);
    if (result.success) {
      notifications.success("Estudiante desasignado correctamente");
      setStudents((prev) =>
        prev.filter((s) => s.studentId !== unenrollTarget.studentId)
      );
      setUnenrollDialogOpen(false);
      setUnenrollTarget(null);
    } else {
      notifications.error(result.message || "Error al desasignar estudiante");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full">
          <defs>
            <pattern id="grid-detail" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid-detail)" />
        </svg>
      </div>

      <div className="bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-600 text-white py-10 px-6 md:px-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        <div className="max-w-7xl mx-auto relative z-10">
          <Link
            href="/dashboard/cursos"
            className="inline-flex items-center gap-2 text-emerald-200 hover:text-white transition-colors mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            Volver a cursos
          </Link>
          <h1 className="text-3xl font-bold tracking-tight mb-2">{course.name}</h1>
          <div className="flex flex-wrap gap-4 text-emerald-100">
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              <span>
                {course.schoolYear} - {course.periodLabel}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4" />
              <span>
                {new Date(course.startDate).toLocaleDateString("es-ES")} →{" "}
                {new Date(course.endDate).toLocaleDateString("es-ES")}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8 relative z-10">
        {course.description && (
          <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-700 shadow-lg p-6 mb-6">
            <h2 className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
              Descripción
            </h2>
            <p className="text-slate-700 dark:text-slate-300">{course.description}</p>
          </div>
        )}

        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-3">
            <Users className="h-5 w-5 text-emerald-500" />
            <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200">
              Estudiantes Inscritos
            </h2>
            <Badge variant="secondary" className="ml-2">
              {students.length}
            </Badge>
          </div>
          <Dialog open={enrollDialogOpen} onOpenChange={setEnrollDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
                <UserPlus className="h-4 w-4 mr-2" />
                Asignar Estudiantes
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Asignar Estudiantes</DialogTitle>
                <DialogDescription>
                  Selecciona los estudiantes para asignar a este curso.
                </DialogDescription>
              </DialogHeader>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar estudiantes..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <ScrollArea className="h-64">
                <div className="space-y-1">
                  {filteredAvailable.length > 0 ? (
                    filteredAvailable.map((student) => (
                      <label
                        key={student.id}
                        className={cn(
                          "flex items-center gap-3 rounded-md px-3 py-2.5 cursor-pointer transition-colors",
                          selectedNewStudents.includes(student.id)
                            ? "bg-primary/10 hover:bg-primary/15"
                            : "hover:bg-muted"
                        )}
                      >
                        <Checkbox
                          checked={selectedNewStudents.includes(student.id)}
                          onCheckedChange={() => {
                            setSelectedNewStudents((prev) =>
                              prev.includes(student.id)
                                ? prev.filter((id) => id !== student.id)
                                : [...prev, student.id]
                            );
                          }}
                        />
                        <div className="flex flex-col">
                          <span className="text-sm font-medium">
                            {student.name} {student.lastname || ""}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {student.email}
                          </span>
                        </div>
                      </label>
                    ))
                  ) : (
                    <p className="text-center text-sm text-muted-foreground py-8">
                      {searchTerm
                        ? "No se encontraron estudiantes"
                        : "No hay estudiantes disponibles"}
                    </p>
                  )}
                </div>
              </ScrollArea>
              <div className="flex justify-end gap-2">
                <Button
                  variant="outline"
                  onClick={() => {
                    setEnrollDialogOpen(false);
                    setSelectedNewStudents([]);
                    setSearchTerm("");
                  }}
                >
                  Cancelar
                </Button>
                <Button
                  onClick={handleEnroll}
                  disabled={selectedNewStudents.length === 0 || loading}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white"
                >
                  {loading
                    ? "Asignando..."
                    : `Asignar (${selectedNewStudents.length})`}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-md shadow-xl overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-700">
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">
                  Nombre
                </TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">
                  Email
                </TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">
                  Fecha de inscripción
                </TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">
                  Acciones
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {students.length > 0 ? (
                students.map((student) => (
                  <TableRow
                    key={student.studentId}
                    className="hover:bg-emerald-50/50 dark:hover:bg-emerald-950/20 transition-all border-b border-slate-100 dark:border-slate-700/50"
                  >
                    <TableCell className="font-medium text-slate-900 dark:text-slate-100">
                      <div className="flex items-center gap-2">
                        <Users className="h-4 w-4 text-slate-400" />
                        {student.name}
                      </div>
                    </TableCell>
                    <TableCell className="text-slate-600 dark:text-slate-400">
                      {student.email}
                    </TableCell>
                    <TableCell className="text-slate-600 dark:text-slate-400">
                      {new Date(student.enrolledAt).toLocaleDateString("es-ES", {
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                      })}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-slate-200 dark:border-slate-700 hover:bg-red-50 dark:hover:bg-red-950/20 hover:border-red-300 dark:hover:border-red-700 hover:text-red-600 dark:hover:text-red-400"
                        onClick={() => {
                          setUnenrollTarget(student);
                          setUnenrollDialogOpen(true);
                        }}
                      >
                        <X className="h-3.5 w-3.5 mr-1" />
                        Desasignar
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={4}
                    className="text-center py-12 text-slate-500 dark:text-slate-400"
                  >
                    <div className="flex flex-col items-center gap-2">
                      <Users className="h-8 w-8 text-slate-300 dark:text-slate-600" />
                      <p>No hay estudiantes inscritos en este curso</p>
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Unenroll Confirmation */}
      <Dialog open={unenrollDialogOpen} onOpenChange={setUnenrollDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Confirmar Desasignación</DialogTitle>
            <DialogDescription>
              {unenrollTarget && (
                <>
                  ¿Estás seguro de desasignar a{" "}
                  <span className="font-medium text-foreground">
                    {unenrollTarget.name}
                  </span>
                  ?
                </>
              )}
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end space-x-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => {
                setUnenrollDialogOpen(false);
                setUnenrollTarget(null);
              }}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button
              type="button"
              variant="destructive"
              onClick={handleUnenroll}
              disabled={loading}
            >
              {loading ? "Desasignando..." : "Desasignar"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
