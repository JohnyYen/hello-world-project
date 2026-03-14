# Frontend Design Specification - Blue & Noir Redesign

## Purpose

This specification defines the visual design system for the Hello World Frontend application, transitioning from a retro/vintage aesthetic (flat-shadow, prominent borders, scanlines) to a modern minimalist design with subtle gradients, elegant shadows, and glassmorphism effects while maintaining the existing Blue & Noir color palette.

## Requirements

### Requirement: CSS Design Tokens

The system MUST define new CSS custom properties for:

- Gradient backgrounds for light and dark modes (subtle, not dramatic)
- Elegant shadow values (replacing flat-shadow)
- Glassmorphism effect properties (backdrop-blur, opacity)
- Gradient mesh background utilities
- Focus ring styles with gradient

The system SHALL maintain backward compatibility with existing color tokens (--primary, --secondary, --accent, etc.).

The system SHOULD use CSS transforms for performance optimization.

#### Scenario: Light Mode Gradient Background

- GIVEN the user visits the application in light mode
- WHEN the page loads
- THEN the background displays a subtle gradient mesh using the defined gradient tokens
- AND the gradient does not distract from content readability

#### Scenario: Dark Mode Gradient Background

- GIVEN the user visits the application in dark mode
- WHEN the page loads
- THEN the background displays a subtle gradient that complements the noir palette
- AND the gradient provides visual depth without being dramatic

#### Scenario: Glassmorphism Sidebar

- GIVEN the user views the dashboard sidebar
- WHEN the sidebar is rendered
- THEN it displays a frosted glass effect with backdrop-blur
- AND semi-transparent background that reveals content behind it subtly
- AND maintains text readability

---

### Requirement: Button Component

The button component MUST support a new "gradient" variant that:

- Uses subtle gradient background (not flat colors)
- Applies elegant shadow-lg instead of flat-shadow
- Maintains hover and active states with smooth transitions
- Supports both light and dark mode appearances

The system SHALL preserve existing button variants (default, secondary, outline, ghost, destructive) for backward compatibility.

#### Scenario: Gradient Button in Light Mode

- GIVEN a button with variant="gradient" in light mode
- WHEN rendered
- THEN displays subtle blue gradient background
- AND has shadow-lg with soft edges
- AND text remains readable (contrast ratio >= 4.5:1)

#### Scenario: Gradient Button in Dark Mode

- GIVEN a button with variant="gradient" in dark mode
- WHEN rendered
- THEN displays adjusted gradient for dark background visibility
- AND maintains the same shadow characteristics

#### Scenario: Legacy Button Variants Still Work

- GIVEN existing buttons using default, secondary, or destructive variants
- WHEN rendered after the redesign
- THEN they display without the flat-shadow effect
- AND maintain visual consistency with new gradient buttons

---

### Requirement: Card Component

The card component MUST:

- Replace flat-shadow with shadow-lg (elegant shadows)
- Support subtle gradient backgrounds as an optional style
- Maintain existing props and API (children, className, etc.)
- Work correctly in both light and dark modes

#### Scenario: Card with Default Styling

- GIVEN a Card component with default props
- WHEN rendered in light mode
- THEN displays white background with shadow-lg
- AND border is subtle or removed for cleaner look

#### Scenario: Card with Gradient Style

- GIVEN a Card component with gradient={true}
- WHEN rendered
- THEN displays a subtle gradient background
- AND maintains shadow-lg for depth

---

### Requirement: Input Component

The input component MUST:

- Implement focus ring with gradient effect
- Maintain existing functionality (onChange, value, placeholder, etc.)
- Support both light and dark mode focus states
- Pass accessibility requirements for focus indicators

#### Scenario: Input Focus State

- GIVEN an Input component
- WHEN the user focuses the input (tab or click)
- THEN displays a gradient ring around the input
- AND the ring is visible and meets WCAG focus requirements

---

### Requirement: Sidebar Component

The sidebar component MUST:

- Apply glassmorphism effect (backdrop-blur)
- Use semi-transparent background with bg-opacity
- Maintain navigation functionality
- Support collapsible state
- Work in both light and dark modes

#### Scenario: Glassmorphism Sidebar in Dashboard

- GIVEN the dashboard page with a sidebar
- WHEN rendered in dark mode
- THEN sidebar displays frosted glass effect
- AND content behind it is subtly visible
- AND navigation items remain fully readable

