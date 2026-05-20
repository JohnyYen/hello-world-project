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

  console.error(`[CursoDetailPage] token presente: ${!!token}, id curso: ${id}`);

  if (!token) {
    return <div className="p-6 text-center text-muted-foreground">No autenticado</div>;
  }

  let course;
  try {
    console.error(`[CursoDetailPage] Intentando fetch detalle curso ${id}...`);
    course = await coursesApi.getById(id, token);
    console.error(`[CursoDetailPage] Curso cargado:`, !!course, course?.name);
  } catch (err: any) {
    const status = err?.status ?? err?.response?.status ?? "desconocido";
    const detail = err?.detail ?? err?.message ?? "Sin detalles";
    const url = `${process.env.NEXT_PUBLIC_API_URL ?? "???"}/api/v1/courses/${id}`;
    console.error("[CursoDetailPage] ❌ Error al cargar el curso:", {
      id,
      url,
      status,
      detail,
    });
    if (status === 404 || err?.status === 404) {
      notFound();
    }
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-slate-800 dark:text-slate-200 mb-4">
            Error al cargar el curso
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mb-2">
            Código: {status}
          </p>
          <p className="text-slate-600 dark:text-slate-400 mb-6 max-w-md">
            {detail}
          </p>
          <p className="text-xs text-slate-400 mb-6 font-mono break-all">
            GET {url}
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
  } catch {}

  return <CourseDetailView course={course} allStudents={allStudents} />;
}
