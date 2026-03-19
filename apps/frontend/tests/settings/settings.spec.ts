import { test, expect } from "@playwright/test";
import { SettingsPage } from "./settings-page";

test.describe("Settings Page", () => {
  test("E2E-SETTINGS-001 - Settings page loads correctly", async ({ page }) => {
    const settingsPage = new SettingsPage(page);
    await settingsPage.goto();
    
    await settingsPage.verifySettingsPage();
  });

  test("E2E-SETTINGS-002 - Settings page shows tabs", async ({ page }) => {
    const settingsPage = new SettingsPage(page);
    await settingsPage.goto();
    
    await settingsPage.verifyTabs();
  });
});
