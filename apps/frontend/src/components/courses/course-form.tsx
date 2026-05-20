"use client";

import { useActionState, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import UserMultiSelect from "@/components/courses/user-multi-select";
import { createCourse, updateCourse } from "@/app/dashboard/courses/actions";
import { toast } from "sonner";
import { Loader2, Calendar, X } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { CourseDetail } from "@/types/course.interface";
import type { ActionState } from "@/lib/actions";
import type { UserResponse } from "@/api/types";

interface GameOption {
  id: string;
  title: string;
}

interface CourseFormProps {
  course?: CourseDetail;
  students: UserResponse[];
  professors: UserResponse[];
  games?: GameOption[];
  onSuccess?: () => void;
  onCancel?: () => void;
}

export default function CourseForm({
  course,
  students,
  professors,
  onSuccess,
  onCancel,
}: CourseFormProps) {
  const action = course
    ? (prevState: ActionState | null, formData: FormData) =>
        updateCourse(course.id, prevState, formData)
    : createCourse;

  const [state, formAction, isPending] = useActionState(action, null);

  // Local state to preserve form values after validation errors
  const [name, setName] = useState(course?.name ?? "");
  const [schoolYear, setSchoolYear] = useState(course?.schoolYear ?? "");
  const [description, setDescription] = useState(course?.description ?? "");
  const [periodLabel, setPeriodLabel] = useState(course?.periodLabel ?? "");
  const [startDate, setStartDate] = useState(course?.startDate ?? "");
  const [endDate, setEndDate] = useState(course?.endDate ?? "");
  const [selectedGameId, setSelectedGameId] = useState<string | null>(
    course?.gameId ?? null
  );

  // Update local state when course prop changes (for edit forms)
  useEffect(() => {
    if (course) {
      setName(course.name ?? "");
      setSchoolYear(course.schoolYear ?? "");
      setDescription(course.description ?? "");
      setPeriodLabel(course.periodLabel ?? "");
      setStartDate(course.startDate ?? "");
      setEndDate(course.endDate ?? "");
    }
  }, [course]);

  const [selectedStudentIds, setSelectedStudentIds] = useState<string[]>(
    course?.students?.map((s) => s.studentId) ?? []
  );
  const [selectedProfessorIds, setSelectedProfessorIds] = useState<string[]>(
    course?.professors?.map((p) => p.professorId) ?? []
  );

  const [filterEnrollYear, setFilterEnrollYear] = useState("");
  const [filterEnrollMonth, setFilterEnrollMonth] = useState("");

  useEffect(() => {
    if (state?.success) {
      toast.success(state.message || (course ? "Curso actualizado correctamente" : "Curso creado correctamente"));
      onSuccess?.();
    } else if (state?.success === false && state?.message) {
      toast.error(state.message);
    }
  }, [state, onSuccess, course]);

  const studentOptions = students.map((s) => ({
    id: s.id,
    label: `${s.name} ${s.lastname || ""}`.trim(),
    subtitle: s.email,
  }));

  const professorOptions = professors.map((p) => ({
    id: p.id,
    label: `${p.name} ${p.lastname || ""}`.trim(),
    subtitle: p.email,
  }));

  const studentCreatedAt = new Map(
    students.filter((s) => s.created_at).map((s) => [s.id, s.created_at!])
  );

  const enrollmentYears = [...new Set(
    students
      .filter((s) => s.created_at)
      .map((s) => new Date(s.created_at!).getFullYear().toString())
  )].sort((a, b) => b.localeCompare(a));

  const enrollmentMonths = [...new Set(
    students
      .filter((s) => s.created_at)
      .map((s) => new Date(s.created_at!).getMonth())
  )].sort((a, b) => a - b);

  const enrollmentFilterFn = (opt: { id: string; label: string; subtitle?: string }) => {
    const createdAt = studentCreatedAt.get(opt.id);
    if (!createdAt) return !filterEnrollYear && !filterEnrollMonth;
    const d = new Date(createdAt);
    if (filterEnrollYear && d.getFullYear().toString() !== filterEnrollYear) return false;
    if (filterEnrollMonth && d.getMonth().toString() !== filterEnrollMonth) return false;
    return true;
  };

  return (
    <form action={formAction} className="space-y-4 py-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="name">Nombre del curso</Label>
          <Input
            id="name"
            name="name"
            placeholder="Matemáticas I"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={isPending}
          />
          {state?.errors?.name && (
            <p className="text-xs text-destructive">{state.errors.name[0]}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="schoolYear">Año Escolar</Label>
          <Input
            id="schoolYear"
            name="schoolYear"
            placeholder="2025-2026"
            required
            value={schoolYear}
            onChange={(e) => setSchoolYear(e.target.value)}
            disabled={isPending}
          />
          {state?.errors?.schoolYear && (
            <p className="text-xs text-destructive">{state.errors.schoolYear[0]}</p>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Descripción</Label>
        <Textarea
          id="description"
          name="description"
          placeholder="Descripción del curso..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isPending}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="periodLabel">Período</Label>
        <select
          id="periodLabel"
          name="periodLabel"
          required
          value={periodLabel}
          onChange={(e) => setPeriodLabel(e.target.value)}
          disabled={isPending}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <option value="" disabled>Seleccionar período</option>
          {PERIODS.map((period) => (
            <option key={period} value={period}>
              {period}
            </option>
          ))}
        </select>
        {state?.errors?.periodLabel && (
          <p className="text-xs text-destructive">{state.errors.periodLabel[0]}</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="startDate">Fecha de inicio</Label>
          <Input
            id="startDate"
            name="startDate"
            type="date"
            required
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            disabled={isPending}
          />
          {state?.errors?.startDate && (
            <p className="text-xs text-destructive">{state.errors.startDate[0]}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="endDate">Fecha de fin</Label>
          <Input
            id="endDate"
            name="endDate"
            type="date"
            required
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            disabled={isPending}
          />
          {state?.errors?.endDate && (
            <p className="text-xs text-destructive">{state.errors.endDate[0]}</p>
          )}
        </div>
      </div>

      <input
        type="hidden"
        name="studentIds"
        value={JSON.stringify(selectedStudentIds)}
      />
      <input
        type="hidden"
        name="professorIds"
        value={JSON.stringify(selectedProfessorIds)}
      />
      <input
        type="hidden"
        name="gameId"
        value={selectedGameId ?? ""}
      />

      {enrollmentYears.length > 0 && (
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Calendar className="h-4 w-4 shrink-0" />
          <span>Período de inscripción:</span>
          <Select
            value={filterEnrollYear || "all"}
            onValueChange={(v) => setFilterEnrollYear(v === "all" ? "" : v)}
          >
            <SelectTrigger className="h-8 w-[110px]">
              <SelectValue placeholder="Año" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos los años</SelectItem>
              {enrollmentYears.map((y) => (
                <SelectItem key={y} value={y}>{y}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select
            value={filterEnrollMonth || "all"}
            onValueChange={(v) => setFilterEnrollMonth(v === "all" ? "" : v)}
          >
            <SelectTrigger className="h-8 w-[130px]">
              <SelectValue placeholder="Mes" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos los meses</SelectItem>
              {enrollmentMonths.map((m) => (
                <SelectItem key={m} value={m.toString()}>{MONTHS[m]}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          {(filterEnrollYear || filterEnrollMonth) && (
            <button
              onClick={() => { setFilterEnrollYear(""); setFilterEnrollMonth(""); }}
              className="text-muted-foreground hover:text-foreground transition-colors"
              title="Limpiar filtro"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
      )}

      <UserMultiSelect
        label="Estudiantes"
        options={studentOptions}
        selected={selectedStudentIds}
        onChange={setSelectedStudentIds}
        placeholder="Seleccionar estudiantes..."
        searchPlaceholder="Buscar estudiantes..."
        emptyMessage="No se encontraron estudiantes"
        filterFn={enrollmentFilterFn}
      />

      {/* Profesores: mensaje fijo en creación, multi-select en edición */}
      {!course ? (
        <div className="space-y-2">
          <Label className="text-sm text-slate-500">Profesor titular</Label>
          <div className="flex items-center gap-2 rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2.5 bg-slate-50 dark:bg-slate-900/40">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="h-4 w-4 text-indigo-500">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            <span className="text-sm text-slate-700 dark:text-slate-300">Tú ya estás asignado como profesor titular</span>
          </div>
        </div>
      ) : (
        <UserMultiSelect
          label="Profesores adicionales"
          options={professorOptions}
          selected={selectedProfessorIds}
          onChange={setSelectedProfessorIds}
          placeholder="Agregar profesores adicionales..."
          searchPlaceholder="Buscar profesores..."
          emptyMessage="No se encontraron profesores"
        />
      )}

      {/* Select de juegos */}
      {games && games.length > 0 && (
        <div className="space-y-2">
          <Label htmlFor="gameId">Juego asociado</Label>
          <Select
            value={selectedGameId ?? "none"}
            onValueChange={(v) => setSelectedGameId(v === "none" ? null : v)}
            disabled={isPending}
          >
            <SelectTrigger id="gameId" className="w-full">
              <SelectValue placeholder="Seleccionar juego (opcional)" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="none">Sin juego</SelectItem>
              {games.map((g) => (
                <SelectItem key={g.id} value={g.id}>
                  {g.title}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      )}

      {state?.errors?._form && (
        <p className="text-sm text-destructive font-medium text-center">
          {state.errors._form[0]}
        </p>
      )}

      <div className="flex justify-end space-x-2 pt-4">
        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isPending}
          >
            Cancelar
          </Button>
        )}
        <Button type="submit" disabled={isPending}>
          {isPending ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              {course ? "Actualizando..." : "Creando..."}
            </>
          ) : course ? (
            "Actualizar Curso"
          ) : (
            "Crear Curso"
          )}
        </Button>
      </div>
    </form>
  );
}
