/**
 * Componente para la sección de criterios de validación
 */

'use client';

import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent } from '@/components/ui/card';
import { Plus, X, AlertCircle } from 'lucide-react';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';
import { ValidationCriterion } from '@/types/editor';

export function ValidationCriteriaForm() {
  const { config, updateValidationCriterion, addValidationCriterion, removeValidationCriterion } = useEditor();

  return (
    <FormSection
      title="Criterios de Validación"
      description="Define las condiciones que deben cumplirse para considerar el nivel completado correctamente."
    >
      <div className="space-y-4">
        {/* Lista de criterios */}
        {config.validation_criteria.length > 0 ? (
          <div className="space-y-3">
            {config.validation_criteria.map((criterion, index) => (
              <Card key={index} className="p-3">
                <div className="flex items-start gap-3">
                  <div className="flex-1 grid gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <Label className="text-xs text-muted-foreground flex items-center gap-1">
                          <AlertCircle size={12} />
                          Condición
                        </Label>
                        <Input
                          placeholder="Ej: resultado_final == 42"
                          value={criterion.condition}
                          onChange={(e) =>
                            updateValidationCriterion(index, {
                              ...criterion,
                              condition: e.target.value
                            })
                          }
                        />
                      </div>
                      <div>
                        <Label className="text-xs text-muted-foreground">Descripción</Label>
                        <Input
                          placeholder="Descripción para el estudiante"
                          value={criterion.description}
                          onChange={(e) =>
                            updateValidationCriterion(index, {
                              ...criterion,
                              description: e.target.value
                            })
                          }
                        />
                      </div>
                    </div>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => removeValidationCriterion(index)}
                    className="shrink-0 text-red-500 hover:text-red-700 hover:bg-red-50 mt-6"
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
            No hay criterios de validación configurados.
          </p>
        )}

        {/* Añadir criterio */}
        <Button
          type="button"
          variant="outline"
          onClick={addValidationCriterion}
          className="w-full"
        >
          <Plus size={16} className="mr-2" />
          Añadir Criterio de Validación
        </Button>
      </div>
    </FormSection>
  );
}

export default ValidationCriteriaForm;
