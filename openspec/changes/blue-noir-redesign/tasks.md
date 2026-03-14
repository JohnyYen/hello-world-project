# Tasks: Blue & Noir Redesign - Modern Minimalist

## Phase 1: Foundation - CSS Design Tokens

- [x] 1.1 Add gradient tokens to `apps/frontend/src/app/globals.css` - Define `--gradient-subtle`, `--gradient-mesh-*` for light and dark modes in :root and .dark
- [x] 1.2 Add glassmorphism utility tokens to `globals.css` - Define `--glass-bg`, `--glass-border`, `--glass-blur` variables
- [x] 1.3 Add gradient focus ring utility classes to `globals.css` - Create `.focus-gradient-ring` class for input focus states

## Phase 2: Core Components

- [x] 2.1 Add `gradient` variant to Button component in `apps/frontend/src/components/ui/button.tsx` - Use CVA to add gradient variant with shadow-lg
- [x] 2.2 Add `glass` variant to Button component in `apps/frontend/src/components/ui/button.tsx` - Add glassmorphism button style via CVA
- [x] 2.3 Update Card component in `apps/frontend/src/components/ui/card.tsx` - Replace flat-shadow border-4 with shadow-lg
- [x] 2.4 Add optional `gradient` prop to Card component in `apps/frontend/src/components/ui/card.tsx` - Enable subtle gradient background when true
- [x] 2.5 Add gradient focus ring to Input component in `apps/frontend/src/components/ui/input.tsx` - Apply gradient box-shadow on focus-visible state

## Phase 3: Layout Components

- [x] 3.1 Apply glassmorphism to Sidebar in `apps/frontend/src/components/ui/sidebar.tsx` - Add backdrop-blur and semi-transparent background classes
- [x] 3.2 Apply glassmorphism to Sheet in `apps/frontend/src/components/ui/sheet.tsx` - Add glassmorphism to SheetContent and blur overlay

## Phase 4: Landing Page

- [ ] 4.1 Update Hero section in `apps/frontend/src/components/landing/hero-section.tsx` - Add gradient mesh background using CSS mesh gradient tokens
- [ ] 4.2 Update Feature cards in `apps/frontend/src/components/landing/features-section.tsx` - Apply gradient styling and shadow-lg to feature cards
- [ ] 4.3 Update Navbar in `apps/frontend/src/components/landing/nav-landing.tsx` - Add glassmorphism effect to navbar container

## Phase 5: Dashboard

- [ ] 5.1 Update metric cards in `apps/frontend/src/components/dashboard/section-cards.tsx` - Apply gradient backgrounds and elegant shadows to metric cards
- [ ] 5.2 Verify Dashboard sidebar has glassmorphism in `apps/frontend/src/components/dashboard/app-sidebar.tsx` - Ensure it uses the updated Sidebar component

## Phase 6: Verification

- [ ] 6.1 Verify light mode - Test all components display correctly in light mode with new gradient/shadow/glass styles
- [ ] 6.2 Verify dark mode - Test all components display correctly in dark mode with adapted gradient/shadow/glass styles
- [ ] 6.3 Verify backward compatibility - Ensure existing button variants (default, secondary, outline, ghost, destructive) and retro variant still work
- [ ] 6.4 Verify accessibility - Confirm focus indicators are visible and meet WCAG requirements
- [ ] 6.5 Verify performance - Check animations run smoothly at 60fps, no jank on glassmorphism elements
