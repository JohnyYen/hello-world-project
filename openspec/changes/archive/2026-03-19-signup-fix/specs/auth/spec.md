# Auth Specification

## Purpose

This specification describes the authentication-related functionality for the signup form, including password visibility toggling, field-level validation, and error message display.

## Requirements

### Requirement: Password Visibility Toggle

The system SHOULD allow users to toggle the visibility of password fields to improve usability.

#### Scenario: Toggle password visibility on click

- GIVEN a user is viewing the password field in the signup form
- WHEN the user clicks the eye icon toggle button
- THEN the password field type changes from "password" to "text"
- AND the eye icon changes to indicate visibility is ON

#### Scenario: Toggle password visibility off on second click

- GIVEN a user has toggled password visibility ON
- WHEN the user clicks the eye icon toggle button again
- THEN the password field type changes from "text" to "password"
- AND the eye icon changes to indicate visibility is OFF

#### Scenario: Independent toggle for password and confirm password fields

- GIVEN a user is viewing both password and confirm password fields
- WHEN the user toggles visibility for the password field only
- THEN only the password field visibility changes
- AND the confirm password field visibility remains unchanged

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
- AND the email field receives visual indication of error

#### Scenario: Maintain backend duplicate prevention

- GIVEN a user attempts to register with an email or username that already exists
- WHEN the user submits the form
- THEN the backend prevents duplicate creation
- AND an error message appears indicating the email or username already exists
- AND the error is displayed appropriately in the UI

### Requirement: Error Message Display

The system SHOULD display validation errors in proximity to the relevant form fields.

#### Scenario: Display errors under specific fields

- GIVEN a user has entered invalid data in the username field (too short)
- WHEN the user submits the form
- THEN the error message "Mínimo 3 caracteres" appears directly below the username field
- AND the username field receives visual indication of error via aria-invalid attribute

#### Scenario: Clear errors when field becomes valid

- GIVEN a user has entered an invalid email and sees an error message
- WHEN the user corrects the email to a valid format
- THEN the error message disappears
- AND the email field no longer shows visual indication of error