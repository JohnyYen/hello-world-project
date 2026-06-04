import { Page, Locator, expect } from "@playwright/test";
import { BasePage } from "../base/base-page";

export class FeedbackModal extends BasePage {
  readonly title: Locator;
  readonly ratingButtons: Locator;
  readonly strengthsTextarea: Locator;
  readonly improvementsTextarea: Locator;
  readonly commentsTextarea: Locator;
  readonly submitButton: Locator;
  readonly cancelButton: Locator;
  readonly modalOverlay: Locator;
  readonly strengthsLabel: Locator;
  readonly improvementsLabel: Locator;

  constructor(page: Page) {
    super(page);
    this.title = page.getByRole("heading", { name: /feedback para/i });
    this.ratingButtons = page.locator("button[aria-label*='Calificación']");
    // Use placeholder-based selectors since labels may not be properly associated
    this.strengthsTextarea = page.locator("textarea[placeholder*='fortalezas y habilidades']");
    this.improvementsTextarea = page.locator("textarea[placeholder*='áreas donde el estudiante']");
    this.commentsTextarea = page.locator("textarea[placeholder*='comentario adicional']");
    this.submitButton = page.getByRole("button", { name: /enviar feedback/i });
    this.cancelButton = page.getByRole("button", { name: /cancelar/i });
    this.modalOverlay = page.locator(".fixed.inset-0.bg-black\\/50");
    this.strengthsLabel = page.getByText(/fortalezas del estudiante/i);
    this.improvementsLabel = page.getByText(/áreas de mejora/i);
  }

  async fillFeedback(form: {
    rating?: number;
    strengths?: string;
    improvements?: string;
    comments?: string;
  }): Promise<void> {
    if (form.rating) {
      await this.ratingButtons.nth(form.rating - 1).click();
    }
    if (form.strengths) {
      await this.strengthsTextarea.fill(form.strengths);
    }
    if (form.improvements) {
      await this.improvementsTextarea.fill(form.improvements);
    }
    if (form.comments) {
      await this.commentsTextarea.fill(form.comments);
    }
  }

  async submit(): Promise<void> {
    await this.submitButton.click();
  }

  async cancel(): Promise<void> {
    await this.cancelButton.click();
  }

  async verifyModalVisible(): Promise<void> {
    await expect(this.modalOverlay).toBeVisible();
    // Check for the card title which is the feedback heading
    await expect(this.page.locator("text=Feedback para").first()).toBeVisible();
  }

  async verifyRatingSelected(rating: number): Promise<void> {
    const selectedStars = this.page.locator("svg.fill-yellow-400");
    await expect(selectedStars).toHaveCount(rating);
  }
}

export class StudentDetailPage extends BasePage {
  readonly feedbackButton: Locator;
  readonly studentName: Locator;
  readonly studentEmail: Locator;
  readonly backButton: Locator;
  readonly feedbackHistorySection: Locator;
  readonly feedbackHistoryTitle: Locator;
  readonly feedbackEmptyState: Locator;

  constructor(page: Page) {
    super(page);
    // The button to open feedback modal - has MessageCircle icon and text "Feedback" 
    this.feedbackButton = page.locator("button:has-text('Feedback'):has(svg)").first();
    this.studentName = page.getByRole("heading", { level: 1 });
    this.studentEmail = page.locator("text=@").first();
    this.backButton = page.getByRole("link", { name: /volver a la lista/i });
    this.feedbackHistorySection = page.locator("text=Historial de feedback").locator("xpath=following-sibling::div").first();
    this.feedbackHistoryTitle = page.getByRole("heading", { name: /historial de feedback/i });
    this.feedbackEmptyState = page.getByText(/no hay feedback registrado/i);
  }

  async goto(studentId: string): Promise<void> {
    await super.goto(`/dashboard/students/${studentId}`);
  }

  async openFeedbackModal(): Promise<void> {
    await this.feedbackButton.click();
  }

  async verifyStudentDetailPage(): Promise<void> {
    await expect(this.studentName).toBeVisible();
    await expect(this.feedbackHistoryTitle).toBeVisible();
  }

  async verifyFeedbackHistoryItem(content: string): Promise<void> {
    const historyItem = this.page.locator(".border.rounded-lg.p-4").filter({ hasText: content });
    await expect(historyItem).toBeVisible({ timeout: 10000 });
  }

  async verifyFeedbackEmptyState(): Promise<void> {
    await expect(this.feedbackEmptyState).toBeVisible();
  }
}