# Design: Auth Pages Refactor - Spanish Translation & UX Improvement

## Technical Approach

Refactorizar LoginForm para usar `useActionState` con `loginAction` (Server Action), eliminar estado muerto de SignupForm, agregar password toggle a login, implementar validación de contraseña en tiempo real, traducir todo el texto a español, y unificar el layout de ambas páginas con diseño centrado sin imagen lateral.

## Architecture Decisions

### Decision: LoginForm Migration to Server Actions

**Choice**: Reemplazar `useState` + `useTransition` + `fetch` con `useActionState` + `loginAction`
**Alternatives considered**: 
- Mantener fetch pero mejorar error handling
- Crear un custom hook que envuelva la lógica de login
**Rationale**: `useActionState` es el patrón estándar del proyecto para mutaciones, ya existe `loginAction` en actions.ts, proporciona validación Zod automática, y elimina código boilerplate de manejo de errores.

### Decision: Remove formValues State from SignupForm

**Choice**: Eliminar completamente `formValues` useState y onChange handlers
**Alternatives considered**:
- Mantener formValues para validación client-side
- Usar formValues para mostrar valores previos en errores
**Rationale**: Server Actions leen directamente de FormData, el estado era código muerto que causaba re-renders innecesarios en cada keystroke. La validación ya ocurre en el servidor con Zod.

### Decision: Password Requirements Validation Approach

**Choice**: Implementar validación client-side en tiempo real con estado local para indicadores visuales, SIN controlar los valores del formulario
**Alternatives considered**:
- Validación solo en el servidor (como ahora)
- Controlar todo el formulario con useState para validación
**Rationale**: Balance óptimo - feedback inmediato al usuario sin re-renders innecesarios. Solo el password field tiene estado local para los indicadores, los demás campos usan FormData directamente.

### Decision: Layout Consistency

**Choice**: Ambas páginas usan layout centrado con `max-w-sm`, sin imagen lateral en signup
**Alternatives considered**:
- Mantener layout diferente para signup con imagen
- Usar layout con imagen solo en desktop
**Rationale**: Consistencia visual entre auth pages, menor complejidad de mantenimiento, y enfoque en usabilidad sobre decoración.

## Data Flow

### Login Flow (New)

```
User Input → FormData → useActionState → loginAction (Server)
                                              ↓
                                         Zod Validation
                                              ↓
                                    authService.login()
                                              ↓
                                   Set auth_token cookie
                                              ↓
                                    redirect("/dashboard")
                                              ↓
                    ┌─────────────────────────┴─────────────────────┐
                    ↓                                               ↓
              Success: Redirect                          Error: Return ActionState
                   ↓                                          ↓
              /dashboard                           Form re-renders with errors
                                                     ↓
                                            aria-describedby announces
```

### Signup Flow (Optimized)

```
User Input → FormData → useActionState → signupAction (Server)
                     ↗
    Password Validation State (local, only for indicators)
                                              ↓
                                         Zod Validation
                                              ↓
                                   authService.register()
                                              ↓
                                    redirect("/login")
                                              ↓
                    ┌─────────────────────────┴─────────────────────┐
                    ↓                                               ↓
              Success: Redirect                          Error: Return ActionState
                   ↓                                          ↓
              /login                               Form re-renders with errors
                                                     ↓
                                            toast.error() + field errors
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `apps/frontend/src/components/auth/login-form.tsx` | Modify | Refactor to useActionState, add password toggle, translate to Spanish, fix ARIA |
| `apps/frontend/src/components/auth/signup-form.tsx` | Modify | Remove formValues state, translate to Spanish, fix ARIA, add password requirements validation |
| `apps/frontend/src/app/(auth)/signup/page.tsx` | Modify | Remove lateral image, change layout to match login |
| `apps/frontend/src/lib/actions.ts` | Unchanged | loginAction and signupAction already exist and are correct |
| `apps/frontend/src/components/auth/index.ts` | Unchanged | Exports already correct |

## Interfaces / Contracts

### LoginForm Component Interface

```typescript
interface LoginFormProps extends React.ComponentProps<"div"> {
  className?: string;
}

// Returns void - form handles redirects internally via Server Action
export function LoginForm({ className, ...props }: LoginFormProps): JSX.Element
```

### SignupForm Component Interface

```typescript
interface SignupFormProps extends React.ComponentProps<"form"> {
  className?: string;
}

export function SignupForm({ className, ...props }: SignupFormProps): JSX.Element
```

### Password Validation State Interface (New for SignupForm)

```typescript
interface PasswordRequirements {
  minLength: boolean;    // 8+ characters
  hasUppercase: boolean; // At least one uppercase
  hasLowercase: boolean; // At least one lowercase
  hasNumber: boolean;    // At least one number
}

// Derived from password value, not stored as state
function getPasswordRequirements(password: string): PasswordRequirements
```

### ActionState Interface (Existing, reused)

```typescript
export type ActionState = {
  message?: string;
  errors?: Record<string, string[]>;
  success?: boolean;
};
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Password requirements validation function | Test each requirement independently, edge cases |
| Unit | LoginForm renders with correct Spanish text | Snapshot or queryByText assertions |
| Unit | SignupForm does NOT have formValues state | Verify component structure |
| Integration | LoginForm submits via loginAction | Mock useActionState, verify action prop |
| Integration | Error messages display with correct ARIA | Render with errors, check aria-describedby |
| E2E | Existing auth tests pass | Run `tests/e2e/auth/auth.spec.ts` |
| Accessibility | Screen reader announces errors | Manual test with NVDA/VoiceOver |
| Accessibility | Keyboard navigation works | Manual test with Tab/Enter/Escape |
| Performance | No unnecessary re-renders | React DevTools Profiler |

## Migration / Rollout

No migration required. This is a pure frontend refactor with no data changes.

**Phased approach**:
1. First: Refactor LoginForm to use Server Action (highest risk)
2. Second: Fix accessibility and translation issues (low risk)
3. Third: Remove signup image and optimize performance (low risk)
4. Final: E2E tests validation

**Feature flags**: None needed - changes are atomic per file.

## Open Questions

- [ ] ¿El link "¿Olvidaste tu contraseña?" debe apuntar a `/forgot-password` (página aún no existe) o mantener `#` temporalmente?
  - **Recommendation**: Mantener `#` por ahora, implementar forgot-password flow en separate change
- [ ] ¿Se debe agregar un `toast.success` en login exitoso además del redirect?
  - **Recommendation**: No - el redirect es feedback suficiente, evitar toast redundantes
