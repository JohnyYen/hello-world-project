/**
 * Panel de vista previa del JSON generado
 */

'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useEditor } from '@/lib/editor-store';
import { Copy, Download, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';

export function PreviewPanel() {
  const { config, exportToJson } = useEditor();
  const [jsonPreview, setJsonPreview] = useState('');
  const [copied, setCopied] = useState(false);

  // Actualizar vista previa cuando cambia la configuración
  useEffect(() => {
    setJsonPreview(exportToJson());
  }, [config, exportToJson]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(jsonPreview);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Error copiando:', error);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([jsonPreview], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${config.title || 'nivel'}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg flex items-center gap-2">
            <RefreshCw size={16} className="text-muted-foreground" />
            Vista Previa JSON
          </CardTitle>
          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={handleCopy}
              className="h-7 text-xs"
            >
              <Copy size={12} className="mr-1" />
              {copied ? '¡Copiado!' : 'Copiar'}
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={handleDownload}
              className="h-7 text-xs"
            >
              <Download size={12} className="mr-1" />
              Descargar
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex-1 min-h-0">
        <div className="h-full overflow-auto bg-muted rounded-md p-3">
          <pre className="text-xs font-mono whitespace-pre-wrap break-all">
            {jsonPreview}
          </pre>
        </div>
      </CardContent>
    </Card>
  );
}

export default PreviewPanel;
