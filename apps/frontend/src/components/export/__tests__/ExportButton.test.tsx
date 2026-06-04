import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ExportButton } from "../ExportButton";
import * as useExportModule from "@/hooks/useExport";

vi.mock("@/hooks/useExport", () => ({
  useExport: vi.fn(),
}));

const mockUseExport = vi.mocked(useExportModule.useExport);

describe("ExportButton", () => {
  const ref = { current: document.createElement("div") } as React.RefObject<HTMLElement | null>;

  it("renders idle state with default label 'Exportar PDF'", () => {
    mockUseExport.mockReturnValue({
      exportPDF: vi.fn(),
      isExporting: false,
      error: null,
      progress: null,
      errors: [],
      resetError: vi.fn(),
    });

    render(<ExportButton targetRef={ref} />);
    expect(screen.getByText("Exportar PDF")).toBeInTheDocument();
  });

  it("renders custom label when provided", () => {
    mockUseExport.mockReturnValue({
      exportPDF: vi.fn(),
      isExporting: false,
      error: null,
      progress: null,
      errors: [],
      resetError: vi.fn(),
    });

    render(<ExportButton targetRef={ref} label="Descargar Informe" />);
    expect(screen.getByText("Descargar Informe")).toBeInTheDocument();
  });

  it("shows progress indicator during multi-section export", () => {
    mockUseExport.mockReturnValue({
      exportPDF: vi.fn(),
      isExporting: true,
      error: null,
      progress: { current: 2, total: 4 },
      errors: [],
      resetError: vi.fn(),
    });

    render(<ExportButton targetRef={ref} />);
    expect(screen.getByText("Exportando sección 2 de 4")).toBeInTheDocument();
  });

  it("shows spinner without progress for single-section export", () => {
    mockUseExport.mockReturnValue({
      exportPDF: vi.fn(),
      isExporting: true,
      error: null,
      progress: null,
      errors: [],
      resetError: vi.fn(),
    });

    render(<ExportButton targetRef={ref} />);
    expect(screen.getByText("Exportando...")).toBeInTheDocument();
  });

  it("renders error list when errors exist after export", () => {
    mockUseExport.mockReturnValue({
      exportPDF: vi.fn(),
      isExporting: false,
      error: null,
      progress: null,
      errors: [
        { sectionName: "KPIs", error: "Timeout capturando imagen" },
        { sectionName: "charts", error: "Elemento no encontrado" },
      ],
      resetError: vi.fn(),
    });

    render(<ExportButton targetRef={ref} />);
    expect(screen.getByText("Errores al exportar:")).toBeInTheDocument();
    expect(screen.getByText("KPIs: Timeout capturando imagen")).toBeInTheDocument();
    expect(screen.getByText("charts: Elemento no encontrado")).toBeInTheDocument();
    expect(screen.getByText("Cerrar")).toBeInTheDocument();
  });

  it("renders error banner when critical error occurs", () => {
    mockUseExport.mockReturnValue({
      exportPDF: vi.fn(),
      isExporting: false,
      error: "No se pudieron exportar secciones",
      progress: null,
      errors: [],
      resetError: vi.fn(),
    });

    render(<ExportButton targetRef={ref} />);
    expect(screen.getByText("Error al exportar")).toBeInTheDocument();
    expect(screen.getByText("No se pudieron exportar secciones")).toBeInTheDocument();
  });

  it("disables button while exporting", () => {
    mockUseExport.mockReturnValue({
      exportPDF: vi.fn(),
      isExporting: true,
      error: null,
      progress: null,
      errors: [],
      resetError: vi.fn(),
    });

    render(<ExportButton targetRef={ref} />);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
