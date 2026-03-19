# Delta for Frontend UI - Dashboard Sidebar Navigation

## ADDED Requirements

### Requirement: Dashboard Sidebar Navigation Structure

The dashboard sidebar MUST display a labeled "Estadísticas" section (NavMain) above its menu items.

The system MUST replace the "Documents" section (NavDocuments) with a new section titled "Gestión de Juegos y Niveles".

The new section MUST contain two navigation items:

1. "Niveles" linking to `/dashboard/levels`
2. "Crear Nivel" linking to `/dashboard/levels/create`

All UI text MUST remain in Spanish.

The system MUST use Tailwind's `cn()` utility for class composition (no `var()` in className).

The system MUST use TypeScript strict mode (no `any` types).

#### Scenario: Admin Views Dashboard Sidebar

- GIVEN an admin user is logged into the dashboard
- WHEN the sidebar is rendered
- THEN the sidebar displays a section labeled "Estadísticas" with its menu items
- AND a second section labeled "Gestión de Juegos y Niveles" with two menu items: "Niveles" and "Crear Nivel"

#### Scenario: Admin Clicks "Niveles" Link

- GIVEN the admin is viewing the dashboard sidebar
- WHEN the admin clicks the "Niveles" menu item
- THEN the browser navigates to `/dashboard/levels`
- AND the levels page loads successfully

#### Scenario: Admin Clicks "Crear Nivel" Link

- GIVEN the admin is viewing the dashboard sidebar
- WHEN the admin clicks the "Crear Nivel" menu item
- THEN the browser navigates to `/dashboard/levels/create`
- AND the create level page loads successfully

#### Scenario: Sidebar Maintains Existing Navigation

- GIVEN the dashboard sidebar is rendered
- WHEN the sidebar is displayed
- THEN existing navigation sections (NavSecondary, NavUser) remain unchanged
- AND no visual regression occurs

### Requirement: Navigation Component Implementation

The system MUST implement a new navigation component for game/level management section (or reuse existing NavDocuments component with modified label and items).

The NavMain component MUST accept an optional `label` prop (default empty string) and render a `SidebarGroupLabel` when provided.

The system MUST update the AppSidebar component to:

1. Import the new navigation component (or modified NavDocuments)
2. Replace `<NavDocuments items={data.documents} />` with the new component
3. Remove the `documents` data array or keep unused

The system MUST export the new component from the shared navigation index.

#### Scenario: NavMain Component with Label

- GIVEN the NavMain component is rendered with a label prop set to "Estadísticas"
- WHEN the component mounts
- THEN it displays a SidebarGroupLabel with the text "Estadísticas" above its menu items

#### Scenario: NavMain Component without Label

- GIVEN the NavMain component is rendered without a label prop
- WHEN the component mounts
- THEN no label is displayed above its menu items

#### Scenario: Game Management Component Rendering

- GIVEN the game management component is rendered
- WHEN the component mounts
- THEN it displays a sidebar group with label "Gestión de Juegos y Niveles"
- AND shows two menu items: "Niveles" and "Crear Nivel"

### Requirement: Accessibility and Visual Consistency

The system MUST maintain visual consistency with existing sidebar sections (same styling, spacing, icons).

The system MUST ensure navigation items have appropriate hover and active states.

The system MUST provide accessible labels for navigation items (aria-labels where needed).

#### Scenario: Navigation Item Hover State

- GIVEN a navigation item in the sidebar
- WHEN the user hovers over the item
- THEN the item displays a hover state (background color change)
- AND the transition is smooth

#### Scenario: Active Navigation Item

- GIVEN the user is on a page linked from a sidebar navigation item
- WHEN the sidebar is rendered
- THEN the corresponding navigation item is visually highlighted as active

## MODIFIED Requirements

### Requirement: Sidebar Component (Existing)

The sidebar component MUST include the new navigation sections as described above.

(Previously: The sidebar component displayed a "Documents" section with placeholder links)

#### Scenario: Updated Sidebar Structure

- GIVEN the dashboard page with sidebar
- WHEN the sidebar is rendered
- THEN it no longer displays a "Documents" section
- AND it displays the new "Gestión de Juegos y Niveles" section

## REMOVED Requirements

### Requirement: Documents Section (NavDocuments)

The "Documents" section with placeholder links is removed from the dashboard sidebar.

(Reason: The section was irrelevant to the application's purpose of game/level management and confused users.)