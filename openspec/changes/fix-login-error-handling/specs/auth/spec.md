# Delta for Auth

## ADDED Requirements

### Requirement: Backend Handles User Not Found as Auth Failure

The backend MUST treat a non-existent user lookup as an authentication failure, returning HTTP 401 with a generic error message that does not reveal whether the email exists in the system.

#### Scenario: Login with non-existent email

- GIVEN a user attempts to login with an email that does not exist in the system
- WHEN the `AuthenticateUseCase.execute` method processes the request
- THEN the system raises an exception that results in HTTP 401
- AND the response body contains `{"detail": "Credenciales incorrectas"}`
- AND the response does NOT reveal that the user does not exist

### Requirement: Frontend Displays Auth Error Messages

The frontend login form MUST display error messages returned by the backend when authentication fails.

#### Scenario: Display error after failed login

- GIVEN a user submits invalid credentials on the login form
- AND the backend returns HTTP 401 with `{"detail": "Credenciales incorrectas"}`
- WHEN the `loginAction` receives the error response
- THEN the `state.errors._form` array contains the detail message
- AND the message is rendered in red text below the form fields
- AND the user remains on the `/login` page

## MODIFIED Requirements

### Requirement: AuthenticateUseCase Error Handling

The `AuthenticateUseCase.execute` method MUST catch all user-not-found and password-verification errors and raise `InvalidCredentialsException` uniformly.

(Previously: Only `InvalidCredentialsException` from `authenticate_by_username_or_email` was caught at the endpoint level; other exceptions like `DoesNotExistError` propagated as unhandled errors.)

#### Scenario: Repository raises DoesNotExistError

- GIVEN the `UserRepository.authenticate_by_username_or_email` method raises an exception indicating user not found
- WHEN the exception is raised inside `AuthenticateUseCase.execute`
- THEN the usecase catches the exception
- AND raises `InvalidCredentialsException("Credenciales incorrectas")` instead

#### Scenario: Repository raises InvalidCredentialsException

- GIVEN the `UserRepository.authenticate_by_username_or_email` method raises `InvalidCredentialsException`
- WHEN the exception is raised inside `AuthenticateUseCase.execute`
- THEN the exception is allowed to propagate as-is (already handled by the endpoint)

### Requirement: Login Endpoint Exception Handling

The login endpoint `/api/v1/auth/login` MUST catch all unexpected exceptions and return HTTP 401 with a generic message.

(Previously: Only `InvalidCredentialsException` was caught; other exceptions like `DoesNotExistError` resulted in 500 errors with `exc_type` in the response body.)

#### Scenario: Unhandled exception during login

- GIVEN an unexpected error occurs during the login flow
- WHEN the exception is raised in the endpoint handler
- THEN the endpoint catches the exception
- AND returns HTTP 401 with `{"detail": "Credenciales incorrectas"}`
