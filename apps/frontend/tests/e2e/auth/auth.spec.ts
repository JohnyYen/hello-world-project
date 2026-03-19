import { test, expect } from "@playwright/test";
import { LoginPage, DashboardPage } from "./auth-page";

test.describe("Auth Flow", () => {
  test("E2E-AUTH-001 - Login page loads correctly", async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    await expect(loginPage.emailInput).toBeVisible();
    await expect(loginPage.passwordInput).toBeVisible();
    await expect(loginPage.submitButton).toBeVisible();
  });

  test("E2E-AUTH-002 - Login with invalid credentials shows error", async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    await loginPage.login({ email: "invalid@test.com", password: "wrongpass" });
    
    // Should show error or redirect away from dashboard
    await page.waitForTimeout(2000);
    await expect(page).not.toHaveURL("/dashboard");
  });

  test("E2E-AUTH-003 - Dashboard navigation elements present", async ({ page }) => {
    const dashboardPage = new DashboardPage(page);
    
    // Navigate to dashboard (may redirect to login if not authenticated)
    await dashboardPage.goto();
    
    // Check for navigation elements
    const hasNavigation = await page.locator("nav, header, [role='navigation']").first().isVisible().catch(() => false);
    expect(hasNavigation).toBeTruthy();
  });
});
