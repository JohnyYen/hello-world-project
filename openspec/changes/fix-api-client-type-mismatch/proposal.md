# Fix API Client Type Mismatch - User ID UUID vs Number

## Problem

The backend returns user `id` as a UUID string (e.g., `4721bf75-cae8-4b0d-891d-b89bb1565b42`) but the auto-generated API client TypeScript model (`UserResponse`) declares `id: number`. This type mismatch causes a runtime parsing error in the Server Action, preventing successful login redirect.

**Evidence**: Backend response shows `"user": {"id": "4721bf75-cae8-4b0d-891d-b89bb1565b42", ...}` — `id` is a string UUID, not a number.

## Impact

- Login Server Action fails silently when parsing the response
- `auth_token` cookie is never set
- User is not redirected to `/dashboard`
- Affects ALL endpoints that return `UserResponse` or any model with UUID `id` fields

## Goals

1. Regenerate the API client from the current OpenAPI spec to fix all type mismatches
2. Verify login redirect works end-to-end
3. Ensure no other type mismatches exist in the client

## Non-Goals

- Changing the backend UUID to integer IDs
- Refactoring the entire API client architecture

## Affected Modules

| Module | File(s) | Change Type |
|--------|---------|-------------|
| API Client | `packages/api-client-ts/models/UserResponse.ts` | Regenerate (id: number → id: string) |
| API Client | `packages/api-client-ts/models/*.ts` | Regenerate all models with correct types |
| Frontend | Any file consuming `UserResponse.id` | May need type adjustments |

## Rollback Plan

Regenerating the API client is reversible by re-running the generator with the old OpenAPI spec. The `git stash` of the current client state allows easy rollback.

## Success Criteria

1. `UserResponse.id` is typed as `string` (matching backend UUID)
2. Login with valid credentials sets `auth_token` cookie and redirects to `/dashboard`
3. No TypeScript errors in changed files (pre-existing errors in unrelated files are acceptable)
