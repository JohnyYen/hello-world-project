/**
 * Componente para la sección de mensajes de feedback
 */

'use client';

import { useState } from 'react';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Plus, X } from 'lucide-react';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';
import { cn } from '@/lib/utils';

export function FeedbackMessagesForm() {
  const { config, updateFeedbackMessage } = useEditor();
  const [newHint, setNewHint] = useState('');

  const handleAddHint = () => {
    if (newHint.trim()) {
              updateFeedbackMessage('hints', [...config.feedback_messages.hints, newHint.trim()] as string[]);
      setNewHint('');
    }
  };

  const handleRemoveHint = (index: number) => {
    const newHints = config.feedback_messages.hints.filter((_, i) => i !== index);
    updateFeedbackMessage('hints', newHints);
  };

  return (
    <FormSection
      title="Mensajes de Feedback"
      description="Mensajes que el estudiante verá al completar o fallar el nivel. Soportan formato markdown."
    >
      <div className="space-y-4">
        {/* Mensaje de éxito */}
        <div>
          <Label htmlFor="successMessage" className="flex items-center gap-2">
            <Badge variant="secondary" className="text-xs text-green-600">✓ Éxito</Badge>
            Mensaje de éxito
          </Label>
          <Textarea
            id="successMessage"
            placeholder="¡Excelente trabajo! Has completado el nivel correctamente."
            value={config.feedback_messages.success}
            onChange={(e) => updateFeedbackMessage('success', e.target.value)}
            rows={2}
          />
        </div>

        {/* Mensaje de fallo */}
        <div>
          <Label htmlFor="failureMessage" className="flex items-center gap-2">
            <Badge variant="destructive" className="text-xs">✗ Fallo</Badge>
            Mensaje de fallo
          </Label>
          <Textarea
            id="failureMessage"
            placeholder="Vuelve a intentarlo. Revisa las reglas del nivel."
            value={config.feedback_messages.failure}
            onChange={(e) => updateFeedbackMessage('failure', e.target.value)}
            rows={2}
          />
        </div>

        {/* Hints/Ayudas */}
        <div>
          <Label className="flex items-center gap-2">
            <Badge variant="secondary" className="text-xs">? Ayudas</Badge>
            Banco de hints
          </Label>
          <div className="space-y-2 mt-2">
            {/* Lista de hints */}
            <div className="flex flex-wrap gap-2">
              {config.feedback_messages.hints.length > 0 ? (
                config.feedback_messages.hints.map((hint: string, index: number) => (
                  <Badge
                    key={index}
                    variant="outline"
                    className="group flex items-center gap-1 pl-2 pr-1 py-1 cursor-pointer hover:bg-destructive hover:text-destructive-foreground transition-colors"
                    onClick={() => handleRemoveHint(index)}
                  >
                    <span className="max-w-[200px] truncate">{hint}</span>
                    <X size={10} className="ml-1 opacity-50 group-hover:opacity-100" />
                  </Badge>
                ))
              ) : (
                <p className="text-sm text-muted-foreground">
                  No hay hints configurados.
                </p>
              )}
            </div>

            {/* Añadir hint */}
            <div className="flex gap-2">
              <Input
                placeholder="Añadir hint para el estudiante"
                value={newHint}
                onChange={(e) => setNewHint(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddHint()}
              />
              <Button
                type="button"
                variant="outline"
                onClick={handleAddHint}
                disabled={!newHint.trim()}
              >
                <Plus size={16} className="mr-1" />
                Añadir
              </Button>
            </div>
          </div>
        </div>
      </div>
    </FormSection>
  );
}

export default FeedbackMessagesForm;
