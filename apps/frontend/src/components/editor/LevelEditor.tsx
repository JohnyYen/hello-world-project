/**
 * Componente principal del editor de niveles
 * Integra el formulario y la vista previa en un layout dividido
 */

'use client';

import { useState, useEffect } from 'react';
import { ConfigurationForm } from './ConfigurationForm';
import { PreviewPanel } from './PreviewPanel';
import { ExportControls } from './ExportControls';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

export function LevelEditor() {
  const [showPreview, setShowPreview] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024);
      if (window.innerWidth < 1024) {
        setShowPreview(false);
      } else {
        setShowPreview(true);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <div className="flex flex-col h-full">
      {/* Header con controles */}
      <div className="border-b bg-background px-4 py-3">
        <ExportControls />
      </div>

      {/* Área de trabajo principal */}
      <div className="flex flex-1 min-h-0 overflow-hidden">
        {/* Panel del formulario */}
        <div className={cn(
          "flex-1 overflow-hidden flex flex-col transition-all duration-300",
          !showPreview && "w-full"
        )}>
          <ScrollArea className="flex-1">
            <div className="p-4">
              <ConfigurationForm />
            </div>
          </ScrollArea>
        </div>

        {/* Toggle button para móvil */}
        {isMobile && (
          <Button
            variant="ghost"
            size="sm"
            className="absolute right-4 bottom-4 z-50 shadow-lg"
            onClick={() => setShowPreview(!showPreview)}
          >
            {showPreview ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          </Button>
        )}

        {/* Panel de vista previa */}
        {showPreview && (
          <div className={cn(
            "w-1/2 border-l overflow-hidden transition-all duration-300",
            isMobile && "fixed inset-0 z-40 bg-background"
          )}>
            <PreviewPanel />
          </div>
        )}
      </div>
    </div>
  );
}

export default LevelEditor;
