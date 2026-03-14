# Design: Blue & Noir Redesign - Modern Minimalist

## Technical Approach

This design transforms the frontend from a retro/vintage aesthetic (flat-shadow, prominent borders, scanlines) to a modern minimalist design with subtle gradients, elegant shadows, and glassmorphism effects. The implementation leverages Tailwind 4's CSS-first configuration and maintains the existing Blue & Noir color palette while introducing new design tokens.

**Key Strategy:**
1. Extend existing CSS variables in `globals.css` with gradient and glassmorphism tokens
2. Add new button variants via CVA (preserving existing variants for backward compatibility)
3. Refactor Card, Input to use modern shadows without breaking existing APIs
4. Apply glassmorphism via CSS backdrop-filter utilities
5. Landing and Dashboard pages receive visual updates using composition patterns

## Architecture Decisions

### Decision: CSS Token Strategy

**Choice**: Extend existing CSS custom properties with new gradient and shadow tokens, keeping all existing Blue & Noir variables intact.

**Alternatives considered:**
- Create entirely new CSS variable prefix (e.g., `--modern-*`)
- Use Tailwind 4 `@theme` exclusively for new tokens

**Rationale**: The existing codebase already has a well-defined color system (--primary, --secondary, --accent, etc.). Adding gradient and shadow tokens maintains backward compatibility and allows gradual migration. Using `@theme` for Tailwind integration while keeping custom properties ensures shadcn/ui components continue working.

---

### Decision: Glassmorphism Implementation

**Choice**: Use Tailwind's `backdrop-blur` + semi-transparent backgrounds with CSS custom properties for opacity control.

**Alternatives considered:**
- Pre-defined glassmorphism utility classes
- CSS-only solution via custom classes

**Rationale**: Tailwind's native backdrop utilities provide GPU-accelerated blur via CSS filters. Using CSS variables for opacity allows fine-tuned control for light/dark modes without duplicating styles.

---

### Decision: Button Variant Strategy

**Choice**: Add new `gradient` and `glass` variants via CVA, keeping all existing variants functional.

**Alternatives considered:**
- Replace existing variants entirely
- Create separate ButtonGradient component

**Rationale**: The existing `retro` variant should remain for backward compatibility (per proposal scope). Adding new variants via CVA composition is the standard shadcn/ui pattern and allows gradual adoption.

---

### Decision: Card Shadow Migration

**Choice**: Replace `border-4 border-foreground flat-shadow` with `shadow-lg` and subtle borders.

**Alternatives considered:**
- Keep flat-shadow as a variant
- Use shadow-xl for all cards

**Rationale**: The spec requires replacing flat-shadow with elegant shadows. Using `shadow-lg` provides the right balance of depth without being dramatic. A subtle border can be added for definition where needed.

---

### Decision: Focus Ring Gradient

**Choice**: Use CSS `box-shadow` with gradient for input focus states, applied via Tailwind's `focus-visible` variant.

**Alternatives considered:**
- Gradient border using `border-image`
- Pseudo-element gradient overlay

**Rationale**: `box-shadow` is performant and works with existing focus-visible patterns. Using a subtle gradient ring maintains accessibility while achieving the gradient effect.

---

## Data Flow

