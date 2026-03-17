/**
 * Página de lista de niveles guardados localmente
 */

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { PageHeader, PageHeaderDescription, PageHeaderTitle } from '@/components/ui/page-header';
import { Plus, Edit, Trash2, FileJson, Copy, Eye } from 'lucide-react';
import { listSavedLevels, loadFromLocalStorage, removeFromLocalStorage, formatDate, configToJson } from '@/lib/editor-helpers';
import { Badge } from '@/components/ui/badge';

interface SavedLevel {
  id: string;
  title: string;
  savedAt: string;
}

export default function LevelsListPage() {
  const [levels, setLevels] = useState<SavedLevel[]>([]);

  useEffect(() => {
    loadLevels();
  }, []);

  const loadLevels = () => {
    const savedLevels = listSavedLevels();
    setLevels(savedLevels);
  };

  const handleDelete = (id: string) => {
    if (confirm('¿Estás seguro de que quieres eliminar este nivel?')) {
      removeFromLocalStorage(id);
      loadLevels();
    }
  };

  const handleCopyJson = async (id: string) => {
    const data = loadFromLocalStorage(id);
    if (data) {
      const json = configToJson(data.config);
      await navigator.clipboard.writeText(json);
    }
  };

  const handleDownloadJson = (id: string, title: string) => {
    const data = loadFromLocalStorage(id);
    if (data) {
      const json = configToJson(data.config);
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${title}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <PageHeader>
        <div className="flex items-center justify-between">
          <div>
            <PageHeaderTitle>Niveles Guardados</PageHeaderTitle>
            <PageHeaderDescription>
              Gestiona los niveles creados localmente.
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
        {levels.length === 0 ? (
          <Card className="text-center py-12">
            <CardContent className="pt-6">
              <p className="text-muted-foreground mb-4">
                No hay niveles guardados todavía.
              </p>
              <Button asChild>
                <Link href="/dashboard/levels/create">
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
                        {level.title || 'Sin título'}
                      </CardTitle>
                      <CardDescription className="flex items-center gap-2 mt-1">
                        <Badge variant="outline" className="text-xs">
                          ID: {level.id.substring(0, 12)}...
                        </Badge>
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col justify-between gap-3">
                  <div className="text-xs text-muted-foreground">
                    Última edición: {formatDate(level.savedAt)}
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
                      onClick={() => handleCopyJson(level.id)}
                    >
                      <Copy size={12} className="mr-1" />
                      JSON
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-7 text-xs"
                      onClick={() => handleDownloadJson(level.id, level.title)}
                    >
                      <FileJson size={12} className="mr-1" />
                      Descargar
                    </Button>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-7 text-xs text-red-600 hover:text-red-700 ml-auto"
                      onClick={() => handleDelete(level.id)}
                    >
                      <Trash2 size={12} />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
