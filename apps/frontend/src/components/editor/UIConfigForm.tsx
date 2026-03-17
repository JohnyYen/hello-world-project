/**
 * Componente para la sección de configuración de UI
 */

'use client';

import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { useEditor } from '@/lib/editor-store';
import { FormSection } from './FormSection';

export function UIConfigForm() {
  const { config, updateUiConfig } = useEditor();

  return (
    <FormSection
      title="Configuración de UI"
      description="Configura cómo se ve y se comporta la interfaz del nivel."
    >
      <div className="space-y-6">
        {/* Configuración del editor de código */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Badge variant="secondary">Editor de Código</Badge>
          </div>
          
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="syntaxHighlighting" className="flex flex-col">
                <span>Sintaxis highlighting</span>
                <span className="text-xs text-muted-foreground">Colorear el código según el lenguaje</span>
              </Label>
              <Switch
                id="syntaxHighlighting"
                checked={config.ui_config.code_editor.syntax_highlighting}
                onCheckedChange={(checked) =>
                  updateUiConfig({
                    code_editor: {
                      ...config.ui_config.code_editor,
                      syntax_highlighting: checked
                    }
                  })
                }
              />
            </div>

            <div className="flex items-center justify-between">
              <Label htmlFor="lineNumbers" className="flex flex-col">
                <span>Números de línea</span>
                <span className="text-xs text-muted-foreground">Mostrar números en el margen</span>
              </Label>
              <Switch
                id="lineNumbers"
                checked={config.ui_config.code_editor.line_numbers}
                onCheckedChange={(checked) =>
                  updateUiConfig({
                    code_editor: {
                      ...config.ui_config.code_editor,
                      line_numbers: checked
                    }
                  })
                }
              />
            </div>
          </div>
        </div>

        {/* Configuración de visualización */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Badge variant="secondary">Visualización</Badge>
          </div>
          
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="showState" className="flex flex-col">
                <span>Mostrar estado</span>
                <span className="text-xs text-muted-foreground">Ver variables durante la ejecución</span>
              </Label>
              <Switch
                id="showState"
                checked={config.ui_config.visualization.show_state}
                onCheckedChange={(checked) =>
                  updateUiConfig({
                    visualization: {
                      ...config.ui_config.visualization,
                      show_state: checked
                    }
                  })
                }
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="animationSpeed" className="flex flex-col">
                <span>Velocidad de animación</span>
                <span className="text-xs text-muted-foreground">
                  {config.ui_config.visualization.animation_speed.toFixed(1)}x
                </span>
              </Label>
            </div>
            <Slider
              id="animationSpeed"
              min={0.1}
              max={5.0}
              step={0.1}
              value={[config.ui_config.visualization.animation_speed]}
              onValueChange={([value]) =>
                updateUiConfig({
                  visualization: {
                    ...config.ui_config.visualization,
                    animation_speed: value
                  }
                })
              }
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>0.1x (lento)</span>
              <span>5.0x (rápido)</span>
            </div>
          </div>
        </div>
      </div>
    </FormSection>
  );
}

export default UIConfigForm;
