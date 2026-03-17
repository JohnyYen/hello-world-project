/**
 * Componente para la sección de bloques/elementos disponibles
 */

'use client';

import { useState } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { X, Plus } from 'lucide-react';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';

export function AvailableBlocksForm() {
  const { config, addAvailableBlock, removeAvailableBlock } = useEditor();
  const [newBlock, setNewBlock] = useState('');

  const handleAddBlock = () => {
    if (newBlock.trim()) {
      addAvailableBlock(newBlock.trim());
      setNewBlock('');
    }
  };

  return (
    <FormSection
      title="Bloques/Elementos Disponibles"
      description="Lista de bloques de código o elementos que el estudiante puede usar para resolver el nivel."
    >
      <div className="space-y-4">
        {/* Lista de bloques actuales */}
        <div className="flex flex-wrap gap-2">
          {config.available_blocks.length > 0 ? (
            config.available_blocks.map((block, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="group flex items-center gap-1 pl-2 pr-1 py-1.5 cursor-pointer hover:bg-destructive hover:text-destructive-foreground transition-colors"
                onClick={() => removeAvailableBlock(index)}
              >
                <span>{block}</span>
                <X size={12} className="ml-1 opacity-50 group-hover:opacity-100" />
              </Badge>
            ))
          ) : (
            <p className="text-sm text-muted-foreground">
              No hay bloques configurados. Añade bloques usando el formulario de abajo.
            </p>
          )}
        </div>

        {/* Añadir nuevo bloque */}
        <div className="flex gap-2">
          <div className="flex-1">
            <Input
              placeholder="Nombre del bloque (ej: move_forward, if_condition)"
              value={newBlock}
              onChange={(e) => setNewBlock(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddBlock()}
            />
          </div>
          <Button
            type="button"
            variant="outline"
            onClick={handleAddBlock}
            disabled={!newBlock.trim()}
          >
            <Plus size={16} className="mr-1" />
            Añadir
          </Button>
        </div>

        {/* Ejemplos rápidos */}
        <div className="flex gap-2 flex-wrap">
          <span className="text-xs text-muted-foreground">Ejemplos rápidos:</span>
          {['move_forward', 'turn_left', 'if_condition', 'loop'].map((example) => (
            <Button
              key={example}
              type="button"
              variant="ghost"
              size="sm"
              className="h-6 text-xs"
              onClick={() => {
                if (!config.available_blocks.includes(example)) {
                  addAvailableBlock(example);
                }
              }}
            >
              + {example}
            </Button>
          ))}
        </div>
      </div>
    </FormSection>
  );
}

export default AvailableBlocksForm;
