"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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
  ChevronLeft,
  ChevronRight,
  Pencil,
  Save,
  Gamepad2,
} from "lucide-react";
import {
  enrollStudents,
  unenrollStudent,
  updateCourseInline,
} from "@/app/dashboard/courses/actions";
import type { CourseDetail, StudentEnrollment, ProfessorAssignment } from "@/types/course.interface";
import type { UserResponse } from "@/api/types";
import { cn } from "@/lib/utils";

const MONTHS = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
];

interface CourseDetailViewProps {
  course: CourseDetail;
  allStudents: UserResponse[];
  availableGames: { id: string; title: string }[];
}

export default function CourseDetailView({
  course,
  allStudents,
  availableGames,
}: CourseDetailViewProps) {
  const notifications = useNotifications();
  const router = useRouter();
  const [students, setStudents] = useState<StudentEnrollment[]>(
    course.students
  );
  const [searchTermStudents, setSearchTermStudents] = useState("");
  const [searchTermProfessors, setSearchTermProfessors] = useState("");
  const [searchTermEnroll, setSearchTermEnroll] = useState("");

  const [enrollmentYearFilter, setEnrollmentYearFilter] = useState("");
  const [enrollmentMonthFilter, setEnrollmentMonthFilter] = useState("");

  const [enrollDialogOpen, setEnrollDialogOpen] = useState(false);
  const [selectedNewStudents, setSelectedNewStudents] = useState<string[]>([]);
  const [unenrollTarget, setUnenrollTarget] = useState<StudentEnrollment | null>(null);
  const [unenrollDialogOpen, setUnenrollDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    name: course.name,
    description: course.description ?? "",
    schoolYear: course.schoolYear,
    periodLabel: course.periodLabel,
    startDate: course.startDate,
    endDate: course.endDate,
    gameId: course.game?.id ?? null as string | null,
  });
  const [saving, setSaving] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, string[]> | null>(null);

  const [pageStudents, setPageStudents] = useState(1);
  const [pageProfessors, setPageProfessors] = useState(1);
  const rowsPerPage = 5;

  /* ---------- Helpers ---------- */
  const safeDateLong = (dateStr?: string | null): string => {
    if (!dateStr) return "—";
    const d = new Date(dateStr);
    return isNaN(d.getTime())
      ? "—"
      : d.toLocaleDateString("es-ES", {
          year: "numeric",
          month: "long",
          day: "numeric",
        });
  };

  // StudentEnrollment.studentId (Level 2 = Student profile UUID) ≠ UserResponse.id (Level 1 = User account UUID)
  // Usamos email como clave de comparación porque es único y está disponible en ambos datasets.
  const enrolledEmails = new Set(
    students.map((s) => s.email.toLowerCase().trim())
  );

  const enrollmentYears = [...new Set(
    students
      .filter((s) => s.enrolledAt)
      .map((s) => new Date(s.enrolledAt).getFullYear().toString())
  )].sort((a, b) => b.localeCompare(a));

  const enrollmentMonths = [...new Set(
    students
      .filter((s) => s.enrolledAt)
      .map((s) => new Date(s.enrolledAt).getMonth())
  )].sort((a, b) => a - b);

  const availableStudents = allStudents.filter(
    (s) => !enrolledEmails.has(s.email.toLowerCase().trim())
  );

  const filteredAvailableForEnroll = availableStudents.filter(
    (s) =>
      s.name.toLowerCase().includes(searchTermEnroll.toLowerCase()) ||
      s.email.toLowerCase().includes(searchTermEnroll.toLowerCase())
  );

  const filteredStudentsTable = students.filter((s) => {
    const matchesSearch =
      s.name.toLowerCase().includes(searchTermStudents.toLowerCase()) ||
      s.email.toLowerCase().includes(searchTermStudents.toLowerCase());

    let matchesEnrollment = true;
    if ((enrollmentYearFilter || enrollmentMonthFilter) && s.enrolledAt) {
      const d = new Date(s.enrolledAt);
      if (enrollmentYearFilter && d.getFullYear().toString() !== enrollmentYearFilter) matchesEnrollment = false;
      if (enrollmentMonthFilter && d.getMonth().toString() !== enrollmentMonthFilter) matchesEnrollment = false;
    } else if ((enrollmentYearFilter || enrollmentMonthFilter) && !s.enrolledAt) {
      matchesEnrollment = false;
    }

    return matchesSearch && matchesEnrollment;
  });

  const filteredProfessorsTable = course.professors.filter(
    (p) =>
      p.name.toLowerCase().includes(searchTermProfessors.toLowerCase()) ||
      p.email.toLowerCase().includes(searchTermProfessors.toLowerCase())
  );

  const totalPagesStudents = Math.max(
    1,
    Math.ceil(filteredStudentsTable.length / rowsPerPage)
  );
  const totalPagesProfessors = Math.max(
    1,
    Math.ceil(filteredProfessorsTable.length / rowsPerPage)
  );

  const getPaginated = <T,>(items: T[], page: number) => {
    const start = (page - 1) * rowsPerPage;
    return items.slice(start, start + rowsPerPage);
  };

  const paginatedStudents = getPaginated(filteredStudentsTable, pageStudents);
  const paginatedProfessors = getPaginated(
    filteredProfessorsTable,
    pageProfessors
  );

  /* ---------- Handlers ---------- */
  const handleEnroll = async () => {
    if (selectedNewStudents.length === 0) return;
    setLoading(true);
    const result = await enrollStudents(course.id, selectedNewStudents);
    setLoading(false);
    if (result.success) {
      notifications.success("Estudiantes asignados correctamente");
      if (result.data) {
        setStudents(result.data);
      }
      setEnrollDialogOpen(false);
      setSelectedNewStudents([]);
      setSearchTermEnroll("");
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

  /* ---------- Inline Editing ---------- */
  const handleStartEdit = () => {
    setEditForm({
      name: course.name,
      description: course.description ?? "",
      schoolYear: course.schoolYear,
      periodLabel: course.periodLabel,
      startDate: course.startDate,
      endDate: course.endDate,
      gameId: course.game?.id ?? null,
    });
    setValidationErrors(null);
    setIsEditing(true);
  };

  const handleCancelEdit = () => {
    setValidationErrors(null);
    setIsEditing(false);
  };

  const handleSaveEdit = async () => {
    setSaving(true);
    setValidationErrors(null);
    const result = await updateCourseInline(course.id, {
      name: editForm.name,
      description: editForm.description,
      schoolYear: editForm.schoolYear,
      periodLabel: editForm.periodLabel,
      startDate: editForm.startDate,
      endDate: editForm.endDate,
      gameId: editForm.gameId,
    });
    setSaving(false);
    if (result.success) {
      notifications.success("Curso actualizado correctamente");
      setIsEditing(false);
      router.refresh();
    } else if (result.errors) {
      setValidationErrors(result.errors);
      notifications.error(result.message || "Error de validación");
    } else {
      notifications.error(result.message || "Error al actualizar el curso");
    }
  };

  /* ---------- Render helpers ---------- */
  const renderEmptyRow = (message: string, icon: React.ReactNode, colSpan: number) => (
    <TableRow>
      <TableCell
        colSpan={colSpan}
        className="text-center py-12 text-slate-500 dark:text-slate-400"
      >
        <div className="flex flex-col items-center gap-2">
          {icon}
          <p>{message}</p>
        </div>
      </TableCell>
    </TableRow>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Grid background */}
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

      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 via-indigo-500 to-violet-600 text-white py-10 px-6 md:px-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="flex items-start justify-between mb-4">
            <Link
              href="/dashboard/courses"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-white/20 bg-white/10 text-white hover:bg-white/20 transition-all text-sm font-medium shadow-lg shadow-black/10"
            >
              <ArrowLeft className="h-4 w-4" />
              Volver a cursos
            </Link>
            {isEditing ? (
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleCancelEdit}
                  disabled={saving}
                  className="border-white/30 text-white hover:bg-white/10 hover:text-white"
                >
                  <X className="h-3.5 w-3.5 mr-1" />
                  Cancelar
                </Button>
                <Button
                  size="sm"
                  onClick={handleSaveEdit}
                  disabled={saving}
                  className="bg-white text-indigo-700 hover:bg-indigo-50"
                >
                  <Save className="h-3.5 w-3.5 mr-1" />
                  {saving ? "Guardando..." : "Guardar"}
                </Button>
              </div>
            ) : (
              <Button
                variant="outline"
                size="sm"
                onClick={handleStartEdit}
                className="border-white/30 text-white hover:bg-white/10 hover:text-white"
              >
                <Pencil className="h-3.5 w-3.5 mr-1" />
                Editar
              </Button>
            )}
          </div>

          {isEditing ? (
            <>
              <div className="mb-3">
                <Input
                  value={editForm.name}
                  onChange={(e) => setEditForm((f) => ({ ...f, name: e.target.value }))}
                  className="text-3xl font-bold tracking-tight h-auto py-1 px-3 bg-white/10 border-white/20 text-white placeholder-indigo-200"
                  placeholder="Nombre del curso"
                />
                {validationErrors?.name && (
                  <p className="text-red-200 text-sm mt-1">{validationErrors.name[0]}</p>
                )}
              </div>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 shrink-0" />
                  <Input
                    value={editForm.schoolYear}
                    onChange={(e) => setEditForm((f) => ({ ...f, schoolYear: e.target.value }))}
                    className="h-8 w-28 bg-white/10 border-white/20 text-white placeholder-indigo-200 text-sm"
                    placeholder="2025-2026"
                  />
                  {validationErrors?.schoolYear && (
                    <p className="text-red-200 text-sm">{validationErrors.schoolYear[0]}</p>
                  )}
                  <Select
                    value={editForm.periodLabel}
                    onValueChange={(v) => setEditForm((f) => ({ ...f, periodLabel: v }))}
                  >
                    <SelectTrigger className="h-8 w-44 bg-white/10 border-white/20 text-white text-sm">
                      <SelectValue placeholder="Período" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Primer Semestre">Primer Semestre</SelectItem>
                      <SelectItem value="Segundo Semestre">Segundo Semestre</SelectItem>
                      <SelectItem value="Primer Trimestre">Primer Trimestre</SelectItem>
                      <SelectItem value="Segundo Trimestre">Segundo Trimestre</SelectItem>
                      <SelectItem value="Tercer Trimestre">Tercer Trimestre</SelectItem>
                      <SelectItem value="Verano Intensivo">Verano Intensivo</SelectItem>
                    </SelectContent>
                  </Select>
                  {validationErrors?.periodLabel && (
                    <p className="text-red-200 text-sm">{validationErrors.periodLabel[0]}</p>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <BookOpen className="h-4 w-4 shrink-0" />
                  <Input
                    type="date"
                    value={editForm.startDate}
                    onChange={(e) => setEditForm((f) => ({ ...f, startDate: e.target.value }))}
                    className="h-8 w-36 bg-white/10 border-white/20 text-white text-sm [color-scheme:dark]"
                  />
                  <span className="text-indigo-200">→</span>
                  <Input
                    type="date"
                    value={editForm.endDate}
                    onChange={(e) => setEditForm((f) => ({ ...f, endDate: e.target.value }))}
                    className="h-8 w-36 bg-white/10 border-white/20 text-white text-sm [color-scheme:dark]"
                  />
                  {validationErrors?.endDate && (
                    <p className="text-red-200 text-sm">{validationErrors.endDate[0]}</p>
                  )}
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-3xl font-bold tracking-tight">{course.name}</h1>
                <Badge
                  variant={course.isActive ? "default" : "secondary"}
                  className={cn(
                    "text-xs font-semibold px-3 py-1",
                    course.isActive
                      ? "bg-emerald-500/20 text-emerald-200 border border-emerald-400/30"
                      : "bg-slate-500/20 text-slate-300 border border-slate-400/30"
                  )}
                >
                  {course.isActive ? "Activo" : "Inactivo"}
                </Badge>
              </div>
              <div className="flex flex-wrap gap-4 text-indigo-100">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  <span>
                    {course.schoolYear} - {course.periodLabel}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <BookOpen className="h-4 w-4" />
              <span>
                {safeDateLong(course.startDate)} → {safeDateLong(course.endDate)}
              </span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Main */}
      <div className="max-w-7xl mx-auto px-6 md:px-12 py-8 relative z-10 space-y-8">
        {(isEditing || course.description) && (
          <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-700 shadow-lg p-6">
            <h2 className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
              Descripción
            </h2>
            {isEditing ? (
              <>
                <textarea
                  value={editForm.description}
                  onChange={(e) => setEditForm((f) => ({ ...f, description: e.target.value }))}
                  className="w-full min-h-[80px] rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-700 dark:text-slate-300 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500"
                  placeholder="Agregar descripción del curso..."
                />
                {validationErrors?.description && (
                  <p className="text-red-500 text-sm mt-1">{validationErrors.description[0]}</p>
                )}
              </>
            ) : (
              <p className="text-slate-700 dark:text-slate-300">{course.description}</p>
            )}
          </div>
        )}

        {/* ─── Juego Asignado ─── */}
        <section>
          <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-md rounded-xl border border-slate-200 dark:border-slate-700 shadow-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/50">
                <Gamepad2 className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-200">
                Juego Asignado
              </h2>
            </div>

            {isEditing ? (
              <div className="space-y-3">
                <Select
                  value={editForm.gameId ?? "none"}
                  onValueChange={(v) =>
                    setEditForm((f) => ({
                      ...f,
                      gameId: v === "none" ? null : v,
                    }))
                  }
                >
                  <SelectTrigger className="w-full bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700">
                    <Gamepad2 className="h-3.5 w-3.5 mr-2 shrink-0 text-muted-foreground" />
                    <SelectValue placeholder="Seleccionar juego..." />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">
                      <span className="text-muted-foreground">Sin juego</span>
                    </SelectItem>
                    {availableGames.map((game) => (
                      <SelectItem key={game.id} value={game.id}>
                        {game.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {validationErrors?.gameId && (
                  <p className="text-red-500 text-sm">
                    {validationErrors.gameId[0]}
                  </p>
                )}
              </div>
            ) : course.game ? (
              <div className="space-y-3">
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-slate-100">
                    {course.game.title}
                  </p>
                  {course.game.description && (
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                      {course.game.description}
                    </p>
                  )}
                </div>
                <div className="flex flex-wrap gap-4 text-sm text-slate-500 dark:text-slate-400">
                  {course.game.subject && (
                    <div className="flex items-center gap-1.5">
                      <BookOpen className="h-3.5 w-3.5" />
                      <span>{course.game.subject}</span>
                    </div>
                  )}
                  {course.game.creator && (
                    <div className="flex items-center gap-1.5">
                      <Users className="h-3.5 w-3.5" />
                      <span>Creado por: {course.game.creator}</span>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center py-6 text-slate-400 dark:text-slate-500">
                <Gamepad2 className="h-10 w-10 mb-2 opacity-50" />
                <p className="text-sm">Este curso no tiene un juego asignado</p>
                <p className="text-xs mt-1">
                  Asigná un juego desde la edición del curso
                </p>
              </div>
            )}
          </div>
        </section>

        {/* ─── Estudiantes ─── */}
        <section>
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center gap-3">
              <Users className="h-5 w-5 text-indigo-500" />
              <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200">
                Estudiantes Inscritos
              </h2>
              <Badge variant="secondary" className="ml-2">
                {students.length}
              </Badge>
            </div>
            <Dialog open={enrollDialogOpen} onOpenChange={setEnrollDialogOpen}>
              <DialogTrigger asChild>
                <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">
                  <UserPlus className="h-4 w-4 mr-2" />
                  Asignar Estudiantes
                </Button>
              </DialogTrigger>
            </Dialog>
          </div>

          {/* Filtro estudiantes */}
          <div className="flex flex-col sm:flex-row gap-2 mb-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar en la tabla de estudiantes..."
                value={searchTermStudents}
                onChange={(e) => {
                  setSearchTermStudents(e.target.value);
                  setPageStudents(1);
                }}
                className="pl-10 pr-10 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700"
              />
              {searchTermStudents && (
                <button
                  onClick={() => {
                    setSearchTermStudents("");
                    setPageStudents(1);
                  }}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>

            {enrollmentYears.length > 0 && (
              <div className="flex gap-2">
                <Select
                  value={enrollmentYearFilter || "all"}
                  onValueChange={(v) => {
                    setEnrollmentYearFilter(v === "all" ? "" : v);
                    setPageStudents(1);
                  }}
                >
                  <SelectTrigger className="w-[120px] bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700">
                    <Calendar className="h-3.5 w-3.5 mr-1 shrink-0" />
                    <SelectValue placeholder="Año" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todos los años</SelectItem>
                    {enrollmentYears.map((y) => (
                      <SelectItem key={y} value={y}>
                        {y}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Select
                  value={enrollmentMonthFilter || "all"}
                  onValueChange={(v) => {
                    setEnrollmentMonthFilter(v === "all" ? "" : v);
                    setPageStudents(1);
                  }}
                >
                  <SelectTrigger className="w-[140px] bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700">
                    <Calendar className="h-3.5 w-3.5 mr-1 shrink-0" />
                    <SelectValue placeholder="Mes" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todos los meses</SelectItem>
                    {enrollmentMonths.map((m) => (
                      <SelectItem key={m} value={m.toString()}>
                        {MONTHS[m]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          </div>

          <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-md shadow-xl overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-700">
                  <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Nombre</TableHead>
                  <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Email</TableHead>
                  <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Fecha de inscripción</TableHead>
                  <TableHead className="font-semibold text-slate-700 dark:text-slate-300 text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {paginatedStudents.length > 0 ? (
                  paginatedStudents.map((student) => (
                    <TableRow
                      key={student.studentId}
                      className="hover:bg-indigo-50/50 dark:hover:bg-indigo-950/20 transition-all border-b border-slate-100 dark:border-slate-700/50"
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
                        {student.enrolledAt
                          ? new Date(student.enrolledAt).toLocaleDateString("es-ES", {
                              year: "numeric",
                              month: "long",
                              day: "numeric",
                            })
                          : "—"}
                      </TableCell>
                      <TableCell className="text-right">
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
                  renderEmptyRow(
                    "No hay estudiantes inscritos en este curso",
                    <Users className="h-8 w-8 text-slate-300 dark:text-slate-600" />,
                    4
                  )
                )}
              </TableBody>
            </Table>
          </div>

          {totalPagesStudents > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between mt-6 gap-4">
              <div className="text-sm text-slate-600 dark:text-slate-400 bg-white/60 dark:bg-slate-800/60 px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700">
                Mostrando{" "}
                <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                  {(pageStudents - 1) * rowsPerPage + 1}
                </span>
                -
                <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                  {Math.min(pageStudents * rowsPerPage, filteredStudentsTable.length)}
                </span>{" "}
                de{" "}
                <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                  {filteredStudentsTable.length}
                </span>{" "}
                estudiantes
              </div>
              <div className="flex items-center gap-1 bg-white/60 dark:bg-slate-800/60 px-2 py-1 rounded-lg border border-slate-200 dark:border-slate-700">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPageStudents((p) => Math.max(1, p - 1))}
                  disabled={pageStudents === 1}
                  className="border-slate-200 dark:border-slate-700 h-8 w-8 p-0"
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <div className="flex items-center gap-1 px-2">
                  {Array.from({ length: totalPagesStudents }, (_, i) => i + 1).map(
                    (page) => (
                      <Button
                        key={page}
                        variant={pageStudents === page ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setPageStudents(page)}
                        className={
                          pageStudents === page
                            ? "bg-indigo-600 hover:bg-indigo-700 text-white h-8 w-8 p-0"
                            : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 h-8 w-8 p-0"
                        }
                      >
                        {page}
                      </Button>
                    )
                  )}
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() =>
                    setPageStudents((p) => Math.min(totalPagesStudents, p + 1))
                  }
                  disabled={pageStudents === totalPagesStudents}
                  className="border-slate-200 dark:border-slate-700 h-8 w-8 p-0"
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </section>

        {/* ─── Profesores ─── */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <GraduationCap className="h-5 w-5 text-violet-500" />
            <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200">
              Profesores Asignados
            </h2>
            <Badge variant="secondary" className="ml-2">
              {course.professors.length}
            </Badge>
          </div>

          {/* Filtro profesores */}
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar en la tabla de profesores..."
              value={searchTermProfessors}
              onChange={(e) => {
                setSearchTermProfessors(e.target.value);
                setPageProfessors(1);
              }}
              className="pl-10 pr-10 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700"
            />
            {searchTermProfessors && (
              <button
                onClick={() => {
                  setSearchTermProfessors("");
                  setPageProfessors(1);
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>

          <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-md shadow-xl overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-700">
                  <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Nombre</TableHead>
                  <TableHead className="font-semibold text-slate-700 dark:text-slate-300">Email</TableHead>
                  <TableHead className="font-semibold text-slate-700 dark:text-slate-300 text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {paginatedProfessors.length > 0 ? (
                  paginatedProfessors.map((prof) => (
                    <TableRow
                      key={prof.professorId}
                      className="hover:bg-indigo-50/50 dark:hover:bg-indigo-950/20 transition-all border-b border-slate-100 dark:border-slate-700/50"
                    >
                      <TableCell className="font-medium text-slate-900 dark:text-slate-100">
                        {prof.name}
                      </TableCell>
                      <TableCell className="text-slate-600 dark:text-slate-400">
                        {prof.email}
                      </TableCell>
                      <TableCell className="text-right text-muted-foreground text-sm italic">
                        {/* TODO: Acciones de profesores (ej. desasignar) pendientes de backend */}
                        Sin acciones
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  renderEmptyRow(
                    "No hay profesores asignados a este curso",
                    <GraduationCap className="h-8 w-8 text-slate-300 dark:text-slate-600" />,
                    3
                  )
                )}
              </TableBody>
            </Table>
          </div>

          {totalPagesProfessors > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between mt-6 gap-4">
              <div className="text-sm text-slate-600 dark:text-slate-400 bg-white/60 dark:bg-slate-800/60 px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-700">
                Mostrando{" "}
                <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                  {(pageProfessors - 1) * rowsPerPage + 1}
                </span>
                -
                <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                  {Math.min(pageProfessors * rowsPerPage, filteredProfessorsTable.length)}
                </span>{" "}
                de{" "}
                <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                  {filteredProfessorsTable.length}
                </span>{" "}
                profesores
              </div>
              <div className="flex items-center gap-1 bg-white/60 dark:bg-slate-800/60 px-2 py-1 rounded-lg border border-slate-200 dark:border-slate-700">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPageProfessors((p) => Math.max(1, p - 1))}
                  disabled={pageProfessors === 1}
                  className="border-slate-200 dark:border-slate-700 h-8 w-8 p-0"
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <div className="flex items-center gap-1 px-2">
                  {Array.from({ length: totalPagesProfessors }, (_, i) => i + 1).map(
                    (page) => (
                      <Button
                        key={page}
                        variant={pageProfessors === page ? "default" : "ghost"}
                        size="sm"
                        onClick={() => setPageProfessors(page)}
                        className={
                          pageProfessors === page
                            ? "bg-indigo-600 hover:bg-indigo-700 text-white h-8 w-8 p-0"
                            : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 h-8 w-8 p-0"
                        }
                      >
                        {page}
                      </Button>
                    )
                  )}
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() =>
                    setPageProfessors((p) => Math.min(totalPagesProfessors, p + 1))
                  }
                  disabled={pageProfessors === totalPagesProfessors}
                  className="border-slate-200 dark:border-slate-700 h-8 w-8 p-0"
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </section>
      </div>

      {/* ─── Enrollment Dialog ─── */}
      <Dialog open={enrollDialogOpen} onOpenChange={setEnrollDialogOpen}>
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
              value={searchTermEnroll}
              onChange={(e) => setSearchTermEnroll(e.target.value)}
              className="pl-10 pr-10"
            />
            {searchTermEnroll && (
              <button
                onClick={() => setSearchTermEnroll("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <ScrollArea className="h-64">
            <div className="space-y-1">
              {filteredAvailableForEnroll.length > 0 ? (
                filteredAvailableForEnroll.map((student) => (
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
                  {searchTermEnroll
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
                setSearchTermEnroll("");
              }}
            >
              Cancelar
            </Button>
            <Button
              onClick={handleEnroll}
              disabled={selectedNewStudents.length === 0 || loading}
              className="bg-indigo-600 hover:bg-indigo-700 text-white"
            >
              {loading
                ? "Asignando..."
                : `Asignar (${selectedNewStudents.length})`}
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* ─── Unenroll Confirmation ─── */}
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
