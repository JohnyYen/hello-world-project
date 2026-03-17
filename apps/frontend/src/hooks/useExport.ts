"use client";

import { useState, useRef } from "react";
import { PDFExportProvider } from "@/components/export/providers";
import type { ExportOptions } from "@/components/export/types";

type ExportState = "idle" | "loading" | "success" | "error";

interface UseExportReturn {
  exportPDF: (targetRef: React.RefObject<HTMLElement | null>, options?: Partial<ExportOptions>) => Promise<void>;
  isExporting: boolean;
  error: string | null;
  resetError: () => void;
}

export function useExport(): UseExportReturn {
  const [state, setState] = useState<ExportState>("idle");
  const [error, setError] = useState<string | null>(null);

  const resetError = () => {
    setError(null);
    setState("idle");
  };

  const exportPDF = async (
    targetRef: React.RefObject<HTMLElement | null>,
    options?: Partial<ExportOptions>
  ): Promise<void> => {
    if (!targetRef.current) {
      const errMsg = "No se encontró el elemento a exportar";
      setError(errMsg);
      setState("error");
      return;
    }

    setState("loading");
    setError(null);

    try {
      const defaultOptions: ExportOptions = {
        format: "pdf",
        fileName: options?.fileName || "reporte",
        scale: options?.scale || 2,
        quality: options?.quality || 1,
        orientation: options?.orientation || "portrait",
      };

      const provider = new PDFExportProvider(defaultOptions);
      await provider.export(targetRef.current);

      setState("success");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Error desconocido";
      setError(message);
      setState("error");
    }
  };

  return {
    exportPDF,
    isExporting: state === "loading",
    error,
    resetError,
  };
}
