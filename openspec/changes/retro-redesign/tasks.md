# Tasks: Retro Redesign

## Phase 1: Foundation & Infrastructure

- [x] **1.1 Configure CSS Variables & Tailwind Theme**  
  Modify `apps/frontend/src/app/globals.css` to define the retro color palette (Cream, Slate Dark, Amber Accent) and typography (`Courier New`) using `@theme` block.  
  *Dependency*: None.

- [x] **1.2 Create Theme Context & Provider**  
  Create `apps/frontend/src/components/theme/ThemeProvider.tsx` (Context API) and `useTheme.ts` hook to manage retro light/dark modes.  
  *Dependency*: None.

- [x] **1.3 Create Theme Toggle Component**  
  Create `apps/frontend/src/components/theme/theme-toggle.tsx` to switch between retro light/dark modes.  
  *Dependency*: 1.2.

- [x] **1.4 Define Visual Effects Utilities**  
  Add CSS classes `.scanlines`, `.retro-grid`, and `.flat-shadow` to `apps/frontend/src/app/globals.css`.  
  *Dependency*: 1.1.

## Phase 2: Component Styling

- [x] **2.1 Update Button Component (shadcn/ui)**  
  Modify `apps/frontend/src/components/ui/button.tsx` to support `variant="retro"` with thick borders, monospace font, and flat shadow.  
  *Dependency*: 1.1, 1.4.

- [x] **2.2 Update Card Component (shadcn/ui)**  
  Modify `apps/frontend/src/components/ui/card.tsx` to support retro styles (thick borders, padding).  
  *Dependency*: 1.1, 1.4.

- [x] **2.3 Update Input Component (shadcn/ui)**  
  Modify `apps/frontend/src/components/ui/input.tsx` to support retro styles (thick borders, distinct focus state).  
  *Dependency*: 1.1, 1.4.

- [x] **2.4 Update NavLanding (Header)**  
  Modify `apps/frontend/src/components/NavLanding.tsx` (or equivalent) to apply retro styling and use the ThemeProvider.  
  *Dependency*: 1.2, 2.1.

## Phase 3: Page Refactoring

- [ ] **3.1 Update Dashboard Layout**  
  Modify `apps/frontend/src/app/dashboard/layout.tsx` to apply retro styles, grid background, and integrate ThemeProvider.  
  *Dependency*: 1.2, 1.4.

- [ ] **3.2 Update HeroSection (Landing Page)**  
  Modify `apps/frontend/src/app/page.tsx` (or specific Hero component) to apply retro styling and effects.  
  *Dependency*: 1.2, 2.1, 2.2.

- [ ] **3.3 Update Login Page**  
  Modify `apps/frontend/src/app/(auth)/login/page.tsx` to apply retro styling.  
  *Dependency*: 1.2, 2.1, 2.3.

## Phase 4: Verification

- [ ] **4.1 Verify Accessibility (WCAG AA)**  
  Check contrast ratios for text/background combinations (Cream/Slate Dark, etc.) using browser dev tools or accessibility linter.  
  *Dependency*: All styling tasks.

- [ ] **4.2 Verify Visual Consistency**  
  Review all modified pages and components to ensure consistent application of the retro theme (colors, fonts, effects).  
  *Dependency*: All styling tasks.

- [ ] **4.3 Verify Responsiveness**  
  Test Dashboard and Login pages on mobile viewports to ensure components stack correctly and text remains readable.  
  *Dependency*: 3.1, 3.3.
