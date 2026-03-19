import { Page, Locator, expect } from "@playwright/test";

export class BasePage {
  constructor(protected page: Page) {}

  async goto(path: string): Promise<void> {
    await this.page.goto(path);
    await this.page.waitForLoadState("networkidle");
  }

  async getCurrentUrl(): Promise<string> {
    return this.page.url();
  }

  async waitForNotification(): Promise<void> {
    await this.page.waitForSelector('[role="status"]', { timeout: 5000 }).catch(() => {
      // No notification appeared, that's okay
    });
  }

  async verifyRedirect(expectedPath: string): Promise<void> {
    await expect(this.page).toHaveURL(new RegExp(expectedPath));
  }
}

export interface AuthUser {
  email: string;
  password: string;
}

export interface TeacherProfile {
  fullName: string;
  email: string;
  username: string;
}
