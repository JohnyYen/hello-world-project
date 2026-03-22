# Settings Domain Specification

## Purpose

This specification describes the settings persistence layer for teacher preferences, covering bidirectional synchronization between the Next.js frontend and FastAPI backend. It defines requirements for GET/PUT operations, theme dual-sync, field mapping, and default values for all settings fields displayed in the settings UI.

## Requirements

### Requirement: GET Settings Returns All Fields

The system MUST return all settings fields when a teacher requests their configuration.

The API endpoint `GET /settings` SHALL return a complete settings object containing: `theme`, `notificationsEnabled`, `notificationFrequency`, `interfaceLanguage`, `autoLogout`, `sessionDurationMinutes`, `rememberLogin`, `colorTheme`, `animationsEnabled`, `emailNotifications`, `dateFormat`, and `timezone`.

#### Scenario: Fetch all settings for authenticated teacher

- GIVEN a teacher is authenticated and has existing settings stored in the database
- WHEN the teacher navigates to the settings page
- THEN the system returns all 12 fields with their stored values
- AND each field reflects the last saved configuration

#### Scenario: Fetch settings for teacher with no existing record

- GIVEN a teacher is authenticated but has no settings record in the database
- WHEN the system receives a GET request for settings
- THEN the system creates a default settings record for that teacher
- AND returns all fields with their default values

#### Scenario: Settings response includes all expanded fields

- GIVEN a teacher with full settings configured (session, appearance, notifications, language)
- WHEN GET /settings is called
- THEN the response includes `autoLogout`, `sessionDurationMinutes`, `rememberLogin`, `colorTheme`, `animationsEnabled`, `emailNotifications`, `dateFormat`, and `timezone`
- AND the response includes all existing fields: `theme`, `notificationsEnabled`, `notificationFrequency`, `interfaceLanguage`

---

### Requirement: PUT Settings Persists All Fields

The system MUST accept and persist all settings fields submitted through the PUT endpoint.

The API endpoint `PUT /settings` SHALL accept a payload containing any subset of settings fields and persist only the provided fields while preserving unchanged fields.

#### Scenario: Save complete settings update

- GIVEN a teacher modifies multiple settings (theme, notifications, session duration, date format)
- WHEN the teacher clicks "Guardar Cambios"
- THEN all modified fields are persisted to the database
- AND unchanged fields retain their previous values
- AND the response returns the complete updated settings object

#### Scenario: Save partial settings update

- GIVEN a teacher modifies only the `animationsEnabled` toggle
- WHEN the teacher submits the update
- THEN only `animationsEnabled` is updated in the database
- AND all other fields remain unchanged
- AND the response reflects the complete settings state

#### Scenario: Backend validates all new fields

- GIVEN a PUT request with `sessionDurationMinutes: 0`
- WHEN the request is processed
- THEN the backend validates the value (integer, 0 = permanent session)
- AND persists the value correctly
- AND returns success response

#### Scenario: Backend rejects invalid date format

- GIVEN a PUT request with `dateFormat: "invalid"`
- WHEN the request is validated
- THEN the backend rejects the value
- AND returns a 422 validation error
- AND no fields are updated

---

### Requirement: Theme Dual-Sync (useTheme + Backend Persistence)

The system MUST maintain theme state in two synchronized layers: the `useTheme` hook for immediate client-side experience and the backend for cross-device persistence.

The frontend SHALL apply theme changes immediately via `useTheme` (next-themes) and SHALL persist the theme to the backend asynchronously without blocking the UI.

The frontend SHALL initialize `useTheme` with the theme value from the backend on page load.

#### Scenario: Theme applied immediately on toggle

- GIVEN a teacher is on the settings page
- WHEN the teacher toggles the dark mode switch
- THEN the UI theme changes immediately (no loading delay)
- AND the new theme is persisted to the backend in the background

#### Scenario: Theme restored from backend on page load

- GIVEN a teacher previously set their theme to "dark"
- WHEN the teacher reloads the settings page
- THEN `useTheme` is initialized with "dark" from the backend response
- AND the UI renders in dark mode immediately (no flash)

#### Scenario: Theme persisted even if other settings fail

