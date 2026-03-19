import { Page, Locator, expect } from "@playwright/test";
import { BasePage } from "../base/base-page";

export class RegisterPage extends BasePage {
  readonly nameInput: Locator;
  readonly lastnameInput: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly confirmPasswordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly successMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.nameInput = page.getByLabel(/nombre|name/i);
    this.lastnameInput = page.getByLabel(/apellido|lastname|surname/i);
    this.emailInput = page.getByLabel(/email|correo/i);
    this.passwordInput = page.getByLabel(/contraseña|password/i);
    this.confirmPasswordInput = page.getByLabel(/confirm|confirmar/i);
    this.submitButton = page.getByRole("button", { name: /registrar|registrarme|sign up|crear/i });
    this.errorMessage = page.getByText(/error|inválido|ya existe/i);
    this.successMessage = page.getByText(/registrado|creado|éxito|success/i);
  }

  async goto(): Promise<void> {
    await super.goto("/signup");
  }

  async register(credentials: {
    name: string;
    lastname: string;
    email: string;
    password: string;
  }): Promise<void> {
    await this.nameInput.fill(credentials.name);
    await this.lastnameInput.fill(credentials.lastname);
    await this.emailInput.fill(credentials.email);
    await this.passwordInput.fill(credentials.password);
    await this.confirmPasswordInput.fill(credentials.password);
    await this.submitButton.click();
  }
}
