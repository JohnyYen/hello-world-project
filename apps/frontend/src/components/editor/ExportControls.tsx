/**
 * Controles de exportación y guardado del editor de niveles
 */

'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useEditor } from '@/lib/editor-store';
import { formatDate } from '@/lib/editor-helpers';
import { Save, Download, Copy, RotateCcw, FolderOpen, List } from 'lucide-react';
import { useRouter } from 'next/navigation';

export function ExportControls() {
  const router = useRouter();
  const { config, saved, lastSaved, currentId, saveToLocalStorage, reset, loadFromLocalStorage, loadFromJson, exportToJson } = useEditor();
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [showLoadDialog, setShowLoadDialog] = useState(false);
  const [savedLevels, setSavedLevels] = useState<Array<{ id: string; title: string; savedAt: string }>>([]);
  const [jsonInput, setJsonInput] = useState('');

  const handleSave = () => {
    const id = saveToLocalStorage();
    setShowSaveDialog(false);
    router.refresh();
  };

  const handleExport = () => {
    const json = exportToJson();
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${config.title || 'nivel'}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleCopy = async () => {
    const json = exportToJson();
    await navigator.clipboard.writeText(json);
  };

  const handleLoadFromJson = () => {
    const success = loadFromJson(jsonInput);
    if (success) {
      setShowLoadDialog(false);
      setJsonInput('');
    }
  };

  const handleLoadLevel = (id: string) => {
    loadFromLocalStorage(id);
    setShowLoadDialog(false);
  };

  const handleOpenLoadDialog = () => {
    // Importamos listSavedLevels dinámicamente para evitar ciclos de importación
    import('@/lib/editor-helpers').then(({ listSavedLevels }) => {
      setSavedLevels(listSavedLevels());
    });
    setShowLoadDialog(true);
  };

  return (
    <div className="flex flex-wrap gap-2 items-center">
      {/* Botón de guardar */}
      <Button
        type="button"
        variant="default"
        onClick={handleSave}
        className="flex items-center gap-2"
      >
        <Save size={16} />
        Guardar
      </Button>

      {/* Badge de estado de guardado */}
      {saved && lastSaved && (
        <Badge variant="outline" className="text-xs">
          Guardado: {formatDate(lastSaved.toISOString())}
        </Badge>
      )}

      {/* Botón de exportar */}
      <Button
        type="button"
        variant="outline"
        onClick={handleExport}
        className="flex items-center gap-2"
      >
        <Download size={16} />
        Exportar JSON
      </Button>

      {/* Botón de copiar */}
      <Button
        type="button"
        variant="outline"
        onClick={handleCopy}
        className="flex items-center gap-2"
      >
        <Copy size={16} />
        Copiar JSON
      </Button>

      {/* Botón de cargar desde JSON */}
      <Dialog open={showLoadDialog} onOpenChange={setShowLoadDialog}>
        <DialogTrigger asChild>
          <Button
            type="button"
            variant="outline"
            className="flex items-center gap-2"
            onClick={handleOpenLoadDialog}
          >
            <FolderOpen size={16} />
            Cargar
          </Button>
        </DialogTrigger>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Cargar configuración</DialogTitle>
            <DialogDescription>
              Selecciona un nivel guardado o pega JSON para cargar.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Niveles guardados */}
            {savedLevels.length > 0 && (
              <div className="space-y-2">
                <Label>Niveles guardados</Label>
                <div className="max-h-40 overflow-auto border rounded-md">
                  {savedLevels.map((level) => (
                    <div
                      key={level.id}
                      className="flex items-center justify-between px-3 py-2 hover:bg-muted cursor-pointer"
                      onClick={() => handleLoadLevel(level.id)}
                    >
                      <div>
                        <p className="text-sm">{level.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {formatDate(level.savedAt)}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Cargar desde JSON */}
            <div className="space-y-2">
              <Label>O pegar JSON</Label>
              <Input
                placeholder='{"title": "...", ...}'
                value={jsonInput}
                onChange={(e) => setJsonInput(e.target.value)}
              />
            </div>
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowLoadDialog(false)}
            >
              Cancelar
            </Button>
            <Button
              onClick={handleLoadFromJson}
              disabled={!jsonInput.trim()}
            >
              Cargar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Botón de resetear */}
      <Button
        type="button"
        variant="ghost"
        onClick={() => {
          if (confirm('¿Estás seguro de que quieres resetear el editor? Se perderán los cambios no guardados.')) {
            reset();
          }
        }}
        className="flex items-center gap-2 text-red-600 hover:text-red-700"
      >
        <RotateCcw size={16} />
        Resetear
      </Button>
    </div>
  );
}

export default ExportControls;
