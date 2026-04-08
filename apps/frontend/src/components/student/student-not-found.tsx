'use client';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ChevronLeft, UserX } from "lucide-react";
import Link from "next/link";

export default function StudentNotFound() {
  return (
    <div className="container mx-auto py-10">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <UserX className="h-5 w-5" />
            Estudiante no encontrado
          </CardTitle>
          <CardDescription>
            El estudiante que buscas no existe o ha sido removido de la base de datos.
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