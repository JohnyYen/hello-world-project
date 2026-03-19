import { Page, Locator, expect } from "@playwright/test";
import { BasePage } from "../base/base-page";

export class StudentsPage extends BasePage {
  readonly studentTable: Locator;
  readonly loadingState: Locator;
  readonly emptyState: Locator;
  readonly createStudentButton: Locator;

  constructor(page: Page) {
    super(page);
    this.studentTable = page.locator("table").or(page.getByRole("grid"));
    this.loadingState = page.getByText(/cargando|loading/i);
    this.emptyState = page.getByText(/no hay|no existen|no hay estudiantes/i);
    this.createStudentButton = page.getByRole("link", { name: /crear.*estudiante|nuevo.*estudiante/i });
  }

  async goto(): Promise<void> {
    await super.goto("/dashboard/students");
  }

  async verifyStudentsPage(): Promise<void> {
    await expect(this.page.getByText(/estudiantes|students/i)).toBeVisible();
  }

  async verifyStudentListOrEmpty(): Promise<void> {
    // Wait for loading to finish
    await this.loadingState.waitFor({ state: "hidden", timeout: 10000 }).catch(() => {
      // Loading might already be done
    });
    
    // Should show either table or empty state
    const hasTable = await this.studentTable.isVisible().catch(() => false);
    const hasEmpty = await this.emptyState.isVisible().catch(() => false);
    
    expect(hasTable || hasEmpty).toBeTruthy();
  }
}
