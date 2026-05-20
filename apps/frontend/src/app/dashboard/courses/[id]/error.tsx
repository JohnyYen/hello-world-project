"use client";

import { Button } from "@/components/ui/button";
import { BookOpen } from "lucide-react";

export default function CursoDetailError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      <div className="text-center max-w-md px-6">
        <BookOpen className="h-16 w-16 text-red-400 mx-auto mb-4" />
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-200 mb-2">
          Error al cargar el curso
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mb-6">
          {error.message || "Ocurrió un error al cargar el detalle del curso."}
        </p>
        <div className="flex gap-3 justify-center">
          <Button onClick={reset} variant="default">
            Reintentar
          </Button>
          <Button
            onClick={() => (window.location.href = "/dashboard/courses")}
            variant="outline"
          >
            Volver a cursos
          </Button>
        </div>
      </div>
    </div>
  );
}
