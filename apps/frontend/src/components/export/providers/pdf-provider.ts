import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";
import { ExportProvider, type ExportOptions } from "../types";

export class PDFExportProvider extends ExportProvider {
  constructor(options: ExportOptions) {
    super(options);
  }

  async export(element: HTMLElement): Promise<void> {
    try {
      const scale = this.options.scale || 2;
      const quality = this.options.quality || 1;

      const canvas = await html2canvas(element, {
        scale,
        useCORS: true,
        allowTaint: true,
        backgroundColor: "#ffffff",
        logging: false,
      });

      const imgData = canvas.toDataURL("image/jpeg", quality);

      const imgWidth = canvas.width;
      const imgHeight = canvas.height;

      const pdf = new jsPDF({
        orientation: this.options.orientation || "portrait",
        unit: "px",
        format: [imgWidth / scale, imgHeight / scale],
      });

      pdf.addImage(imgData, "JPEG", 0, 0, imgWidth / scale, imgHeight / scale);

      const fileName = this.getFileName();
      pdf.save(`${fileName}.pdf`);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Error desconocido al exportar PDF";
      throw new Error(`Error al exportar PDF: ${message}`);
    }
  }
}
