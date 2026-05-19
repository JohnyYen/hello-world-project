"use client";

import { useActionState, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import UserMultiSelect from "@/components/courses/user-multi-select";
import { createCourse, updateCourse } from "@/app/dashboard/courses/actions";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";
import type { CourseDetail } from "@/types/course.interface";
import type { ActionState } from "@/lib/actions";
import type { UserResponse } from "@/api/types";

const PERIODS = [
  "Semestre 1",
  "Semestre 2",
  "Anual",
  "Trimestre 1",
  "Trimestre 2",
  "Trimestre 3",
];

interface CourseFormProps {
  course?: CourseDetail;
  students: UserResponse[];
  professors: UserResponse[];
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

  const [selectedStudentIds, setSelectedStudentIds] = useState<string[]>(
    course?.students?.map((s) => s.studentId) ?? []
  );
  const [selectedProfessorIds, setSelectedProfessorIds] = useState<string[]>(
    course?.professors?.map((p) => p.professorId) ?? []
  );

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
            defaultValue={course?.name}
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
            defaultValue={course?.schoolYear}
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
          defaultValue={course?.description ?? ""}
          disabled={isPending}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="periodLabel">Período</Label>
        <select
          id="periodLabel"
          name="periodLabel"
          required
          defaultValue={course?.periodLabel ?? ""}
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
            defaultValue={course?.startDate}
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
            defaultValue={course?.endDate}
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

      <UserMultiSelect
        label="Estudiantes"
        options={studentOptions}
        selected={selectedStudentIds}
        onChange={setSelectedStudentIds}
        placeholder="Seleccionar estudiantes..."
        searchPlaceholder="Buscar estudiantes..."
        emptyMessage="No se encontraron estudiantes"
      />

      <UserMultiSelect
        label="Profesores"
        options={professorOptions}
        selected={selectedProfessorIds}
        onChange={setSelectedProfessorIds}
        placeholder="Seleccionar profesores..."
        searchPlaceholder="Buscar profesores..."
        emptyMessage="No se encontraron profesores"
      />

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