- GIVEN a teacher changes theme to "dark"
- AND the subsequent PUT request for all settings fails due to a network error
- WHEN the system retries the save
- THEN the theme preference is included in the retry payload
- AND the theme change is not lost

---

### Requirement: notification_frequency Mapping Fix

The system MUST display "En tiempo real" for the `realtime` value of `notificationFrequency` in the UI select dropdown.

The backend SHALL store `notificationFrequency` values as `realtime`, `daily`, `weekly`, and `disabled` (not `instant`).

The frontend SHALL display human-readable labels in Spanish for each value.

#### Scenario: Display "En tiempo real" for realtime frequency

- GIVEN a teacher has `notificationFrequency` set to `realtime`
- WHEN the settings page loads
- THEN the "Frecuencia de Resumen" dropdown shows "En tiempo real" as selected
- AND the API stores and returns `realtime` (not `instant`)

#### Scenario: Backend accepts only valid frequency values

- GIVEN a PUT request with `notificationFrequency: "instant"`
- WHEN the backend validates the payload
- THEN the backend normalizes `instant` to `realtime` OR
- AND the backend accepts `instant` as a valid alias for `realtime`
- AND the response returns `realtime`

#### Scenario: All notification frequency options displayed in Spanish

- GIVEN a teacher is viewing the notification frequency dropdown
- WHEN the dropdown is opened
- THEN the options displayed are: "En tiempo real", "Diario", "Semanal", "Desactivado"
- AND the backend values are: `realtime`, `daily`, `weekly`, `disabled`

---

### Requirement: "Guardar Cambios" Button Is Functional

The system MUST wire the "Guardar Cambios" button to persist all current settings state to the backend.

The button SHALL collect all current form state, submit via PUT /settings, and display success or error feedback.

#### Scenario: Save button triggers PUT request

- GIVEN a teacher has modified multiple settings (auto_logout, color_theme, date_format)
- WHEN the teacher clicks "Guardar Cambios"
- THEN a PUT request is sent to `/settings` with all current form values
- AND a loading state is shown on the button during the request

#### Scenario: Save button shows success feedback

- GIVEN a teacher clicks "Guardar Cambios"
- AND the PUT request succeeds (200 response)
- THEN the button shows a success indicator (checkmark or "Guardado")
- AND the button returns to normal state after 2 seconds
- AND a toast notification confirms "Configuración guardada exitosamente"

#### Scenario: Save button shows error feedback

- GIVEN a teacher clicks "Guardar Cambios"
- AND the PUT request fails (network error or 500)
- THEN the button shows an error state
- AND a toast notification displays "Error al guardar la configuración"
- AND the form data is NOT lost (remains populated)

#### Scenario: Save button is disabled during request

- GIVEN a teacher clicks "Guardar Cambios"
- AND the request is in progress
- WHEN the teacher clicks the button again
- THEN the button is disabled and shows a spinner
- AND no duplicate request is sent

---

### Requirement: Default Values for New Settings Fields

The system MUST initialize new settings fields with sensible defaults when creating a new TeacherSettings record.

New users SHALL receive defaults that provide a good out-of-box experience matching the existing UI defaults.

#### Scenario: New teacher settings get correct defaults

- GIVEN a new teacher account is created
- WHEN the teacher logs in for the first time
- THEN `autoLogout` defaults to `false`
- AND `sessionDurationMinutes` defaults to `60`
- AND `rememberLogin` defaults to `true`
- AND `colorTheme` defaults to `"Indigo"`
- AND `animationsEnabled` defaults to `true`
- AND `emailNotifications` defaults to `false`
- AND `dateFormat` defaults to `"ddmmyyyy"`
- AND `timezone` defaults to `"America/Bogota"` (or closest UTC offset)

#### Scenario: Existing teachers retain their existing field values

- GIVEN a teacher already has settings with `theme`, `notificationsEnabled`, `notificationFrequency`, `interfaceLanguage`
- WHEN a migration adds the new columns with defaults
- THEN the existing records are NOT affected
- AND existing teachers see their original values for existing fields

#### Scenario: Existing teachers get defaults for new fields

