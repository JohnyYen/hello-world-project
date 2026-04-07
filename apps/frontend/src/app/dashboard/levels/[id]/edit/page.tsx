"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { PageHeader, PageHeaderDescription, PageHeaderTitle } from "@/components/ui/page-header";
import { ArrowLeft, Save, Loader2 } from "lucide-react";
import Link from "next/link";
import type { LevelUpdate } from "@/api/types";

export default function EditLevelPage({
  params,
}: {
  params: { id: string };
}) {
  const router = useRouter();
  const levelId = params.id;

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [goal, setGoal] = useState("");
  const [levelNumber, setLevelNumber] = useState(1);
  const [gameId, setGameId] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const loadLevel = useCallback(async () => {
    if (!levelId || levelId === "undefined") {
      setError("ID de nivel inválido");
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const response = await fetch(`/api/levels/${levelId}`);
      if (!response.ok) throw new Error("Failed to load level");
      const data = await response.json();
      const levelData = data.data || data;
      if (levelData) {
        setTitle(levelData.title);
        setDescription(levelData.description ?? "");
        setGoal(levelData.goal ?? "");
        setLevelNumber(Number(levelData.level_number));
        setGameId(levelData.game_id);
      }
    } catch {
      setError("Error al cargar el nivel. Verifica que el backend esté disponible.");
    } finally {
      setIsLoading(false);
    }
  }, [levelId]);

  useEffect(() => {
    loadLevel();
  }, [loadLevel]);

  const handleSave = async () => {
    try {
      setIsSaving(true);
      setError(null);
      setSuccess(null);

      const updateData: LevelUpdate = {
        title,
        description: description || undefined,
        goal: goal || undefined,
        level_number: levelNumber,
      };

      const response = await fetch(`/api/levels/${levelId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updateData),
      });
      if (!response.ok) throw new Error("Failed to update level");
      setSuccess("Nivel actualizado correctamente");
      router.refresh();
    } catch {
      setError("Error al guardar el nivel.");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col h-full">
        <PageHeader>
          <PageHeaderTitle>Cargando...</PageHeaderTitle>
        </PageHeader>
        <div className="flex-1 flex items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <PageHeader>
        <div className="flex items-center justify-between">
          <div>
            <PageHeaderTitle>Editar Nivel</PageHeaderTitle>
            <PageHeaderDescription>
              Modifica los datos del nivel.
            </PageHeaderDescription>
          </div>
          <Button variant="outline" asChild>
            <Link href="/dashboard/levels">
              <ArrowLeft size={16} className="mr-2" />
              Volver
            </Link>
          </Button>
        </div>
      </PageHeader>

      <div className="flex-1 p-4 overflow-auto">
        {error && (
          <Card className="mb-4 border-red-500">
            <CardContent className="pt-6">
              <p className="text-red-500">{error}</p>
            </CardContent>
          </Card>
        )}

        {success && (
          <Card className="mb-4 border-green-500">
            <CardContent className="pt-6">
              <p className="text-green-500">{success}</p>
            </CardContent>
          </Card>
        )}

        <Card className="max-w-2xl">
          <CardHeader>
            <CardTitle>Datos del Nivel</CardTitle>
            <CardDescription>
              Nivel #{levelNumber} del juego #{gameId}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Título *</Label>
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Título del nivel"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Descripción</Label>
              <Input
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Descripción del nivel"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="goal">Objetivo</Label>
              <Input
                id="goal"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                placeholder="Objetivo del nivel"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="levelNumber">Número de Nivel</Label>
              <Input
                id="levelNumber"
                type="number"
                value={levelNumber}
                onChange={(e) => setLevelNumber(Number(e.target.value))}
                min={1}
                disabled
              />
              <p className="text-xs text-muted-foreground">
                El número de nivel no se puede cambiar después de creado.
              </p>
            </div>

            <div className="flex gap-2 pt-4">
              <Button onClick={handleSave} disabled={isSaving || !title.trim()}>
                {isSaving ? (
                  <>
                    <Loader2 size={16} className="mr-2 animate-spin" />
                    Guardando...
                  </>
                ) : (
                  <>
                    <Save size={16} className="mr-2" />
                    Guardar Cambios
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="max-w-2xl mt-4">
          <CardHeader>
            <CardTitle>Nota sobre la Configuración</CardTitle>
            <CardDescription>
              La configuración completa del nivel (bloques disponibles, estado
              inicial, criterios de validación, etc.) se edita localmente y
              no está sincronizada con el backend.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Para editar la configuración completa del nivel, usa el editor
              local en la página de creación de niveles y guarda en
              localStorage.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}