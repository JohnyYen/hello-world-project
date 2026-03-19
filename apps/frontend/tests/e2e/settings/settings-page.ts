import { Page, Locator, expect } from "@playwright/test";
import { BasePage } from "../base/base-page";

export class SettingsPage extends BasePage {
  readonly profileTab: Locator;
  readonly notificationsTab: Locator;
  readonly languageSelect: Locator;
  readonly notificationsToggle: Locator;

  constructor(page: Page) {
    super(page);
    this.profileTab = page.getByRole("tab", { name: /perfil|profile/i });
    this.notificationsTab = page.getByRole("tab", { name: /notificaciones|notifications/i });
    this.languageSelect = page.getByLabel(/idioma|language/i);
    this.notificationsToggle = page.getByRole("switch", { name: /notificaciones|notifications/i });
  }

  async goto(): Promise<void> {
    await super.goto("/dashboard/settings");
  }

  async verifySettingsPage(): Promise<void> {
    await expect(this.page.getByText(/configuración|settings/i)).toBeVisible();
  }

  async verifyTabs(): Promise<void> {
    await expect(this.profileTab).toBeVisible();
    await expect(this.notificationsTab).toBeVisible();
  }
}
