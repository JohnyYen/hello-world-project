/**
 * Página de lista de niveles del backend
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader, PageHeaderDescription, PageHeaderTitle } from "@/components/ui/page-header";
import { Plus, Edit, Trash2, FileJson, Copy } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import type { GameResponse } from "@/api/types";

interface LevelDisplay {
  id: string;
  title: string;
  description: string | null;
  goal: string | null;
  levelNumber: number;
  gameId: string;
  createdAt: string;
  updatedAt: string | null;
}

export default function LevelsListPage() {
  const [games, setGames] = useState<GameResponse[]>([]);
  const [selectedGameId, setSelectedGameId] = useState<string | null>(null);
  const [levels, setLevels] = useState<LevelDisplay[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingLevels, setIsLoadingLevels] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadGames = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      // Use backend API via server-side fetch with cookie
      const response = await fetch("/api/games");
      if (!response.ok) throw new Error("Failed to load games");
      const data = await response.json();
      const gamesData = data.data || data;
      if (gamesData && gamesData.length > 0) {
        setGames(gamesData);
        setSelectedGameId(gamesData[0].id);
      }
    } catch {
      setError("Error al cargar los juegos. Verifica que el backend esté disponible.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadLevels = useCallback(async (gameId: string) => {
    try {
      setIsLoadingLevels(true);
      const response = await fetch("/api/levels");
      if (!response.ok) throw new Error("Failed to load levels");
      const data = await response.json();
      const levelsData = data.data || data;
      if (levelsData) {
        const filtered = levelsData.filter((l: { game_id: string }) => l.game_id === gameId);
        setLevels(
          filtered.map((level: { id: string; title: string; description: string | null; goal: string | null; level_number: number; game_id: string; created_at: string; updated_at: string | null }): LevelDisplay => ({
            id: level.id,
            title: level.title,
            description: level.description ?? null,
            goal: level.goal ?? null,
            levelNumber: level.level_number,
            gameId: level.game_id,
            createdAt: level.created_at,
            updatedAt: level.updated_at ?? null,
          }))
        );
      }
    } catch {
      setError("Error al cargar los niveles.");
    } finally {
      setIsLoadingLevels(false);
    }
  }, []);

  useEffect(() => {
    loadGames();
  }, [loadGames]);

  useEffect(() => {
    if (selectedGameId !== null) {
      loadLevels(selectedGameId);
    }
  }, [selectedGameId, loadLevels]);

  const handleDelete = async (levelId: string) => {
    try {
      const response = await fetch(`/api/levels/${levelId}`, { method: "DELETE" });
      if (!response.ok) throw new Error("Failed to delete level");
      if (selectedGameId !== null) {
        loadLevels(selectedGameId);
      }
    } catch {
      setError("Error al eliminar el nivel.");
    }
  };

  const handleCopyJson = async (level: LevelDisplay) => {
    const json = JSON.stringify(
      {
        title: level.title,
        description: level.description,
        goal: level.goal,
        levelNumber: level.levelNumber,
      },
      null,
      2
    );
    await navigator.clipboard.writeText(json);
  };

  const handleDownloadJson = (level: LevelDisplay) => {
    const json = JSON.stringify(
      {
        title: level.title,
        description: level.description,
        goal: level.goal,
        levelNumber: level.levelNumber,
      },
      null,
      2
    );
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${level.title || "nivel"}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const formatDate = (date: string | Date): string => {
    return new Date(date).toLocaleDateString("es-ES", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="flex flex-col h-full">
      <PageHeader>
        <div className="flex items-center justify-between">
          <div>
            <PageHeaderTitle>Niveles</PageHeaderTitle>
            <PageHeaderDescription>
              Gestiona los niveles de los juegos.
            </PageHeaderDescription>
          </div>
          <Button asChild>
            <Link href="/dashboard/levels/create">
              <Plus size={16} className="mr-2" />
              Nuevo Nivel
            </Link>
          </Button>
        </div>
      </PageHeader>

      <div className="flex-1 p-4 overflow-auto">
        {isLoading ? (
          <Card className="text-center py-12">
            <CardContent className="pt-6">
              <p className="text-muted-foreground">Cargando juegos...</p>
            </CardContent>
          </Card>
        ) : error && games.length === 0 ? (
          <Card className="text-center py-12">
            <CardContent className="pt-6">
              <p className="text-red-500 mb-4">{error}</p>
              <Button onClick={loadGames}>Reintentar</Button>
            </CardContent>
          </Card>
        ) : games.length === 0 ? (
          <Card className="text-center py-12">
            <CardContent className="pt-6">
              <p className="text-muted-foreground mb-4">
                No hay juegos disponibles.
              </p>
              <Button asChild>
                <Link href="/dashboard/games/create">
                  <Plus size={16} className="mr-2" />
                  Crear tu primer juego
                </Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <>
            <div className="mb-4 flex items-center gap-4">
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">Juego:</span>
                <Select
                  value={selectedGameId?.toString() ?? ""}
                  onValueChange={(value) => setSelectedGameId(value)}
                >
                  <SelectTrigger className="w-[250px]">
                    <SelectValue placeholder="Selecciona un juego" />
                  </SelectTrigger>
                  <SelectContent>
                    {games.map((game) => (
                      <SelectItem key={game.id} value={game.id.toString()}>
                        {game.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {isLoadingLevels ? (
              <Card className="text-center py-12">
                <CardContent className="pt-6">
                  <p className="text-muted-foreground">Cargando niveles...</p>
                </CardContent>
              </Card>
            ) : levels.length === 0 ? (
              <Card className="text-center py-12">
                <CardContent className="pt-6">
                  <p className="text-muted-foreground mb-4">
                    No hay niveles para este juego.
                  </p>
                  <Button asChild>
                    <Link href={`/dashboard/levels/create?gameId=${selectedGameId}`}>
                      <Plus size={16} className="mr-2" />
                      Crear tu primer nivel
                    </Link>
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {levels.map((level) => (
                  <Card key={level.id} className="flex flex-col">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <CardTitle className="truncate text-base">
                            {level.title || "Sin título"}
                          </CardTitle>
                          <CardDescription className="flex items-center gap-2 mt-1">
                            <Badge variant="outline" className="text-xs">
                              Nivel {level.levelNumber}
                            </Badge>
                          </CardDescription>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="flex-1 flex flex-col justify-between gap-3">
                      <div className="text-xs text-muted-foreground">
                        Creado: {formatDate(level.createdAt)}
                        {level.updatedAt && (
                          <>
                            <br />
                            Actualizado: {formatDate(level.updatedAt)}
                          </>
                        )}
                      </div>

                      <div className="flex gap-2 flex-wrap">
                        <Button
                          asChild
                          variant="outline"
                          size="sm"
                          className="h-7 text-xs"
                        >
                          <Link href={`/dashboard/levels/${level.id}/edit`}>
                            <Edit size={12} className="mr-1" />
                            Editar
                          </Link>
                        </Button>

                        <Button
                          variant="outline"
                          size="sm"
                          className="h-7 text-xs"
                          onClick={() => handleCopyJson(level)}
                        >
                          <Copy size={12} className="mr-1" />
                          JSON
                        </Button>

                        <Button
                          variant="outline"
                          size="sm"
                          className="h-7 text-xs"
                          onClick={() => handleDownloadJson(level)}
                        >
                          <FileJson size={12} className="mr-1" />
                          Descargar
                        </Button>

                        <Dialog>
                          <DialogTrigger asChild>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-7 text-xs text-red-600 hover:text-red-700 ml-auto"
                            >
                              <Trash2 size={12} />
                            </Button>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Eliminar nivel</DialogTitle>
                              <DialogDescription>
                                ¿Estás seguro de que quieres eliminar el nivel &quot;{level.title}&quot;? Esta acción no se puede deshacer.
                              </DialogDescription>
                            </DialogHeader>
                            <DialogFooter>
                              <Button variant="outline">Cancelar</Button>
                              <Button
                                onClick={() => handleDelete(level.id)}
                                className="bg-red-600 hover:bg-red-700"
                              >
                                Eliminar
                              </Button>
                            </DialogFooter>
                          </DialogContent>
                        </Dialog>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
