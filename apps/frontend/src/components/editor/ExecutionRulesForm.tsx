/**
 * Componente para la sección de reglas de ejecución
 */

'use client';

import { useEffect, useState } from 'react';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { AlertCircle, CheckCircle, RefreshCw } from 'lucide-react';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';

export function ExecutionRulesForm() {
  const { config, updateField } = useEditor();
  const [jsonString, setJsonString] = useState('');
  const [isValid, setIsValid] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Inicializar con el JSON actual
  useEffect(() => {
    setJsonString(JSON.stringify(config.execution_rules, null, 2));
  }, []);

  // Validar JSON cuando cambia
  useEffect(() => {
    try {
      JSON.parse(jsonString);
      setIsValid(true);
      setError(null);
    } catch (e) {
      setIsValid(false);
      setError(e instanceof Error ? e.message : 'JSON inválido');
    }
  }, [jsonString]);

  const handleUpdate = () => {
    try {
      const parsed = JSON.parse(jsonString);
      updateField('execution_rules', parsed);
    } catch (e) {
      // JSON inválido, no actualizar
    }
  };

  const handleReset = () => {
    const defaultRules = {
      max_steps: 100,
      timeout_ms: 5000,
      allow_debugging: true
    };
    setJsonString(JSON.stringify(defaultRules, null, 2));
    updateField('execution_rules', defaultRules);
  };

  return (
    <FormSection
      title="Reglas de Ejecución"
      description="Define las reglas bajo las cuales se ejecuta el nivel (límites, restricciones, etc.)."
    >
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <Label htmlFor="executionRules">Reglas (JSON)</Label>
          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={handleReset}
              className="h-7 text-xs"
            >
              <RefreshCw size={12} className="mr-1" />
              Resetear
            </Button>
            {isValid ? (
              <span className="flex items-center gap-1 text-xs text-green-600">
                <CheckCircle size={12} />
                Válido
              </span>
            ) : (
              <span className="flex items-center gap-1 text-xs text-red-600">
                <AlertCircle size={12} />
                Inválido
              </span>
            )}
          </div>
        </div>
        
        <Textarea
          id="executionRules"
          value={jsonString}
          onChange={(e) => setJsonString(e.target.value)}
          onBlur={handleUpdate}
          className="font-mono text-sm h-32"
          placeholder='{"max_steps": 100, "timeout_ms": 5000}'
        />
        
        {error && (
          <p className="text-xs text-red-600 bg-red-50 px-2 py-1 rounded">
            {error}
          </p>
        )}
      </div>
    </FormSection>
  );
}

export default ExecutionRulesForm;
