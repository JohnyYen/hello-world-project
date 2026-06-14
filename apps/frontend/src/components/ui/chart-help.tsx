"use client";

import { Info } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface ChartHelpProps {
  /** Texto descriptivo que se muestra en el tooltip */
  content: string;
}

/**
 * Ícono de ayuda con tooltip para gráficos.
 * Agrega un ⓘ sutil al lado del título que al hacer hover
 * explica para qué sirve analizar ese gráfico.
 */
export function ChartHelp({ content }: ChartHelpProps) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button
          type="button"
          className="inline-flex items-center justify-center align-middle ml-1.5 -mt-0.5 rounded-full text-muted-foreground/60 hover:text-muted-foreground transition-colors cursor-help focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-label="Más información sobre este gráfico"
        >
          <Info className="h-4 w-4" />
        </button>
      </TooltipTrigger>
      <TooltipContent
        side="right"
        align="center"
        className="max-w-[260px] text-xs leading-relaxed"
      >
        {content}
      </TooltipContent>
    </Tooltip>
  );
}
