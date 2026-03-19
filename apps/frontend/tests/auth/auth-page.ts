import { Page, Locator, expect } from "@playwright/test";
import { BasePage, AuthUser } from "../base/base-page";

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByLabel(/email|correo/i);
    this.passwordInput = page.getByLabel(/contraseña|password/i);
    this.submitButton = page.getByRole("button", { name: /entrar|sign in|iniciar/i });
    this.errorMessage = page.getByText(/error|credenciales inválidas/i);
  }

  async goto(): Promise<void> {
    await super.goto("/login");
  }

  async login(credentials: AuthUser): Promise<void> {
    await this.emailInput.fill(credentials.email);
    await this.passwordInput.fill(credentials.password);
    await this.submitButton.click();
  }

  async verifyLoginError(): Promise<void> {
    await expect(this.errorMessage).toBeVisible();
  }
}

export class DashboardPage extends BasePage {
  readonly accountLink: Locator;
  readonly settingsLink: Locator;
  readonly studentsLink: Locator;
  readonly levelsLink: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    super(page);
    this.accountLink = page.getByRole("link", { name: /cuenta|perfil|account/i });
    this.settingsLink = page.getByRole("link", { name: /configuración|settings/i });
    this.studentsLink = page.getByRole("link", { name: /estudiantes|students/i });
    this.levelsLink = page.getByRole("link", { name: /niveles|levels/i });
    this.logoutButton = page.getByRole("button", { name: /cerrar sesión|logout|salir/i });
  }

  async goto(): Promise<void> {
    await super.goto("/dashboard");
  }

  async verifyLoggedIn(): Promise<void> {
    await expect(this.page.getByText(/bienvenido|dashboard|gestiona/i)).toBeVisible();
  }

  async logout(): Promise<void> {
    await this.logoutButton.click();
  }
}
