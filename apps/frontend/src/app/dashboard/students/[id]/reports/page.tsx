import { Button } from "@/components/ui/button";
import { ChevronLeft } from "lucide-react";
import Link from "next/link";

export default function StudentReportPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto py-10">
      <div className="mb-6">
        <Link href={`/dashboard/students/${params.id}`}>
          <Button variant="outline" className="mb-4">
            <ChevronLeft className="h-4 w-4 mr-2" />
            Volver al perfil
          </Button>
        </Link>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Reporte de Progreso</h1>
            <p className="text-muted-foreground">Reportes detallados del estudiante</p>
          </div>
        </div>
      </div>

      <div className="text-center py-20 text-muted-foreground">
        Los reportes detallados se implementarán próximamente
      </div>
    </div>
  );
}