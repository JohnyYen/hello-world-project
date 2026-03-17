import { ExportProvider, type ExportOptions } from "../types";

export class CSVExportProvider extends ExportProvider {
  constructor(options: ExportOptions) {
    super(options);
  }

  async export(_element: HTMLElement): Promise<void> {
    throw new Error("CSV export no implementado aún");
  }
}
