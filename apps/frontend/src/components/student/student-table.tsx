"use client";

import { useState } from "react";
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
import { Mail, MessageCircle, ChevronLeft, ChevronRight, Users, BookOpen, Search } from "lucide-react";
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import CreateStudentForm from "./create-student-form";
import { Student } from "@/types/index";

type StudentTableProps = {
  initialStudents: Student[];
  initialCourses: string[];
};

export default function StudentTable({ initialStudents, initialCourses }: StudentTableProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const notifications = useNotifications();

  // Set default course filter to the most recent course (first in the sorted list)
  const [courseFilter, setCourseFilter] = useState<string>("all");

  // Filter students based on search term and course filter
  const filteredStudents = initialStudents.filter(
    (student) =>
      (student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
       student.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
       student.maxLevel.toString().includes(searchTerm)) &&
      (courseFilter === "all" || student.course === courseFilter)
  );

  // Calculate pagination values
  const totalPages = Math.ceil(filteredStudents.length / rowsPerPage);
  const startIndex = (currentPage - 1) * rowsPerPage;
  const endIndex = startIndex + rowsPerPage;
  const currentStudents = filteredStudents.slice(startIndex, endIndex);

  // Handle page change
  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  // State for tracking selected students
  const [selectedStudents, setSelectedStudents] = useState<Set<string>>(new Set());

  // States for the create student modal
  const [isModalOpen, setIsModalOpen] = useState(false);

  // State for the delete confirmation dialog
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  // Handle delete button click
  const handleDeleteClick = () => {
    setDeleteDialogOpen(true);
  };

  // Confirm deletion
  const confirmDelete = () => {
    // In a real application, you would call an API to delete the students
    // eslint-disable-next-line no-console -- Debug logging for student deletion
    console.log(`Deleting students:`, Array.from(selectedStudents));
    
    // Reset selections after deletion
    setSelectedStudents(new Set());
    setDeleteDialogOpen(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Background pattern */}
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

      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 via-indigo-500 to-violet-600 text-white py-10 px-6 md:px-12 relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="flex items-center gap-3 mb-2">
            <Users className="h-6 w-6 text-indigo-200" />
            <span className="text-sm font-medium text-indigo-200 uppercase tracking-wider">
              Gestión
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            Estudiantes
          </h1>
          <p className="text-indigo-100 text-lg max-w-2xl">
            Vista general de todos los estudiantes registrados en la plataforma
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8 relative z-10">
        {/* Header Actions */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-4 py-2 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm">
              <Users className="h-4 w-4 text-indigo-500" />
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                {filteredStudents.length} estudiantes
              </span>
            </div>
          </div>
          <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
            <DialogTrigger asChild>
              <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/25">
                Crear Nuevo Estudiante
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Crear Nuevo Estudiante</DialogTitle>
                <DialogDescription>
                  Ingresa los datos del nuevo estudiante aquí. Se creará una cuenta de usuario automáticamente.
                </DialogDescription>
              </DialogHeader>
              <CreateStudentForm 
                onSuccess={() => setIsModalOpen(false)}
                onCancel={() => setIsModalOpen(false)}
              />
            </DialogContent>
          </Dialog>
        </div>

        {/* Filter Card */}
        <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-700 shadow-lg shadow-slate-200/50 dark:shadow-slate-900/50 p-4 mb-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="w-full sm:w-auto flex flex-col sm:flex-row gap-3">
              {/* Search Input */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  placeholder="Buscar estudiantes..."
                  value={searchTerm}
                  onChange={(e) => {
                    setSearchTerm(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="pl-10 w-full sm:w-64 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 focus:border-indigo-500 focus:ring-indigo-500/20"
                />
              </div>
              
              {/* Course Filter - Using shadcn Select */}
              <Select value={courseFilter} onValueChange={(value) => {
                setCourseFilter(value);
                setCurrentPage(1);
              }}>
                <SelectTrigger className="w-full sm:w-56 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 focus:border-indigo-500 focus:ring-indigo-500/20">
                  <div className="flex items-center gap-2">
                    <BookOpen className="h-4 w-4 text-indigo-500" />
                    <SelectValue placeholder="Todos los cursos" />
                  </div>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos los cursos</SelectItem>
                  {initialCourses.map((course) => (
                    <SelectItem key={course} value={course}>
                      {course}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {selectedStudents.size > 0 && (
                <Button 
                  variant="destructive" 
                  size="sm"
                  onClick={handleDeleteClick}
                  className="shadow-lg"
                >
                  Eliminar {selectedStudents.size} estudiante{selectedStudents.size !== 1 ? 's' : ''}
                </Button>
              )}
            </div>

            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-600 dark:text-slate-400">Filas:</span>
              <Select value={rowsPerPage.toString()} onValueChange={(value) => {
                setRowsPerPage(Number(value));
                setCurrentPage(1);
              }}>
                <SelectTrigger className="w-20 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="5">5</SelectItem>
                  <SelectItem value="10">10</SelectItem>
                  <SelectItem value="20">20</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Confirmar Eliminación</DialogTitle>
            <DialogDescription>
              {selectedStudents.size === 1
                ? "¿Estás seguro de que deseas eliminar este estudiante?"
                : `¿Estás seguro de que deseas eliminar ${selectedStudents.size} estudiantes?`}
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end space-x-2">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => setDeleteDialogOpen(false)}
            >
              Cancelar
            </Button>
            <Button 
              type="button" 
              variant="destructive"
              onClick={confirmDelete}
            >
              Eliminar
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-md shadow-xl shadow-slate-200/50 dark:shadow-slate-900/50 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800/80">
              <TableHead className="w-[50px]">
                <input
                  type="checkbox"
                  className="h-4 w-4 rounded border-slate-300 dark:border-slate-600 text-indigo-600 focus:ring-indigo-500"
                  checked={selectedStudents.size === currentStudents.length && currentStudents.length > 0}
                  aria-label="Seleccionar todos los estudiantes de esta página"
                  onChange={(e) => {
                    if (e.target.checked) {
                      const newSelected = new Set(selectedStudents);
                      currentStudents.forEach(student => newSelected.add(student.id));
                      setSelectedStudents(newSelected);
                    } else {
                      const newSelected = new Set(selectedStudents);
                      currentStudents.forEach(student => newSelected.delete(student.id));
                      setSelectedStudents(newSelected);
                    }
                  }}
                />
              </TableHead>
              <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Nombre</TableHead>
              <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Estado</TableHead>
              <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Nivel</TableHead>
              <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Curso</TableHead>
              <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Correo</TableHead>
              <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentStudents.length > 0 ? (
              currentStudents.map((student) => (
                <TableRow
                  key={student.id}
                  className={`cursor-pointer hover:bg-indigo-50/50 dark:hover:bg-indigo-950/20 transition-all border-b border-slate-100 dark:border-slate-700/50 ${selectedStudents.has(student.id) ? 'bg-indigo-50/70 dark:bg-indigo-950/30' : ''}`}
                  onClick={() =>
                    (window.location.href = `/dashboard/students/${student.id}`)
                  }
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      window.location.href = `/dashboard/students/${student.id}`;
                    }
                  }}
                  tabIndex={0}
                  role="button"
                  aria-label={`Ver detalles de ${student.name}`}
                >
                  <TableCell>
                  <input
                      type="checkbox"
                      className="h-4 w-4 rounded border-slate-300 dark:border-slate-600 text-indigo-600 focus:ring-indigo-500"
                      aria-label={`Seleccionar estudiante ${student.name}`}
                      checked={selectedStudents.has(student.id)}
                      onChange={(e) => {
                          const newSelected = new Set(selectedStudents);
                          if (e.target.checked) {
                            newSelected.add(student.id);
                          } else {
                            newSelected.delete(student.id);
                          }
                          setSelectedStudents(newSelected);
                        }}
                        onClick={(e) => e.stopPropagation()}
                    />
                  </TableCell>
                  <TableCell className="font-medium text-slate-900 dark:text-slate-100">{student.name}</TableCell>
                  <TableCell>
                    {student.status === "active" ? (
                      <Badge className="bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 dark:hover:bg-emerald-900/40">
                        Activo
                      </Badge>
                    ) : student.status === "inactive" ? (
                      <Badge className="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800 hover:bg-red-100 dark:hover:bg-red-900/40">
                        Inactivo
                      </Badge>
                    ) : (
                      <Badge className="bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 border-orange-200 dark:border-orange-800 hover:bg-orange-100 dark:hover:bg-orange-900/40">
                        Pendiente
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>
                    <span className="inline-flex items-center rounded-full bg-indigo-100 dark:bg-indigo-900/40 px-3 py-1 text-xs font-semibold text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                      Nivel {student.maxLevel}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <BookOpen className="h-3.5 w-3.5 text-violet-500" />
                      <span className="text-slate-700 dark:text-slate-300">{student.course}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Mail className="h-3.5 w-3.5 text-slate-400" />
                      <span className="text-slate-600 dark:text-slate-400">{student.email}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 hover:border-indigo-300 dark:hover:border-indigo-700"
                        onClick={(e) => {
                          e.stopPropagation();
                          window.location.href = `mailto:${student.email}`;
                        }}
                      >
                        <Mail className="h-3.5 w-3.5 mr-1" />
                        Correo
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 hover:border-indigo-300 dark:hover:border-indigo-700"
                        onClick={(e) => {
                          e.stopPropagation();
                          notifications.success(
                            `Redirigiendo para enviar feedback a ${student.name}`,
                            {
                              description: "Serás redirigido a la página de feedback del estudiante."
                            }
                          );
                        }}
                      >
                        <MessageCircle className="h-3.5 w-3.5 mr-1" />
                        Feedback
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={7}
                  className="text-center py-12 text-slate-500 dark:text-slate-400"
                >
                  <div className="flex flex-col items-center gap-2">
                    <Users className="h-8 w-8 text-slate-300 dark:text-slate-600" />
                    <p>No se encontraron estudiantes</p>
                  </div>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination controls */}
      {totalPages > 1 && (
        <div className="flex flex-col sm:flex-row items-center justify-between mt-6 gap-4">
          <div className="text-sm text-slate-600 dark:text-slate-400 bg-white/60 dark:bg-slate-800/60 px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700">
            Mostrando <span className="font-semibold text-indigo-600 dark:text-indigo-400">{startIndex + 1}</span>-
            <span className="font-semibold text-indigo-600 dark:text-indigo-400">{Math.min(endIndex, filteredStudents.length)}</span> de{" "}
            <span className="font-semibold text-indigo-600 dark:text-indigo-400">{filteredStudents.length}</span> estudiantes
          </div>

          <div className="flex items-center gap-1 bg-white/60 dark:bg-slate-800/60 px-2 py-1 rounded-lg border border-slate-200 dark:border-slate-700">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>

            <div className="flex items-center gap-1 px-2">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                (page) => (
                  <Button
                    key={page}
                    variant={currentPage === page ? "default" : "ghost"}
                    size="sm"
                    onClick={() => handlePageChange(page)}
                    className={currentPage === page ? "bg-indigo-600 hover:bg-indigo-700 text-white min-w-[2.25rem]" : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-indigo-600 dark:hover:text-indigo-400"}
                  >
                    {page}
                  </Button>
                )
              )}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}