```
globals.css (design tokens)
    │
    ├── Gradient tokens ──────► Button (gradient variant)
    │                            Card (shadow-lg)
    │                            Input (focus ring)
    │
    ├── Glassmorphism tokens ──► Sidebar
    │                            Sheet
    │                            Navbar
    │
    └── Mesh gradient ─────────► Landing Hero
                                  Dashboard backgrounds
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `apps/frontend/src/app/globals.css` | Modify | Add gradient tokens, glassmorphism utilities, mesh background |
| `apps/frontend/src/components/ui/button.tsx` | Modify | Add `gradient` and `glass` variants via CVA |
| `apps/frontend/src/components/ui/card.tsx` | Modify | Replace flat-shadow with shadow-lg, add gradient prop support |
| `apps/frontend/src/components/ui/input.tsx` | Modify | Add gradient focus ring via box-shadow |
| `apps/frontend/src/components/ui/sidebar.tsx` | Modify | Add glassmorphism classes to container |
| `apps/frontend/src/components/ui/sheet.tsx` | Modify | Add glassmorphism to SheetContent and overlay |
| `apps/frontend/src/components/landing/hero-section.tsx` | Modify | Add gradient mesh background |
| `apps/frontend/src/components/landing/features-section.tsx` | Modify | Update cards with gradient styling |
| `apps/frontend/src/components/landing/nav-landing.tsx` | Modify | Add glassmorphism to navbar |
| `apps/frontend/src/components/dashboard/section-cards.tsx` | Modify | Update metric cards with gradients |
| `apps/frontend/src/components/dashboard/app-sidebar.tsx` | Modify | Ensure glassmorphism via sidebar component |

## Interfaces / Contracts

### New CSS Custom Properties

```css
/* Gradient tokens - to be added to :root and .dark */
--gradient-subtle: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
--gradient-mesh-1: #1e40af;
--gradient-mesh-2: #3b82f6;
--gradient-mesh-3: #0a0a0a;

/* Glassmorphism tokens */
--glass-bg: rgba(255, 255, 255, 0.1);
--glass-border: rgba(255, 255, 255, 0.2);
--glass-blur: 12px;

/* Shadow tokens (using Tailwind's built-in shadow-lg, shadow-xl) */
```

### Button Variant Schema

```typescript
// New variants to add to buttonVariants CVA
variant: {
  // ... existing variants
  gradient: "bg-gradient-to-r from-primary to-blue-500 text-primary-foreground shadow-lg hover:shadow-xl hover:from-primary/90 hover:to-blue-500/90",
  glass: "bg-glass text-foreground backdrop-blur-md border border-glass-border hover:bg-glass/80",
}
```

### Card Component API

```typescript
// Optional prop for gradient cards
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  gradient?: boolean;  // New: enables gradient background
  glass?: boolean;     // New: enables glassmorphism
}
```

### Input Focus Ring

```css
/* Gradient focus ring - added to Input component */
focus-visible:ring-2 focus-visible:ring-primary/50 focus-visible:ring-offset-2
/* OR using box-shadow for gradient */
focus-visible:shadow-[0_0_0_2px_var(--background),0_0_0_4px_var(--primary)]
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Visual | Gradient backgrounds render correctly in light/dark | Manual verification + screenshot diffs |
| Visual | Glassmorphism effects visible on sidebar/sheet | Manual verification |
| Functional | All existing button variants still work | Component storybook or manual |
| Functional | Input focus states work with keyboard | Accessibility test |
| Performance | Animations run at 60fps | Chrome DevTools Performance tab |
| Responsive | Works on mobile, tablet, desktop | Responsive preview |

## Migration / Rollout

**No database migration required** — this is a purely visual change.

**Phased Rollout:**
1. **Phase 1**: Update `globals.css` with new design tokens (safe, backward compatible)
2. **Phase 2**: Add button variants (backward compatible additions)
3. **Phase 3**: Update Card and Input components (may affect existing usages)
4. **Phase 4**: Apply glassmorphism to Sidebar and Sheet
5. **Phase 5**: Landing page gradient mesh
6. **Phase 6**: Dashboard metric cards

**Rollback:**
Each phase can be reverted by:
1. Removing added CSS tokens from globals.css
2. Removing new CVA variants from button.tsx
3. Restoring Card/Input to previous styling
4. Removing glassmorphism classes from Sidebar/Sheet
5. Reverting landing/dashboard components

## Open Questions

- [ ] Should the `retro` variant be deprecated or maintained indefinitely?
- [ ] Should gradient mesh use CSS-only or include subtle animated movement?
- [ ] Should metric cards include hover elevation animations?
