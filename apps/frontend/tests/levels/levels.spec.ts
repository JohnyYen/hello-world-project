import { test, expect } from "@playwright/test";
import { LevelsPage } from "./levels-page";

test.describe("Levels Page", () => {
  test("E2E-LEVELS-001 - Levels page loads correctly", async ({ page }) => {
    const levelsPage = new LevelsPage(page);
    await levelsPage.goto();
    
    await levelsPage.verifyLevelsPage();
  });

  test("E2E-LEVELS-002 - Levels list loads or shows empty state", async ({ page }) => {
    const levelsPage = new LevelsPage(page);
    await levelsPage.goto();
    
    await levelsPage.verifyLevelsLoad();
  });

  test("E2E-LEVELS-003 - Game selector is visible", async ({ page }) => {
    const levelsPage = new LevelsPage(page);
    await levelsPage.goto();
    
    await expect(levelsPage.gameSelector).toBeVisible();
  });
});
