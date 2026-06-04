import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";
import { useExport } from "../useExport";
import type { ExportOptions } from "@/components/export/types";

vi.mock("@/components/export/providers", () => ({
  PDFExportProvider: vi.fn(),
}));

const { PDFExportProvider } = await import("@/components/export/providers");
const MockPDFExportProvider = vi.mocked(PDFExportProvider);

describe("useExport progress/errors state", () => {
  const createRef = () =>
    ({ current: document.createElement("div") }) as React.RefObject<HTMLElement | null>;

  beforeEach(() => {
    vi.clearAllMocks();
    MockPDFExportProvider.mockImplementation(
      () =>
        ({
          export: vi.fn().mockResolvedValue(undefined),
          errors: [],
        }) as any,
    );
  });

  it("tracks progress via onProgress callback", async () => {
    let capturedOnProgress: ((p: { current: number; total: number; sectionName?: string }) => void) | undefined;

    MockPDFExportProvider.mockImplementation((options: ExportOptions) => {
      capturedOnProgress = options.onProgress!;
      return {
        export: vi.fn().mockImplementation(async () => {
          capturedOnProgress!({ current: 1, total: 4, sectionName: "Sec A" });
          capturedOnProgress!({ current: 2, total: 4, sectionName: "Sec B" });
        }),
        errors: [],
      } as any;
    });

    const { result } = renderHook(() => useExport());

    await act(async () => {
      await result.current.exportPDF(createRef());
    });

    expect(result.current.progress).toEqual({ current: 2, total: 4, sectionName: "Sec B" });
    expect(result.current.isExporting).toBe(false);
  });

  it("captures error when provider throws", async () => {
    const testError = new Error("No se pudieron exportar secciones: \"test\": Failed capture");

    MockPDFExportProvider.mockImplementation(
      () =>
        ({
          export: vi.fn().mockRejectedValue(testError),
          errors: [],
        }) as any,
    );

    const { result } = renderHook(() => useExport());

    await act(async () => {
      await result.current.exportPDF(createRef());
    });

    expect(result.current.error).toBe(testError.message);
    expect(result.current.isExporting).toBe(false);
  });

  it("captures ref not found error when targetRef.current is null", async () => {
    const { result } = renderHook(() => useExport());
    const emptyRef = { current: null } as React.RefObject<HTMLElement | null>;

    await act(async () => {
      await result.current.exportPDF(emptyRef);
    });

    expect(result.current.error).toBe("No se encontró el elemento a exportar");
    expect(result.current.isExporting).toBe(false);
  });

  it("resetError clears all state", async () => {
    MockPDFExportProvider.mockImplementation(
      () =>
        ({
          export: vi.fn().mockRejectedValue(new Error("fail")),
          errors: [],
        }) as any,
    );

    const { result } = renderHook(() => useExport());

    await act(async () => {
      await result.current.exportPDF(createRef());
    });

    expect(result.current.error).toBe("fail");

    act(() => {
      result.current.resetError();
    });

    expect(result.current.error).toBeNull();
    expect(result.current.isExporting).toBe(false);
    expect(result.current.progress).toBeNull();
  });

  it("sets isExporting true during export", async () => {
    let resolveExport: () => void;
    const exportPromise = new Promise<void>((resolve) => {
      resolveExport = resolve;
    });

    MockPDFExportProvider.mockImplementation(
      () =>
        ({
          export: vi.fn().mockReturnValue(exportPromise),
          errors: [],
        }) as any,
    );

    const { result } = renderHook(() => useExport());

    act(() => {
      result.current.exportPDF(createRef());
    });

    await waitFor(() => {
      expect(result.current.isExporting).toBe(true);
    });

    await act(async () => {
      resolveExport!();
    });

    expect(result.current.isExporting).toBe(false);
  });
});
