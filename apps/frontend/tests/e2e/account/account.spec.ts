import { test, expect } from "@playwright/test";
import { AccountPage } from "./account-page";

test.describe("Account Page", () => {
  test("E2E-ACCOUNT-001 - Account page loads and shows teacher profile", async ({ page }) => {
    const accountPage = new AccountPage(page);
    await accountPage.goto();
    
    await accountPage.verifyTeacherProfile();
  });

  test("E2E-ACCOUNT-002 - Account page shows profile fields", async ({ page }) => {
    const accountPage = new AccountPage(page);
    await accountPage.goto();
    
    await accountPage.verifyProfileFields();
  });

  test("E2E-ACCOUNT-003 - Account page has change password option", async ({ page }) => {
    const accountPage = new AccountPage(page);
    await accountPage.goto();
    
    await expect(accountPage.changePasswordButton).toBeVisible();
  });
});
