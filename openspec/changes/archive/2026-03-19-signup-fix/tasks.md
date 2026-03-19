# Tasks: Corrección de la Funcionalidad de Registro

## Phase 1: Foundation / Infrastructure

- [x] 1.1 Analyze current signup-form.tsx structure to understand existing form state and validation flow
- [x] 1.2 Add local state hooks for password visibility: `showPassword` and `showConfirmPassword` initialized to false
- [x] 1.3 Import required icons from lucide-react (`Eye` and `EyeOff`) for password toggle functionality

## Phase 2: Core Implementation

- [x] 2.1 Modify password input field to wrap in relative div with toggle button implementation
- [x] 2.2 Implement password visibility toggle functionality: onClick handler to toggle `showPassword` state
- [x] 2.3 Modify confirm password input field similarly with its own toggle button and `showConfirmPassword` state
- [x] 2.4 Implement dynamic input type switching between "password" and "text" based on visibility state
- [x] 2.5 Add accessible aria-labels to toggle buttons: "Mostrar contraseña" and "Ocultar contraseña"
- [x] 2.6 Refactor form state management to use controlled components for all fields to preserve values
- [x] 2.7 Modify validation error display to show field-specific errors instead of consolidated errors
- [x] 2.8 Implement logic to preserve valid field values when form submission fails with partial errors
- [x] 2.9 Ensure aria-invalid attributes are set per-field based on validation errors

## Phase 3: Integration / Wiring

- [x] 3.1 Verify integration with existing `signupAction` and `useActionState` hooks
- [x] 3.2 Test that backend duplicate prevention still works correctly with frontend changes
- [x] 3.3 Confirm that form submission flow remains unchanged: validation → API call → success/error handling
- [x] 3.4 Verify that visual styling remains consistent with existing shadcn/ui components
- [x] 3.5 Test that toast notifications and redirect behavior work correctly with new implementation

## Phase 4: Testing / Verification

- [x] 4.1 Write unit tests for password visibility toggle functionality
- [x] 4.2 Write unit tests for field-level validation preservation
- [x] 4.3 Write unit tests for field-specific error message display
- [x] 4.4 Test scenario: valid name/username/email with mismatched passwords - verify valid fields preserve values
- [x] 4.5 Test scenario: invalid email format - verify error shows only under email field
- [x] 4.6 Test scenario: duplicate email/username - verify backend error is displayed appropriately
- [x] 4.7 Test accessibility: verify aria-label functionality and keyboard navigation
- [x] 4.8 Test edge cases: rapid toggling, form reset behavior, etc.

## Phase 5: Cleanup / Documentation

- [x] 5.1 Remove any temporary code or console logs added during development
- [x] 5.2 Ensure all imports are necessary and used
- [x] 5.3 Verify component follows existing code style and conventions
- [x] 5.4 Update any relevant comments to reflect new functionality