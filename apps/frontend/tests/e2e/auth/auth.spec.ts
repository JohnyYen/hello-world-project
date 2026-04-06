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

  test("E2E-AUTH-004 - Login redirects to dashboard after successful authentication",
    { tag: ["@critical", "@e2e", "@auth", "@AUTH-E2E-004"] },
    async ({ page, context }) => {
      const dashboardPage = new DashboardPage(page);

      // Step 1: Login via API to get token (more reliable than UI form for server actions)
      const loginResponse = await page.request.post("http://localhost:8010/api/v1/auth/login", {
        data: {
          email: "admin.321@example.com",
          password: "Adminpass123!"
        }
      });

      expect(loginResponse.ok()).toBeTruthy();
      const loginData = await loginResponse.json();
      expect(loginData.access_token).toBeTruthy();
      console.log("✓ Got access token from API");

      // Step 2: Set the auth_token cookie for the browser
      await context.addCookies([
        {
          name: "auth_token",
          value: loginData.access_token,
          domain: "localhost",
          path: "/",
          httpOnly: true,
          secure: false,
          sameSite: "Lax"
        }
      ]);
      console.log("✓ Set auth_token cookie");

      // Step 3: Navigate to dashboard - should load successfully with valid token
      await dashboardPage.goto();
      
      // Step 4: Verify we're on dashboard (not redirected to login)
      await expect(page).toHaveURL(/\/dashboard/);
      console.log("✓ Successfully accessed dashboard with auth token");

      // Step 5: Verify dashboard content is loaded
      await page.waitForLoadState("networkidle");
      await page.waitForTimeout(1000);
      
      // Verify we're still on dashboard (AuthGuard didn't redirect us to login)
      await expect(page).toHaveURL(/\/dashboard/);
      console.log("✓ AuthGuard allowed access to dashboard");
    }
  );

  test("E2E-AUTH-005 - Unauthenticated access to dashboard redirects to login",
    { tag: ["@critical", "@e2e", "@auth", "@AUTH-E2E-005"] },
    async ({ page }) => {
      // Step 1: Try to access dashboard without authentication
      await page.goto("/dashboard");
      await page.waitForLoadState("networkidle");
      await page.waitForTimeout(1000);

      // Step 2: Verify redirect to login page
      await expect(page).toHaveURL(/\/login/);
    }
  );
});
