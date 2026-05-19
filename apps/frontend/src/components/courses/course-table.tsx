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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  ChevronLeft,
  ChevronRight,
  Search,
  BookOpen,
  Users,
  GraduationCap,
  Plus,
  Eye,
  Pencil,
  Trash2,
} from "lucide-react";
import CourseForm from "@/components/courses/course-form";
import { deleteCourse } from "@/app/dashboard/courses/actions";
import type { Course } from "@/types/course.interface";
import type { UserResponse } from "@/api/types";

interface CourseTableProps {
  initialCourses: Course[];
  total: number;
  students: UserResponse[];
  professors: UserResponse[];
}

export default function CourseTable({
  initialCourses,
  total,
  students,
  professors,
}: CourseTableProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;
  const notifications = useNotifications();

  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editCourse, setEditCourse] = useState<Course | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [courseToDelete, setCourseToDelete] = useState<Course | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const filtered = initialCourses.filter(
    (c) =>
      c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.schoolYear.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.periodLabel.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalPages = Math.ceil(filtered.length / rowsPerPage);
  const startIndex = (currentPage - 1) * rowsPerPage;
  const currentItems = filtered.slice(startIndex, startIndex + rowsPerPage);

  const handleDelete = async () => {
    if (!courseToDelete) return;
    setDeleteLoading(true);
    const result = await deleteCourse(courseToDelete.id);
    setDeleteLoading(false);
    setDeleteDialogOpen(false);
    setCourseToDelete(null);
    if (result.success) {
      notifications.success("Curso eliminado correctamente");
    } else {
      notifications.error(result.message || "Error al eliminar el curso");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid-courses" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid-courses)" />
        </svg>
      </div>

      <div className="bg-gradient-to-r from-indigo-600 via-indigo-500 to-violet-600 text-white py-10 px-6 md:px-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="flex items-center gap-3 mb-2">
            <BookOpen className="h-6 w-6 text-indigo-200" />
            <span className="text-sm font-medium text-indigo-200 uppercase tracking-wider">
              Gestión Académica
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">Cursos</h1>
          <p className="text-indigo-100 text-lg max-w-2xl">
            Administración de cursos, estudiantes y profesores
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8 relative z-10">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-4 py-2 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm">
              <BookOpen className="h-4 w-4 text-indigo-500" />
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                {total} cursos
              </span>
            </div>
          </div>
          <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/25">
                <Plus className="h-4 w-4 mr-2" />
                Crear Curso
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Crear Nuevo Curso</DialogTitle>
                <DialogDescription>
                  Completa los datos del nuevo curso. Puedes asignar estudiantes y profesores.
                </DialogDescription>
              </DialogHeader>
              <CourseForm
                students={students}
                professors={professors}
                onSuccess={() => setCreateDialogOpen(false)}
                onCancel={() => setCreateDialogOpen(false)}
              />
            </DialogContent>
          </Dialog>
        </div>

        <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-700 shadow-lg shadow-slate-200/50 dark:shadow-slate-900/50 p-4 mb-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="relative w-full sm:w-72">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <Input
                placeholder="Buscar cursos..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1);
                }}
                className="pl-10 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 focus:border-indigo-500 focus:ring-indigo-500/20"
              />
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-md shadow-xl shadow-slate-200/50 dark:shadow-slate-900/50 overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800/80">
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Nombre</TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Año Escolar</TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Período</TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Estudiantes</TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Profesores</TableHead>
                <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {currentItems.length > 0 ? (
                currentItems.map((course) => (
                  <TableRow
                    key={course.id}
                    className="hover:bg-indigo-50/50 dark:hover:bg-indigo-950/20 transition-all border-b border-slate-100 dark:border-slate-700/50"
                  >
                    <TableCell className="font-medium text-slate-900 dark:text-slate-100">
                      {course.name}
                    </TableCell>
                    <TableCell className="text-slate-700 dark:text-slate-300">
                      {course.schoolYear}
                    </TableCell>
                    <TableCell>
                      <span className="inline-flex items-center rounded-full bg-indigo-100 dark:bg-indigo-900/40 px-3 py-1 text-xs font-semibold text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                        {course.periodLabel}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Users className="h-3.5 w-3.5 text-indigo-500" />
                        <span className="text-slate-700 dark:text-slate-300">{course.studentCount}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <GraduationCap className="h-3.5 w-3.5 text-violet-500" />
                        <span className="text-slate-700 dark:text-slate-300">{course.professorCount}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Link href={`/dashboard/courses/${course.id}`}>
                          <Button
                            variant="outline"
                            size="sm"
                            className="border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 hover:border-indigo-300 dark:hover:border-indigo-700"
                          >
                            <Eye className="h-3.5 w-3.5 mr-1" />
                            Ver detalle
                          </Button>
                        </Link>
                        <Button
                          variant="outline"
                          size="sm"
                          className="border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 hover:border-amber-300 dark:hover:border-amber-700"
                          onClick={() => {
                            setEditCourse(course);
                          }}
                        >
                          <Pencil className="h-3.5 w-3.5 mr-1" />
                          Editar
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          className="border-slate-200 dark:border-slate-700 hover:bg-red-50 dark:hover:bg-red-950/20 hover:border-red-300 dark:hover:border-red-700 hover:text-red-600 dark:hover:text-red-400"
                          onClick={() => {
                            setCourseToDelete(course);
                            setDeleteDialogOpen(true);
                          }}
                        >
                          <Trash2 className="h-3.5 w-3.5 mr-1" />
                          Eliminar
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-16 text-slate-500 dark:text-slate-400">
                    <div className="flex flex-col items-center gap-3">
                      <BookOpen className="h-12 w-12 text-slate-300 dark:text-slate-600" />
                      <p className="text-lg font-medium">No hay cursos registrados</p>
                      <Button
                        className="bg-indigo-600 hover:bg-indigo-700 text-white"
                        onClick={() => setCreateDialogOpen(true)}
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Crear Curso
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

        {totalPages > 1 && (
          <div className="flex flex-col sm:flex-row items-center justify-between mt-6 gap-4">
            <div className="text-sm text-slate-600 dark:text-slate-400 bg-white/60 dark:bg-slate-800/60 px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700">
              Mostrando{" "}
              <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                {startIndex + 1}
              </span>
              -
              <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                {Math.min(startIndex + rowsPerPage, filtered.length)}
              </span>{" "}
              de{" "}
              <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                {filtered.length}
              </span>{" "}
              cursos
            </div>
            <div className="flex items-center gap-1 bg-white/60 dark:bg-slate-800/60 px-2 py-1 rounded-lg border border-slate-200 dark:border-slate-700">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="border-slate-200 dark:border-slate-700"
              >
                <ChevronLeft className="h-4 w-4" />
              </Button>
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <Button
                  key={page}
                  variant={currentPage === page ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setCurrentPage(page)}
                  className={
                    currentPage === page
                      ? "bg-indigo-600 hover:bg-indigo-700 text-white min-w-[2.25rem]"
                      : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                  }
                >
                  {page}
                </Button>
              ))}
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="border-slate-200 dark:border-slate-700"
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Edit Dialog */}
      <Dialog
        open={!!editCourse}
        onOpenChange={(open) => {
          if (!open) setEditCourse(null);
        }}
      >
        <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Editar Curso</DialogTitle>
            <DialogDescription>
              Modifica los datos del curso. Los cambios se guardarán automáticamente.
            </DialogDescription>
          </DialogHeader>
          {editCourse && (
            <CourseForm
              course={editCourse as any}
              students={students}
              professors={professors}
              onSuccess={() => setEditCourse(null)}
              onCancel={() => setEditCourse(null)}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Confirmar Eliminación</DialogTitle>
            <DialogDescription>
              ¿Estás seguro de eliminar este curso? Esta acción no se puede deshacer.
              {courseToDelete && (
                <span className="block mt-2 font-medium text-foreground">
                  &ldquo;{courseToDelete.name}&rdquo; - {courseToDelete.schoolYear}
                </span>
              )}
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end space-x-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setDeleteDialogOpen(false)}
              disabled={deleteLoading}
            >
              Cancelar
            </Button>
            <Button
              type="button"
              variant="destructive"
              onClick={handleDelete}
              disabled={deleteLoading}
            >
              {deleteLoading ? "Eliminando..." : "Eliminar"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