- GIVEN a teacher with existing settings (before migration)
- WHEN the teacher logs in after migration adds new fields
- THEN the new fields are populated with default values
- AND the teacher does NOT lose any existing field values

---

### Requirement: Backend Schema Supports All New Fields

The backend MUST define Pydantic schemas and SQLAlchemy model fields for all new settings.

The TeacherSettingsUpdate schema SHALL accept optional fields for: `autoLogout`, `sessionDurationMinutes`, `rememberLogin`, `colorTheme`, `animationsEnabled`, `emailNotifications`, `dateFormat`, `timezone`.

The TeacherSettingsResponse schema SHALL return all fields with defaults.

#### Scenario: Backend accepts new fields in PUT request

- GIVEN a request body with `colorTheme: "Violeta"` and `sessionDurationMinutes: 30`
- WHEN the PUT endpoint processes the request
- THEN both fields are accepted and persisted
- AND the response includes all original fields plus the new ones

#### Scenario: Backend omits null fields from response

- GIVEN a PUT request that only sends `colorTheme: "Esmeralda"`
- WHEN the response is generated
- THEN only the modified fields reflect the change
- AND other fields show their stored values (not null)

---

### Requirement: API Client Supports All New Fields

The TypeScript API client (packages/api-client-ts) MUST include types and methods for all new settings fields.

The TeacherSettingsUpdate interface SHALL include all new optional fields with camelCase naming.

The TeacherSettingsResponse interface SHALL include all new fields.

#### Scenario: API client type includes new fields

- GIVEN the API client is imported in a frontend component
- WHEN the component defines a settings update payload
- THEN TypeScript accepts an object with `colorTheme`, `sessionDurationMinutes`, `autoLogout`, etc.

#### Scenario: API client serializes new fields correctly

- GIVEN a settings update object with `sessionDurationMinutes: 45`
- WHEN the payload is sent to the backend
- THEN the JSON contains `session_duration_minutes: 45` (snake_case for API)

---

### Requirement: Zod Validation on Frontend

The frontend SHALL validate settings form data with Zod schemas before submission.

The validation SHALL ensure `sessionDurationMinutes` is a non-negative integer, `colorTheme` is one of the allowed values, and `dateFormat` matches allowed patterns.

#### Scenario: Frontend rejects invalid session duration

- GIVEN a teacher enters a negative value for session duration
- WHEN the form is validated before submission
- THEN the frontend shows a validation error
- AND the PUT request is NOT sent

#### Scenario: Frontend validates date format options

- GIVEN the date format select options are limited to `ddmmyyyy`, `mmddyyyy`, `yyyymmdd`
- WHEN the form is submitted
- THEN the frontend validates the value matches one of the allowed options

---

## Acceptance Criteria

### API Backend

- [ ] GET /settings returns all 12 fields (4 existing + 8 new)
- [ ] PUT /settings accepts and persists all 12 fields
- [ ] `notificationFrequency` values normalized to `realtime`, `daily`, `weekly`, `disabled`
- [ ] Pydantic schemas updated with new fields
- [ ] SQLAlchemy model includes new columns with defaults
- [ ] Alembic migration created for new columns

### API Client (TypeScript)

- [ ] TeacherSettingsUpdate interface includes all new fields
- [ ] TeacherSettingsResponse interface includes all new fields
- [ ] Field mapping (camelCase ↔ snake_case) works for all fields

### Frontend Settings Page

- [ ] "Guardar Cambios" button triggers PUT request with all form state
- [ ] Success toast displayed on successful save
- [ ] Error handling with error toast on failure
- [ ] Loading state on button during save operation
- [ ] Button disabled during in-flight request

### Theme Dual-Sync

- [ ] `useTheme` initialized with value from backend on page load
- [ ] Theme toggle changes UI immediately
- [ ] Theme change persisted to backend asynchronously
- [ ] No theme flash on page reload

### Defaults

- [ ] New TeacherSettings records get correct defaults for all 8 new fields
- [ ] Existing records unaffected by migration
- [ ] UI selects show correct initial values from backend

### UI Text

- [ ] All labels and messages in Spanish
- [ ] "En tiempo real" displayed for `realtime` notification frequency
- [ ] "Guardar Cambios" button text in Spanish
