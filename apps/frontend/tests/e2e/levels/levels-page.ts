import { Page, Locator, expect } from "@playwright/test";
import { BasePage } from "../base/base-page";

export class LevelsPage extends BasePage {
  readonly gameSelector: Locator;
  readonly levelsList: Locator;
  readonly loadingState: Locator;
  readonly emptyState: Locator;
  readonly createLevelButton: Locator;
  readonly levelCard: Locator;

  constructor(page: Page) {
    super(page);
    this.gameSelector = page.getByLabel(/juego|game/i).or(page.locator('[role="combobox"]'));
    this.levelsList = page.locator('[class*="grid"]').filter({ has: page.locator("[class*='card']") });
    this.loadingState = page.getByText(/cargando|loading/i);
    this.emptyState = page.getByText(/no hay niveles|no existen/i);
    this.createLevelButton = page.getByRole("link", { name: /nuevo.*nivel|crear.*nivel/i });
    this.levelCard = page.locator("[class*='card']").filter({ hasText: /nivel/i });
  }

  async goto(): Promise<void> {
    await super.goto("/dashboard/levels");
  }

  async verifyLevelsPage(): Promise<void> {
    await expect(this.page.getByText(/niveles|levels/i)).toBeVisible();
  }

  async verifyLevelsLoad(): Promise<void> {
    // Wait for loading to finish
    await this.loadingState.waitFor({ state: "hidden", timeout: 10000 }).catch(() => {});
    
    // Should show either levels or empty state
    const hasLevels = await this.levelsList.isVisible().catch(() => false);
    const hasEmpty = await this.emptyState.isVisible().catch(() => false);
    
    expect(hasLevels || hasEmpty).toBeTruthy();
  }

  async selectGame(gameName: string): Promise<void> {
    await this.gameSelector.click();
    await this.page.getByRole("option", { name: gameName }).click();
  }
}
