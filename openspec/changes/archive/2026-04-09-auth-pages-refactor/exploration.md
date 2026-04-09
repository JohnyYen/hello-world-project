# Exploration: Auth Pages Refactor

**Date**: 2026-04-09  
**Status**: Complete  
**Change**: auth-pages-refactor

---

## Current State

The authentication system consists of:

- **Login**: Two parallel implementations - `LoginForm` uses direct `fetch("/api/auth/login")`, while `loginAction` (Server Action) exists but is unused
- **Signup**: Uses `useActionState` with `signupAction` (Server Action) with Zod validation
- **Password Change**: Uses `useActionState` with `changePasswordAction` (Server Action)
- **State Management**: Mixed - client-side via `AuthContext`, server-side via `getServerUser()` and HTTP-only cookies
- **Design**: Indigo & Violet palette with shadcn/ui components

---

## Affected Areas

- `apps/frontend/src/components/auth/login-form.tsx` — Main login form, needs refactor to use Server Actions
- `apps/frontend/src/components/auth/signup-form.tsx` — Signup form, has dead `formValues` state
- `apps/frontend/src/app/(auth)/login/page.tsx` — Login page layout
- `apps/frontend/src/app/(auth)/signup/page.tsx` — Signup page layout, has lateral image to remove
- `apps/frontend/src/lib/actions.ts` — Server actions (loginAction, signupAction already exist)
- `apps/frontend/src/context/auth-context.tsx` — Client-side auth state management
- `apps/frontend/src/lib/auth-server.ts` — Server-side user retrieval utilities
- `apps/frontend/tests/e2e/auth/auth.spec.ts` — E2E tests that may need updates

---

## Issues Identified

### Functional Issues
1. **LoginForm bypasses Server Action** — Uses direct fetch instead of `loginAction`, missing Zod validation
2. **Error display inconsistency** — Login shows all errors under email field only
3. **Dead code in SignupForm** — `formValues` state is maintained but never used by action
4. **Mixed language** — English text in labels, placeholders, and descriptions

### Accessibility Issues
1. **Incorrect ARIA associations** — `aria-describedby` points to wrong error elements
2. **Missing aria-labels** — Password toggle buttons in ChangePasswordForm lack labels
3. **No loading announcements** — AuthGuard spinner not announced to screen readers
4. **SVG without context** — GitHub OAuth button lacks accessible description

### Performance Issues
1. **Unnecessary re-renders** — SignupForm's `formValues` causes re-render on every keystroke
2. **Expensive server calls** — `getServerUser` fallback chain can make 2 API calls + fetch 1000 users
3. **No caching strategy** — All fetches use `cache: "no-store"` unnecessarily
4. **Client-side fetch on mount** — `getMeFromCookie` calls API route on every client mount

---

## Approaches

### Approach 1: Incremental Refactor (Recommended)
**Description**: Refactor login form to use `loginAction` Server Action, fix accessibility issues, translate to Spanish, remove signup image, improve UX with password validation feedback

- **Pros**: 
  - Minimal risk, builds on existing patterns
  - Leverages existing `loginAction` already in codebase
  - Can be tested incrementally
  - No breaking changes to auth flow
- **Cons**: 
  - Doesn't address deeper architectural issues (dual logout, expensive getServerUser)
  - Still has mixed client/server state management
- **Effort**: Low-Medium
- **Timeline**: 2-3 sessions

### Approach 2: Complete Auth System Redesign
**Description**: Unify all auth into a single coherent pattern: Server Actions only, shared form components, centralized error handling, optimized getServerUser with caching

- **Pros**:
  - Clean, consistent architecture
  - Better performance with caching
  - Easier to maintain long-term
- **Cons**:
  - High risk of breaking existing functionality
  - Requires changes to backend API routes
  - Needs extensive testing
  - May introduce regressions
- **Effort**: High
- **Timeline**: 5-7 sessions

### Approach 3: UI/UX Focus Only
**Description**: Keep current architecture, focus only on visual design improvements, Spanish translation, and accessibility fixes

- **Pros**:
  - Lowest risk
  - Quick to implement
  - Immediate user-facing improvements
- **Cons**:
  - Doesn't fix underlying inconsistencies
  - LoginForm still bypasses Server Actions
  - Technical debt remains
- **Effort**: Low
- **Timeline**: 1-2 sessions

---

## Recommendation

**Approach 1: Incremental Refactor**

This balances risk with impact:
1. Fixes the most critical inconsistency (LoginForm not using Server Action)
2. Addresses all user-facing concerns (Spanish translation, accessibility, design)
3. Removes dead code and improves performance
4. Sets foundation for future improvements without breaking changes
5. Can be completed quickly with minimal testing scope

The deeper architectural issues (dual logout, expensive getServerUser) should be addressed in a separate, focused change.

---

## Risks

1. **LoginForm refactor may break existing login flow** — Mitigation: Keep API route as fallback initially, test E2E thoroughly
2. **Removing signup image may affect brand perception** — Mitigation: Ensure new layout is visually compelling with design system
3. **Changing error handling may affect error messages** — Mitigation: Maintain backward compatibility in error format
4. **Translation errors or inconsistencies** — Mitigation: Review all Spanish text with native speaker (user can validate)

---

## Ready for Proposal

**Yes** — Ready to create proposal with Approach 1 scope:
- Refactor LoginForm to use `loginAction` Server Action
- Translate all text to Spanish
- Remove signup lateral image
- Fix accessibility issues (ARIA, error display, loading states)
- Remove dead code (`formValues` in signup)
- Add real-time password validation feedback
- Consistent design patterns across both forms
