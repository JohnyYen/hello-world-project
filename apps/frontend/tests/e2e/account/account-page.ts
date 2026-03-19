import { Page, Locator, expect } from "@playwright/test";
import { BasePage } from "../base/base-page";

export class AccountPage extends BasePage {
  readonly profileName: Locator;
  readonly emailField: Locator;
  readonly usernameField: Locator;
  readonly changePasswordButton: Locator;

  constructor(page: Page) {
    super(page);
    this.profileName = page.locator("h2").filter({ hasText: /profesor|docente|teacher/i }).or(page.locator("text=/@\\w+/"));
    this.emailField = page.getByLabel(/email|correo/i);
    this.usernameField = page.getByLabel(/usuario|username/i);
    this.changePasswordButton = page.getByRole("button", { name: /cambiar contraseña|cambiar password/i });
  }

  async goto(): Promise<void> {
    await super.goto("/dashboard/account");
  }

  async verifyTeacherProfile(): Promise<void> {
    await expect(this.page.getByText(/mi perfil|cuenta/i)).toBeVisible();
    await expect(this.profileName).toBeVisible();
  }

  async verifyProfileFields(): Promise<void> {
    await expect(this.emailField).toBeVisible();
    await expect(this.usernameField).toBeVisible();
  }
}