#### Scenario: Sidebar Collapse Animation

- GIVEN the sidebar is expanded
- WHEN user clicks collapse button
- THEN sidebar animates smoothly to collapsed state
- AND glassmorphism effect is maintained throughout animation

---

### Requirement: Sheet Component

The sheet component (slide-out panel) MUST:

- Apply glassmorphism effect matching the sidebar
- Maintain existing open/close animations
- Support all positions (top, right, bottom, left)
- Work correctly with focus trap

#### Scenario: Sheet Glassmorphism

- GIVEN a Sheet component in open state
- WHEN rendered
- THEN displays with glassmorphism background
- AND overlay behind sheet is blurred

---

### Requirement: Landing Page Design

The landing page MUST implement:

- Hero section with gradient mesh background
- Feature cards with subtle gradient styling
- Navbar with glassmorphism effect
- Responsive design for mobile, tablet, and desktop

#### Scenario: Landing Page Hero Gradient Mesh

- GIVEN the landing page
- WHEN the hero section loads
- THEN displays a gradient mesh background using CSS
- AND the mesh uses Blue & Noir color palette
- AND text content remains readable

#### Scenario: Feature Cards

- GIVEN the features section on landing page
- WHEN cards are rendered
- THEN each card displays with subtle gradient background
- AND shadow-lg for depth
- AND hover effect with slight elevation change

---

### Requirement: Dashboard Design

The dashboard MUST implement:

- Metric cards with gradient and elegant shadows
- Glassmorphism sidebar (same as standalone sidebar)
- Visual improvement for charts and tables
- Consistent styling with landing page

#### Scenario: Metric Cards Display

- GIVEN dashboard metric cards
- WHEN rendered
- THEN each card shows subtle gradient background
- AND displays shadow-lg for elegant depth
- AND value text is prominent and readable

#### Scenario: Dashboard Sidebar Glassmorphism

- GIVEN the dashboard sidebar
- WHEN rendered
- THEN matches the glassmorphism specification from sidebar requirement
- AND integrates visually with the metric cards

---

### Requirement: Theme Mode Support

The system MUST:

- Support light and dark modes via Tailwind's dark: variant
- Provide gradient adjustments for each mode
- Ensure all glassmorphism effects work in both modes
- Persist user preference (if theme toggle exists)

#### Scenario: Light to Dark Mode Toggle

- GIVEN the application in light mode
- WHEN user toggles to dark mode
- THEN all gradients, shadows, and glassmorphism adapt appropriately
- AND no visual glitches occur during transition

---

### Requirement: Performance

The system SHOULD:

- Use CSS transforms for animations (GPU acceleration)
- Avoid heavy blur values (>20px backdrop-blur)
- Use will-change sparingly for animated elements
- Test performance on mid-range devices

#### Scenario: Glassmorphism Performance

- GIVEN glassmorphism effects on sidebar and sheets
- WHEN page scrolls or animates
- THEN animations remain smooth (60fps)
- AND no jank or frame drops on standard hardware

---

## Acceptance Criteria

### CSS Design Tokens

- [ ] New gradient CSS variables defined in :root and .dark
- [ ] Shadow tokens updated (shadow-lg, shadow-xl added)
- [ ] Glassmorphism utility classes available
- [ ] Focus ring with gradient implemented

### Components

- [ ] Button component has new gradient variant
- [ ] Card component uses shadow-lg (no flat-shadow)
- [ ] Input component has gradient focus ring
- [ ] Sidebar displays glassmorphism effect
- [ ] Sheet displays glassmorphism effect

### Pages

- [ ] Landing page hero has gradient mesh background
- [ ] Feature cards have subtle gradient styling
- [ ] Navbar has glassmorphism effect
- [ ] Dashboard metric cards display gradients
- [ ] Dashboard sidebar has glassmorphism

### Mode Support

- [ ] Light mode displays correctly with all new styles
- [ ] Dark mode displays correctly with all new styles
- [ ] Theme toggle transitions smoothly

### UI Text

- [ ] All UI text remains in Spanish

### Quality

- [ ] No console errors related to new styles
- [ ] Responsive design works on mobile, tablet, desktop
- [ ] Accessibility: focus indicators visible
- [ ] Performance: smooth animations (no jank)
