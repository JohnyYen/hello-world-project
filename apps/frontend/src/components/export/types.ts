export type ExportFormat = "pdf" | "csv";

export interface ExportOptions {
  fileName?: string;
  format: ExportFormat;
  scale?: number;
  quality?: number;
  orientation?: "portrait" | "landscape";
}

export abstract class ExportProvider {
  protected options: ExportOptions;

  constructor(options: ExportOptions) {
    this.options = options;
  }

  abstract export(element: HTMLElement): Promise<void>;

  protected getFileName(): string {
    return this.options.fileName || `export-${Date.now()}`;
  }
}
