# Auth Specification

## Purpose

This specification describes the authentication-related functionality for login and signup forms, including password visibility toggling, field-level validation, error message display, Server Action integration, accessibility requirements, and Spanish localization.

## Requirements

### Requirement: Password Visibility Toggle

The system MUST allow users to toggle the visibility of password fields on both login and signup forms to improve usability.

#### Scenario: Toggle password visibility on click (Login Form)

- GIVEN a user is viewing the password field in the login form
- WHEN the user clicks the eye icon toggle button
- THEN the password field type changes from "password" to "text"
- AND the eye icon changes to EyeOff to indicate visibility is ON
- AND the button has an aria-label in Spanish ("Mostrar contraseña")

#### Scenario: Toggle password visibility off on second click (Login Form)

- GIVEN a user has toggled password visibility ON in the login form
- WHEN the user clicks the eye icon toggle button again
- THEN the password field type changes from "text" to "password"
- AND the eye icon changes back to Eye
- AND the button aria-label changes to "Ocultar contraseña"

#### Scenario: Independent toggle for password and confirm password fields (Signup Form)

- GIVEN a user is viewing both password and confirm password fields in the signup form
- WHEN the user toggles visibility for the password field only
- THEN only the password field visibility changes
- AND the confirm password field visibility remains unchanged

#### Scenario: Password field returns to hidden on form submission

- GIVEN a user has toggled password visibility to visible
- WHEN the user submits the login or signup form
- THEN the password field type resets to "password" on next render

### Requirement: Real-Time Password Requirements Validation

The signup form MUST display visual feedback for password requirements as the user types.

#### Scenario: Password requirements displayed as checklist

- GIVEN a user is filling the password field in the signup form
- WHEN the password field receives focus
- THEN a requirements checklist appears below the field
- AND each requirement shows a red X icon initially (unchecked state)
- AND the requirements are: "Al menos 8 caracteres", "Al menos una mayúscula", "Al menos una minúscula", "Al menos un número"

#### Scenario: Requirement met shows visual feedback

- GIVEN a user is typing a password
- WHEN the password meets a specific requirement (e.g., 8+ characters)
- THEN that requirement shows a green checkmark icon
- AND the requirement text changes to a success color

#### Scenario: All requirements met

- GIVEN a user has entered a password meeting all requirements
- THEN all requirements show green checkmarks
- AND the password field has no validation error styling

### Requirement: Accessible Loading State Announcement

The login and signup forms MUST announce loading states to assistive technologies.

#### Scenario: Loading state announced on form submission

- GIVEN a user submits the login or signup form
- WHEN the form action is processing
- THEN the submit button text changes to "Iniciando sesión..." or "Creando cuenta..."
- AND the submit button is disabled
- AND the button has aria-live="polite" attribute

#### Scenario: Loading state cleared on completion

- GIVEN a form is in loading state
- WHEN the action completes (success or error)
- THEN the button text returns to normal state
- AND the submit button is re-enabled

### Requirement: Login Form Server Action Integration

The login form SHALL use the `loginAction` Server Action via `useActionState` instead of direct fetch calls.

#### Scenario: Login form uses Server Action

- GIVEN a user fills in email and password
- WHEN the user submits the login form
- THEN the form calls `loginAction` via the action prop
- AND the form does NOT use fetch or XMLHttpRequest directly
- AND validation errors from the server are displayed in the error region

#### Scenario: Login form displays field-level errors

- GIVEN a user submits the login form with invalid data
- WHEN the server action returns validation errors
- THEN each field displays its specific error below the input
- AND a general error banner appears for form-level errors (e.g., invalid credentials)
- AND the `aria-describedby` attribute points to the correct error element for each field

### Requirement: Signup Form State Management

The signup form SHALL use controlled state only for UI toggles (password visibility, requirements validation), NOT for form field values.

#### Scenario: Form uses FormData directly

- GIVEN a user fills out the signup form
- WHEN the user submits the form
- THEN the Server Action receives a FormData object with all field values
- AND the form does NOT maintain `formValues` useState for name, username, email, password, confirmPassword
- AND inputs are uncontrolled (no value/onChange for form data)

### Requirement: Field-Level Validation State Management

The system SHOULD manage validation state at the field level to preserve valid inputs when form submission fails.

#### Scenario: Preserve valid field values on validation failure

- GIVEN a user has filled out the signup form with valid name, username, and email
- AND the user has entered invalid passwords that don't match
- WHEN the user submits the form
- THEN the name, username, and email fields retain their values
- AND only the password fields show validation errors
- AND the form does not reset completely

#### Scenario: Show field-specific errors

- GIVEN a user has entered an invalid email format
- AND all other fields are valid
- WHEN the user submits the form
- THEN an error message appears specifically below the email field
- AND no error messages appear below other fields
- AND the email field receives visual indication of error via aria-invalid attribute

#### Scenario: Maintain backend duplicate prevention

- GIVEN a user attempts to register with an email or username that already exists
- WHEN the user submits the form
- THEN the backend prevents duplicate creation
- AND an error message appears indicating the email or username already exists
- AND the error is displayed appropriately in the UI

### Requirement: Error Message Display

The system MUST display validation errors in proximity to the relevant form fields with proper accessibility attributes.

#### Scenario: Display errors under specific fields

- GIVEN a user has entered invalid data in the username field (too short)
- WHEN the user submits the form
- THEN the error message appears directly below the username field
- AND the username field receives visual indication of error via aria-invalid attribute
- AND the error message element has a unique ID
- AND the input has aria-describedby pointing to the error element

#### Scenario: Clear errors when field becomes valid

- GIVEN a user has entered an invalid email and sees an error message
- WHEN the user corrects the email to a valid format
- THEN the error message disappears
- AND the email field no longer shows visual indication of error

### Requirement: Error Message Localization

All error messages, labels, placeholders, and UI text in auth forms MUST be in Spanish.

#### Scenario: Login form entirely in Spanish

- GIVEN the login form is rendered
- THEN all labels, placeholders, descriptions, and button text are in Spanish
- AND error messages from the server are displayed as-is (already in Spanish from backend)
- AND the "Forgot password" link text is "¿Olvidaste tu contraseña?"
- AND the signup link text is "¿No tienes cuenta? Regístrate"

#### Scenario: Signup form entirely in Spanish

- GIVEN the signup form is rendered
- THEN all labels, placeholders, descriptions, and button text are in Spanish
- AND password requirements text is in Spanish
- AND the login link text is "¿Ya tienes cuenta? Inicia sesión"
- AND the GitHub OAuth button text is "Registrarse con GitHub"
- AND the GitHub OAuth button has aria-label="Registrarse con GitHub"