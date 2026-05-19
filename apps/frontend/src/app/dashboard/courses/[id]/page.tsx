import { notFound } from "next/navigation";
import Link from "next/link";
import { coursesApi } from "@/api/client";
import { cookies } from "next/headers";
import CourseDetailView from "@/components/courses/course-detail";
import type { UserResponse } from "@/api/types";

export const dynamic = "force-dynamic";

export default async function CursoDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const token = (await cookies()).get("auth_token")?.value;
  if (!token) return <div className="p-6 text-center text-muted-foreground">No autenticado</div>;

  let course;
  try {
    course = await coursesApi.getById(id, token);
  } catch {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-slate-800 dark:text-slate-200 mb-4">
            Curso no encontrado
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mb-6">
            El curso que buscas no existe o ha sido eliminado.
          </p>
          <Link
            href="/dashboard/courses"
            className="inline-flex items-center gap-2 text-indigo-600 hover:text-indigo-700 transition-colors font-medium"
          >
            ← Volver a cursos
          </Link>
        </div>
      </div>
    );
  }

  let allStudents: UserResponse[] = [];
  try {
    allStudents = await coursesApi.listByRole("student", token);
  } catch {
    allStudents = [];
  }

  return <CourseDetailView course={course} allStudents={allStudents} />;
}
