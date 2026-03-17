/**
 * Componente para la sección de información básica del nivel
 */

'use client';

import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';

export function BasicInfoForm() {
  const { config, updateField, generateNewSegmentId } = useEditor();

  return (
    <FormSection
      title="Información Básica"
      description="Datos generales del nivel como título, descripción y objetivo educacional."
    >
      <div className="grid gap-4 sm:grid-cols-2">
        {/* Título */}
        <div className="sm:col-span-2">
          <Label htmlFor="title" className="required">Título</Label>
          <Input
            id="title"
            placeholder="Nombre del nivel"
            value={config.title}
            onChange={(e) => updateField('title', e.target.value)}
            maxLength={200}
          />
        </div>

        {/* Descripción */}
        <div className="sm:col-span-2">
          <Label htmlFor="description">Descripción</Label>
          <Textarea
            id="description"
            placeholder="Descripción detallada del nivel"
            value={config.description || ''}
            onChange={(e) => updateField('description', e.target.value)}
            rows={3}
            maxLength={1000}
          />
        </div>

        {/* Segment ID */}
        <div className="flex items-end gap-2">
          <div className="flex-1">
            <Label htmlFor="segmentId" className="flex items-center gap-2">
              ID de Segmento
              <Badge variant="outline" className="text-xs">
                {config.segment_id}
              </Badge>
            </Label>
            <Input
              id="segmentId"
              type="number"
              value={config.segment_id}
              onChange={(e) => updateField('segment_id', Number(e.target.value))}
              readOnly
              disabled
            />
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={generateNewSegmentId}
            className="mb-[1px]"
          >
            Generar
          </Button>
        </div>

        {/* Versión */}
        <div>
          <Label htmlFor="version">Versión</Label>
          <Input
            id="version"
            type="number"
            step="0.1"
            value={config.version}
            onChange={(e) => updateField('version', Number(e.target.value))}
          />
        </div>

        {/* Objetivo Educativo */}
        <div className="sm:col-span-2">
          <Label htmlFor="learningObjective" className="required">Objetivo Educativo</Label>
          <Textarea
            id="learningObjective"
            placeholder="¿Qué debe aprender el estudiante con este nivel?"
            value={config.learning_objective}
            onChange={(e) => updateField('learning_objective', e.target.value)}
            rows={2}
            maxLength={500}
          />
        </div>
      </div>
    </FormSection>
  );
}

export default BasicInfoForm;
