/**
 * Componente para la sección de estado inicial del nivel
 */

'use client';

import { useState } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { X, Plus } from 'lucide-react';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';
import { cn } from '@/lib/utils';

export function InitialStateForm() {
  const { config, updateInitialField, removeInitialField } = useEditor();
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');

  const handleAddField = () => {
    if (newKey.trim()) {
      updateInitialField(newKey.trim(), newValue || '');
      setNewKey('');
      setNewValue('');
    }
  };

  const fields = Object.entries(config.initial_state);

  return (
    <FormSection
      title="Estado Inicial"
      description="Configura el estado inicial del juego. Estas variables estarán disponibles al inicio del nivel."
    >
      <div className="space-y-4">
        {/* Lista de campos existentes */}
        {fields.length > 0 ? (
          <div className="grid gap-2">
            {fields.map(([key, value]) => (
              <Card key={key} className="p-3">
                <div className="flex items-center gap-2">
                  <div className="flex-1 grid grid-cols-2 gap-2">
                    <div>
                      <Label className="text-xs text-muted-foreground">Llave</Label>
                      <Input
                        value={key}
                        readOnly
                        className="bg-muted"
                      />
                    </div>
                    <div>
                      <Label className="text-xs text-muted-foreground">Valor</Label>
                      <Input
                        value={String(value)}
                        onChange={(e) => updateInitialField(key, e.target.value)}
                      />
                    </div>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => removeInitialField(key)}
                    className="shrink-0 text-red-500 hover:text-red-700 hover:bg-red-50"
                  >
                    <X size={16} />
                    <span className="sr-only">Eliminar</span>
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground text-center py-4">
            No hay campos configurados aún. Añade tu primer campo abajo.
          </p>
        )}

        {/* Añadir nuevo campo */}
        <div className={cn("flex gap-2", fields.length > 0 && "pt-2 border-t")}>
          <div className="flex-1 grid grid-cols-2 gap-2">
            <Input
              placeholder="Llave (ej: x_position)"
              value={newKey}
              onChange={(e) => setNewKey(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddField()}
            />
            <Input
              placeholder="Valor (ej: 0)"
              value={newValue}
              onChange={(e) => setNewValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddField()}
            />
          </div>
          <Button
            type="button"
            variant="outline"
            onClick={handleAddField}
            disabled={!newKey.trim()}
          >
            <Plus size={16} className="mr-1" />
            Añadir
          </Button>
        </div>
      </div>
    </FormSection>
  );
}

export default InitialStateForm;
