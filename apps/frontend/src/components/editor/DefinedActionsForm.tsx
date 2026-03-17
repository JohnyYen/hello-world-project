/**
 * Componente para la sección de acciones definidas
 */

'use client';

import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Plus, X } from 'lucide-react';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';
import { DefinedAction } from '@/types/editor';

export function DefinedActionsForm() {
  const { config, updateAction, addAction, removeAction } = useEditor();

  return (
    <FormSection
      title="Acciones Definidas"
      description="Lista de acciones que el jugador puede realizar, con sus valores asociados."
    >
      <div className="space-y-4">
        {/* Lista de acciones */}
        {config.defined_actions.length > 0 ? (
          <div className="space-y-3">
            {            config.defined_actions.map((action: { name: string; value: string }, index: number) => (
              <Card key={index} className="p-3">
                <div className="flex items-center gap-3">
                  <div className="flex-1 grid grid-cols-2 gap-3">
                    <div>
                      <Label className="text-xs text-muted-foreground">Nombre</Label>
                      <Input
                        placeholder="Nombre de la acción"
                        value={action.name}
                        onChange={(e) =>
                          updateAction(index, {
                            ...action,
                            name: e.target.value
                          })
                        }
                      />
                    </div>
                    <div>
                      <Label className="text-xs text-muted-foreground">Valor</Label>
                      <Input
                        placeholder="Valor/código asociado"
                        value={action.value}
                        onChange={(e) =>
                          updateAction(index, {
                            ...action,
                            value: e.target.value
                          })
                        }
                      />
                    </div>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => removeAction(index)}
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
            No hay acciones configuradas. Añade acciones para definir las interacciones del jugador.
          </p>
        )}

        {/* Añadir acción */}
        <Button
          type="button"
          variant="outline"
          onClick={addAction}
          className="w-full"
        >
          <Plus size={16} className="mr-2" />
          Añadir Acción
        </Button>
      </div>
    </FormSection>
  );
}

export default DefinedActionsForm;
