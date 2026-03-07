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
import { Mail, MessageCircle, ChevronLeft, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
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
  const [courseFilter, setCourseFilter] = useState<string>(initialCourses[0] || "");

  // Filter students based on search term and course filter
  const filteredStudents = initialStudents.filter(
    (student) =>
      (student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
       student.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
       student.maxLevel.toString().includes(searchTerm)) &&
      (courseFilter === "" || student.course === courseFilter)
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

  // Handle rows per page change
  const handleRowsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setRowsPerPage(Number(e.target.value));
    setCurrentPage(1); // Reset to first page when changing rows per page
  };

  // Handle course filter change
  const handleCourseFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setCourseFilter(e.target.value);
    setCurrentPage(1); // Reset to first page when changing course filter
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
    <div className="container mx-auto py-10">
      <div className="mb-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">Gestión de Estudiantes</h1>
            <p className="text-muted-foreground">
              Vista general de todos los estudiantes registrados en la plataforma
            </p>
          </div>
          <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
            <DialogTrigger asChild>
              <Button>Crear Nuevo Estudiante</Button>
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
      </div>

      {/* Filter section */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <div className="w-full sm:w-auto flex flex-col sm:flex-row gap-2">
          <Input
            placeholder="Buscar estudiantes..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1); // Reset to first page when searching
            }}
            className="max-w-sm"
          />
          <select
            value={courseFilter}
            onChange={handleCourseFilterChange}
            className="border rounded px-2 py-1 text-sm"
          >
            <option value="">Todos los cursos</option>
            {initialCourses.map((course) => (
              <option key={course} value={course}>
                {course}
              </option>
            ))}
          </select>
          {selectedStudents.size > 0 && (
            <Button 
              variant="destructive" 
              size="sm"
              onClick={handleDeleteClick}
            >
              Eliminar {selectedStudents.size} estudiante{selectedStudents.size !== 1 ? 's' : ''}
            </Button>
          )}
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-sm">Filas por página:</span>
          <select
            value={rowsPerPage}
            onChange={handleRowsPerPageChange}
            className="border rounded px-2 py-1 text-sm"
          >
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
          </select>
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

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[50px]">
                <input
                  type="checkbox"
                  className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  checked={selectedStudents.size === currentStudents.length && currentStudents.length > 0}
                  aria-label="Seleccionar todos los estudiantes de esta página"
                  onChange={(e) => {
                    if (e.target.checked) {
                      // Select all current students
                      const newSelected = new Set(selectedStudents);
                      currentStudents.forEach(student => newSelected.add(student.id));
                      setSelectedStudents(newSelected);
                    } else {
                      // Deselect all current students
                      const newSelected = new Set(selectedStudents);
                      currentStudents.forEach(student => newSelected.delete(student.id));
                      setSelectedStudents(newSelected);
                    }
                  }}
                />
              </TableHead>
              <TableHead>Nombre</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead>Nivel Máximo</TableHead>
              <TableHead>Curso</TableHead>
              <TableHead>Correo Electrónico</TableHead>
              <TableHead>Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentStudents.length > 0 ? (
              currentStudents.map((student) => (
                <TableRow
                  key={student.id}
                  className={`cursor-pointer hover:bg-muted/50 transition-colors ${selectedStudents.has(student.id) ? 'bg-muted' : ''}`}
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
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
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
                      onClick={(e) => e.stopPropagation()} // Prevent row click when checkbox is clicked
                    />
                  </TableCell>
                  <TableCell className="font-medium">{student.name}</TableCell>
                  <TableCell>
                    {student.status === "active" ? (
                      <Badge className="bg-emerald-100 text-emerald-800 border-emerald-200 hover:bg-emerald-200">
                        Activo
                      </Badge>
                    ) : student.status === "inactive" ? (
                      <Badge className="bg-amber-100 text-amber-800 border-amber-200 hover:bg-amber-200">
                        Inactivo
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="border-red-200 text-red-700 bg-red-50">
                        No Registrado
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>
                    <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
                      Nivel {student.maxLevel}
                    </span>
                  </TableCell>
                  <TableCell>{student.course}</TableCell>
                  <TableCell>{student.email}</TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          window.location.href = `mailto:${student.email}`;
                        }}
                      >
                        <Mail className="h-4 w-4 mr-1" />
                        Correo
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          // Enviar feedback al estudiante con toast moderno
                          notifications.success(
                            `Redirigiendo para enviar feedback a ${student.name}`,
                            {
                              description: "Serás redirigido a la página de feedback del estudiante."
                            }
                          );
                        }}
                      >
                        <MessageCircle className="h-4 w-4 mr-1" />
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
                  className="text-center py-8 text-muted-foreground"
                >
                  No se encontraron estudiantes
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination controls */}
      {totalPages > 1 && (
        <div className="flex flex-col sm:flex-row items-center justify-between mt-4 gap-4">
          <div className="text-sm text-muted-foreground">
            Mostrando {startIndex + 1}-
            {Math.min(endIndex, filteredStudents.length)} de{" "}
            {filteredStudents.length} estudiantes
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>

            <div className="flex items-center space-x-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                (page) => (
                  <Button
                    key={page}
                    variant={currentPage === page ? "default" : "outline"}
                    size="sm"
                    onClick={() => handlePageChange(page)}
                    className={currentPage === page ? "bg-blue-600" : ""}
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
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}