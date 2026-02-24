'use client';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ChevronLeft } from "lucide-react";
import Link from "next/link";

type StudentNotFoundProps = {
  studentId: string;
};

export default function StudentNotFound({ studentId }: StudentNotFoundProps) {
  return (
    <div className="container mx-auto py-10">
      <Card>
        <CardHeader>
          <CardTitle>Estudiante no encontrado</CardTitle>
          <CardDescription>
            El estudiante con ID {studentId} no existe en la base de datos.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Link href="/dashboard/students">
            <Button variant="outline">
              <ChevronLeft className="h-4 w-4 mr-2" />
              Volver a la lista de estudiantes
            </Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}