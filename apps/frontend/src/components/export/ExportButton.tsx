"use client";

import { useExport } from "@/hooks/useExport";
import { cn } from "@/lib/utils";
import type { ExportOptions } from "@/components/export/types";
import { FileDown, Loader2 } from "lucide-react";

interface ExportButtonProps {
  targetRef: React.RefObject<HTMLElement | null>;
  fileName?: string;
  options?: Partial<ExportOptions>;
  className?: string;
  variant?: "default" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  label?: string;
}

export function ExportButton({
  targetRef,
  fileName,
  options,
  className,
  variant = "default",
  size = "md",
  label = "Exportar PDF",
}: ExportButtonProps) {
  const { exportPDF, isExporting, error, resetError } = useExport();

  const handleExport = async () => {
    await exportPDF(targetRef, { ...options, fileName });
  };

  const baseStyles = "inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

  const variantStyles = {
    default: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 dark:bg-blue-600 dark:hover:bg-blue-700",
    outline: "border border-slate-300 text-slate-700 hover:bg-slate-50 focus:ring-slate-500 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800",
    ghost: "text-slate-700 hover:bg-slate-100 focus:ring-slate-500 dark:text-slate-300 dark:hover:bg-slate-800",
  };

  const sizeStyles = {
    sm: "text-sm px-3 py-1.5 gap-1.5",
    md: "text-sm px-4 py-2 gap-2",
    lg: "text-base px-5 py-2.5 gap-2",
  };

  return (
    <div className="relative">
      <button
        onClick={handleExport}
        disabled={isExporting}
        className={cn(
          baseStyles,
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
      >
        {isExporting ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Exportando...</span>
          </>
        ) : (
          <>
            <FileDown className="w-4 h-4" />
            <span>{label}</span>
          </>
        )}
      </button>

      {error && (
        <div className="absolute top-full mt-2 left-0 z-50">
          <div className="px-3 py-2 text-sm text-red-600 bg-red-50 rounded-lg border border-red-200 shadow-sm dark:bg-red-900/20 dark:border-red-800 dark:text-red-400">
            <p className="font-medium">Error al exportar</p>
            <p className="text-xs mt-1 opacity-80">{error}</p>
            <button
              onClick={resetError}
              className="text-xs underline mt-2 hover:text-red-700 dark:hover:text-red-300"
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
