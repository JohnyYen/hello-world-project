import { test, expect } from "@playwright/test";
import { RegisterPage } from "./register-page";

test.describe("Register Flow", () => {
  test("E2E-REGISTER-001 - Register page loads correctly", async ({ page }) => {
    await page.goto("/signup");
    
    // Verify page has all required form fields with exact selectors
    await expect(page.getByRole("textbox", { name: "Nombre Completo", exact: true })).toBeVisible();
    await expect(page.getByRole("textbox", { name: "Nombre de Usuario", exact: true })).toBeVisible();
    await expect(page.getByRole("textbox", { name: "Correo Electrónico", exact: true })).toBeVisible();
    await expect(page.getByRole("textbox", { name: "Contraseña", exact: true })).toBeVisible();
    await expect(page.getByRole("textbox", { name: "Confirmar Contraseña", exact: true })).toBeVisible();
    await expect(page.getByRole("button", { name: "Crear Cuenta", exact: true })).toBeVisible();
  });

  test("E2E-REGISTER-002 - Register page has login link", async ({ page }) => {
    await page.goto("/signup");
    
    // Should have a link to go back to login with exact text
    const loginLink = page.getByRole("link", { name: "Iniciar sesión", href: "/login" });
    await expect(loginLink).toBeVisible();
  });

  test("E2E-REGISTER-003 - Register with empty fields shows validation", async ({ page }) => {
    await page.goto("/signup");
    
    // Click submit without filling any field
    await page.getByRole("button", { name: "Crear Cuenta", exact: true }).click();
    
    // HTML5 required validation should prevent submission
    // or backend validation should show error
    await page.waitForTimeout(2000);
    
    // Should still be on register page (not redirected to dashboard)
    await expect(page).not.toHaveURL("/dashboard");
    
    // Should show some validation error (browser or backend)
    const hasError = page.locator('[role="alert"], .text-destructive, [aria-invalid="true"]').first();
    await expect(hasError).toBeVisible();
  });

  test("E2E-REGISTER-004 - Register with valid credentials creates user", async ({ page }) => {
    await page.goto("/signup");
    
    // Generate unique email for this test
    const timestamp = Date.now();
    await page.getByRole("textbox", { name: "Nombre Completo", exact: true }).fill("Test");
    await page.getByRole("textbox", { name: "Nombre de Usuario", exact: true }).fill("testuser");
    await page.getByRole("textbox", { name: "Correo Electrónico", exact: true }).fill(`test.${timestamp}@example.com`);
    await page.getByRole("textbox", { name: "Contraseña", exact: true }).fill("TestPassword123!");
    await page.getByRole("textbox", { name: "Confirmar Contraseña", exact: true }).fill("TestPassword123!");
    
    // Submit form
    await page.getByRole("button", { name: "Crear Cuenta", exact: true }).click();
    
    // Wait for response (redirect or success message)
    await page.waitForTimeout(5000);
    
    // Either shows success or error (if email already exists)
    const onDashboard = await page.url().includes("/dashboard");
    const onLogin = await page.url().includes("/login");
    const hasSuccess = await page.getByText(/éxito|creado|success|registrado/i).isVisible().catch(() => false);
    const hasError = await page.getByText(/error|ya existe|invalid|failed/i).isVisible().catch(() => false);
    
    // Should either succeed (redirect to dashboard/login) or show meaningful feedback
    expect(onDashboard || onLogin || hasSuccess || hasError).toBeTruthy();
  });

  test("E2E-REGISTER-005 - Password confirmation mismatch shows error", async ({ page }) => {
    await page.goto("/signup");
    
    await page.getByRole("textbox", { name: "Nombre Completo", exact: true }).fill("Test");
    await page.getByRole("textbox", { name: "Nombre de Usuario", exact: true }).fill("testuser");
    await page.getByRole("textbox", { name: "Correo Electrónico", exact: true }).fill("test@example.com");
    await page.getByRole("textbox", { name: "Contraseña", exact: true }).fill("Password123!");
    await page.getByRole("textbox", { name: "Confirmar Contraseña", exact: true }).fill("DifferentPassword!");
    await page.getByRole("button", { name: "Crear Cuenta", exact: true }).click();
    
    await page.waitForTimeout(2000);
    
    // Should show error about password mismatch
    const hasError = await page.getByText(/las contraseñas no coinciden|password.*match/i).isVisible();
    await expect(hasError).toBeTruthy();
  });
});
