# Delta for Frontend

## ADDED Requirements

### Requirement: Consistent Auth Page Layout

Both login and signup pages SHALL use a centered, single-column layout without lateral images.

#### Scenario: Login page centered layout

- GIVEN the login page is rendered
- THEN the form is centered vertically and horizontally
- AND the form has a maximum width of `max-w-sm`
- AND the page includes the logo and branding at the top
- AND the background uses the `retro-grid scanlines` pattern

#### Scenario: Signup page centered layout

- GIVEN the signup page is rendered
- THEN the form is centered vertically and horizontally
- AND the lateral image panel is NOT present
- AND the form has a maximum width of `max-w-sm` or `max-w-xs`
- AND the page includes the logo and branding at the top
- AND the layout matches the login page structure for consistency

### Requirement: Password Requirements Indicator Component

The signup form SHALL include a visual component showing password requirements with checkmark/X icons.

#### Scenario: Requirements list appearance

- GIVEN a password field in the signup form
- WHEN the user focuses the password field
- THEN a list of requirements appears with icons
- AND each requirement has a red X icon initially
- AND the list includes: "Al menos 8 caracteres", "Al menos una mayúscula", "Al menos una minúscula", "Al menos un número"

#### Scenario: Requirements validation on input

- GIVEN a user is typing in the password field
- WHEN a requirement is met
- THEN the icon changes from red X to green checkmark
- AND the requirement text changes color to success state
- AND the validation updates in real-time (on every change event)

## MODIFIED Requirements

### Requirement: Signup Page Structure

The signup page SHALL NOT include a lateral image panel on desktop viewports.

(Previously: Signup page had a two-column layout with form on left and image on right for lg: screens)

#### Scenario: Signup page without image

- GIVEN the signup page is viewed on any screen size
- THEN the page displays only the form in a centered layout
- AND no `<Image>` component is rendered for decorative purposes
- AND the page structure matches the login page layout pattern

### Requirement: Password Toggle Button Accessibility

Password toggle buttons SHALL have descriptive `aria-label` attributes in Spanish.

(Previously: Some toggle buttons lacked aria-labels, making them inaccessible to screen readers)

#### Scenario: Toggle button accessible in signup

- GIVEN a user navigates with a screen reader
- WHEN the password toggle button receives focus
- THEN the screen reader announces "Mostrar contraseña" or "Ocultar contraseña" based on current state
- AND the button has `type="button"` to prevent form submission
- AND the button has proper focus ring styling per design system

## REMOVED Requirements

### Requirement: Lateral Image Panel in Signup

(Reason: Simplifying layout to match login page, removing maintenance burden of managing two different auth page layouts, and focusing on design system consistency)
