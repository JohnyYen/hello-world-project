# Delta for Auth

## ADDED Requirements

### Requirement: Password Visibility Toggle on Login Form

The login form MUST provide a toggle button to show/hide the password field content.

#### Scenario: Toggle password visibility on login form

- GIVEN a user is viewing the login form
- WHEN the user clicks the eye icon toggle button in the password field
- THEN the password field type changes from "password" to "text"
- AND the icon changes from Eye to EyeOff
- AND the button has an aria-label in Spanish ("Mostrar contraseña" or "Ocultar contraseña")

#### Scenario: Password field returns to hidden on form submission

- GIVEN a user has toggled password visibility to visible
- WHEN the user submits the login form
- THEN the password field type resets to "password" on next render

### Requirement: Real-Time Password Requirements Validation

The signup form MUST display visual feedback for password requirements as the user types.

#### Scenario: Password requirements displayed as checklist

- GIVEN a user is filling the password field in the signup form
- WHEN the password field receives focus
- THEN a requirements checklist appears below the field
- AND each requirement shows a red X icon initially (unchecked state)

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
- THEN an aria-live="polite" region displays "Iniciando sesión..." or "Creando cuenta..."
- AND the submit button is disabled
- AND the button text changes to the loading state

#### Scenario: Loading state cleared on completion

- GIVEN a form is in loading state
- WHEN the action completes (success or error)
- THEN the aria-live region updates with the result message
- AND the submit button is re-enabled

## MODIFIED Requirements

### Requirement: Login Form Submission Method

The login form SHALL use the `loginAction` Server Action via `useActionState` instead of direct fetch calls.

(Previously: LoginForm used inline fetch to `/api/auth/login` with manual state management)

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

(Previously: SignupForm maintained `formValues` state for all fields, causing unnecessary re-renders)

#### Scenario: Form uses FormData directly

- GIVEN a user fills out the signup form
- WHEN the user submits the form
- THEN the Server Action receives a FormData object with all field values
- AND the form does NOT maintain `formValues` useState for name, username, email, password, confirmPassword

### Requirement: Error Message Localization

All error messages, labels, placeholders, and UI text in auth forms MUST be in Spanish.

(Previously: Mixed English/Spanish text - "Forgot your password?", "Don't have an account?", etc.)

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

## REMOVED Requirements

### Requirement: Client-Side Fetch for Login

(Reason: LoginForm now uses Server Action pattern, eliminating the need for direct fetch calls and manual error extraction)

### Requirement: Dual Password State in Signup

(Reason: `formValues` state was dead code - Server Actions read from FormData directly, making the useState for form values unnecessary and causing re-renders)
