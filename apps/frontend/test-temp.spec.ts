import { test, expect } from '@playwright/test';

test('temp test', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Plataforma Educativa/);
});
