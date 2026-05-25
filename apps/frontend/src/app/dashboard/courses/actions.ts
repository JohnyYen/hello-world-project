"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { coursesApi } from "@/api/client";
import type { ActionState } from "@/lib/actions";

const courseSchema = z.object({
  name: z.string().min(1, "El nombre es requerido").max(100, "Máximo 100 caracteres"),
  description: z.string().optional(),
  schoolYear: z
    .string()
    .regex(/^\d{4}-\d{4}$/, "Formato inválido. Use YYYY-YYYY"),
  periodLabel: z.string().min(1, "El período es requerido"),
  startDate: z.string().min(1, "La fecha de inicio es requerida"),
  endDate: z.string().min(1, "La fecha de fin es requerida"),
  gameId: z.string().uuid().nullable().optional(),
  studentIds: z.string().transform((val) => {
    try {
      return JSON.parse(val) as string[];
    } catch {
      return [] as string[];
    }
  }),
  professorIds: z.string().transform((val) => {
    try {
      return JSON.parse(val) as string[];
    } catch {
      return [] as string[];
    }
  }),
}).refine(
  (data) => !data.startDate || !data.endDate || new Date(data.endDate) > new Date(data.startDate),
  {
    message: "La fecha de fin debe ser posterior a la fecha de inicio",
    path: ["endDate"],
  }
);

async function getAuthToken(): Promise<string> {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;
  if (!token) throw new Error("No autenticado");
  return token;
}

export async function createCourse(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validated = courseSchema.safeParse({
      name: formData.get("name"),
      description: formData.get("description"),
      schoolYear: formData.get("schoolYear"),
      periodLabel: formData.get("periodLabel"),
      startDate: formData.get("startDate"),
      endDate: formData.get("endDate"),
      studentIds: formData.get("studentIds") ?? "[]",
      professorIds: formData.get("professorIds") ?? "[]",
    });

    if (!validated.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validated.error.flatten().fieldErrors,
      };
    }

    const token = await getAuthToken();
    const { studentIds, professorIds, gameId, ...fields } = validated.data;

    await coursesApi.create(
      {
        ...fields,
        description: fields.description || undefined,
        gameId: gameId ?? null,
        studentIds,
        professorIds,
      },
      token
    );

    revalidatePath("/dashboard/courses");

    redirect("/dashboard/courses");
  } catch (error) {
    if (error instanceof Error && error.message.includes("NEXT_REDIRECT")) {
      throw error;
    }
    const message = error instanceof Error ? error.message : "Error al actualizar el curso";
    return { success: false, message, errors: { _form: [message] } };
  }
}

export async function updateCourse(
  courseId: string,
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validated = courseSchema.safeParse({
      name: formData.get("name"),
      description: formData.get("description"),
      schoolYear: formData.get("schoolYear"),
      periodLabel: formData.get("periodLabel"),
      startDate: formData.get("startDate"),
      endDate: formData.get("endDate"),
      studentIds: formData.get("studentIds") ?? "[]",
      professorIds: formData.get("professorIds") ?? "[]",
    });

    if (!validated.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validated.error.flatten().fieldErrors,
      };
    }

    const token = await getAuthToken();
    const { studentIds, professorIds, gameId, ...fields } = validated.data;

    await coursesApi.update(
      courseId,
      {
        ...fields,
        description: fields.description || undefined,
        gameId: gameId ?? null,
        studentIds,
        professorIds,
      },
      token
    );

    revalidatePath("/dashboard/courses");
    redirect("/dashboard/courses");
  } catch (error) {
    if (error instanceof Error && error.message.includes("NEXT_REDIRECT")) {
      throw error;
    }
    const message = error instanceof Error ? error.message : "Error al actualizar el curso";
    return { success: false, message, errors: { _form: [message] } };
  }
}

export async function deleteCourse(courseId: string) {
  try {
    const token = await getAuthToken();
    await coursesApi.delete(courseId, token);
    revalidatePath("/dashboard/courses");
    return { success: true, message: "Curso eliminado correctamente" };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Error al eliminar el curso";
    return { success: false, message };
  }
}

export async function enrollStudents(
  courseId: string,
  studentIds: string[]
): Promise<{ success: boolean; message: string; data?: import("@/types/course.interface").StudentEnrollment[] }> {
  try {
    const token = await getAuthToken();
    const data = await coursesApi.enrollStudents(courseId, { studentIds }, token);
    revalidatePath(`/dashboard/courses/${courseId}`);
    return { success: true, message: "Estudiantes asignados correctamente", data };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Error al asignar estudiantes";
    return { success: false, message };
  }
}

export async function unenrollStudent(
  courseId: string,
  studentId: string
): Promise<{ success: boolean; message: string }> {
  try {
    const token = await getAuthToken();
    await coursesApi.unenrollStudent(courseId, studentId, token);
    revalidatePath(`/dashboard/courses/${courseId}`);
    return { success: true, message: "Estudiante desasignado correctamente" };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Error al desasignar estudiante";
    return { success: false, message };
  }
}

const courseInlineSchema = z.object({
  name: z.string().min(1, "El nombre es requerido").max(100, "Máximo 100 caracteres"),
  description: z.string().optional(),
  schoolYear: z.string().regex(/^\d{4}-\d{4}$/, "Formato inválido. Use YYYY-YYYY"),
  periodLabel: z.string().min(1, "El período es requerido"),
  startDate: z.string().min(1, "La fecha de inicio es requerida"),
  endDate: z.string().min(1, "La fecha de fin es requerida"),
  gameId: z.string().uuid().nullable().optional(),
}).refine(
  (data) => !data.startDate || !data.endDate || new Date(data.endDate) > new Date(data.startDate),
  { message: "La fecha de fin debe ser posterior a la fecha de inicio", path: ["endDate"] }
);

export async function updateCourseInline(
  courseId: string,
  fields: {
    name: string;
    description?: string;
    schoolYear: string;
    periodLabel: string;
    startDate: string;
    endDate: string;
    gameId?: string | null;
  }
): Promise<{ success: boolean; message: string; errors?: Record<string, string[]> }> {
  try {
    const validated = courseInlineSchema.safeParse(fields);

    if (!validated.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validated.error.flatten().fieldErrors,
      };
    }

    const token = await getAuthToken();
    const { gameId, ...rest } = validated.data;
    await coursesApi.update(courseId, { ...rest, gameId: gameId ?? null }, token);
    revalidatePath(`/dashboard/courses/${courseId}`);

    return { success: true, message: "Curso actualizado correctamente" };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Error al actualizar el curso";
    return { success: false, message };
  }
}

export async function getUsersForForm(role: "student" | "professor") {
  try {
    const token = await getAuthToken();
    return coursesApi.listByRole(role, token);
  } catch {
    return [];
  }
}

export async function getAvailableGamesAction(): Promise<{ id: string; title: string }[]> {
  try {
    const token = await getAuthToken();
    const games = await coursesApi.listGames(token);
    return games.map((g) => ({ id: g.id, title: g.title }));
  } catch {
    return [];
  }
}

export async function getCourseDetailAction(courseId: string) {
  try {
    const token = await getAuthToken();
    return await coursesApi.getById(courseId, token);
  } catch {
    return null;
  }
}
