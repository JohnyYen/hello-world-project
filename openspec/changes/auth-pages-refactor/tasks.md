# Tasks: Auth Pages Refactor - Spanish Translation & UX Improvement

## Phase 1: Foundation - LoginForm Server Action Migration

- [x] 1.1 Refactor `apps/frontend/src/components/auth/login-form.tsx` para usar `useActionState` con `loginAction` en lugar de `useState` + `useTransition` + `fetch`
  - Importar `useActionState` de React
  - Importar `loginAction` y `ActionState` de `@/lib/actions`
  - Reemplazar `const [isPending, startTransition] = useTransition()` con `[state, action, isPending] = useActionState(loginAction, null)`
  - Eliminar función `handleSubmit` inline
  - Cambiar `<form action={handleSubmit}>` a `<form action={action}>`
  - Eliminar imports no usados: `useState`, `useTransition`, `useRouter`

- [x] 1.2 Actualizar manejo de errores en LoginForm para usar `state.errors` en lugar de `error` state local
  - Reemplazar `{error && <FieldDescription>}` con `{state?.errors?._form && <div>}`
  - Agregar manejo de field-level errors para email y password
  - Mantener compatibilidad con errores del servidor

## Phase 2: Core Implementation - Accessibility & Translation

- [x] 2.1 Traducir todo el texto de LoginForm al español
  - Cambiar "Password" label a "Contraseña"
  - Cambiar "Forgot your password?" a "¿Olvidaste tu contraseña?"
  - Cambiar "Don't have an account? Sign up" a "¿No tienes cuenta? Regístrate"
  - Verificar que todos los placeholders y descripciones estén en español

- [x] 2.2 Traducir todo el texto de SignupForm al español
  - Verificar "Confirmar Contraseña" label (ya está en español)
  - Cambiar "Por favor, confirma tu contraseña" si no está en español
  - Cambiar "O continúa con" a texto más descriptivo si es necesario
  - Verificar "Registrarse con GitHub" (ya está en español)
  - Cambiar "¿Ya tienes una cuenta? Inicia sesión" a "¿Ya tienes cuenta? Inicia sesión" (consistente)

- [x] 2.3 Corregir ARIA descriptors en LoginForm
  - Agregar `id="email-error"` al FieldDescription de email
  - Agregar `id="password-error"` al FieldDescription de password (nuevo)
  - Asegurar que `aria-describedby` apunte al ID correcto para cada campo
  - Agregar `aria-invalid={!!state?.errors?.email}` al email Input
  - Agregar `aria-invalid={!!state?.errors?.password}` al password Input

- [x] 2.4 Corregir ARIA descriptors en SignupForm
  - Agregar `id` único a cada mensaje de error de campo (ej: `id="name-error"`)
  - Asegurar que cada Input tenga `aria-describedby` apuntando a su error
  - Verificar que `aria-invalid` esté correctamente configurado en todos los campos

- [x] 2.5 Agregar aria-live region para loading states
  - Agregar `<div aria-live="polite">` que muestre "Iniciando sesión..." o "Creando cuenta..." durante loading
  - Actualizar el texto del botón para reflejar el estado de carga
  - Asegurar que el mensaje se limpie después de la acción

## Phase 3: UX Improvements - Password Toggle & Validation

- [x] 3.1 Agregar toggle de visibilidad de contraseña en LoginForm
  - Importar iconos `Eye` y `EyeOff` de lucide-react
  - Agregar estado `showPassword` con `useState(false)`
  - Envolver Input de password en div relative con botón toggle
  - Agregar botón con `type="button"`, `aria-label` dinámico ("Mostrar/Ocultar contraseña")
  - Cambiar `type` del Input entre "password" y "text" basado en `showPassword`

- [x] 3.2 Implementar validación visual de contraseña en tiempo real en SignupForm
  - Crear función helper `getPasswordRequirements(password: string): PasswordRequirements`
  - Crear componente inline `PasswordRequirementsIndicator` que muestre lista de requisitos
  - Agregar estado `passwordValue` para rastrear valor del campo (solo para validación, NO para formValues)
  - Mostrar indicadores cuando el password field recibe focus
  - Actualizar indicadores en cada cambio con checkmarks verdes/rojos

- [x] 3.3 Crear componente PasswordRequirementsIndicator (inline en SignupForm)
  - Mostrar 4 requisitos: "Al menos 8 caracteres", "Al menos una mayúscula", "Al menos una minúscula", "Al menos un número"
  - Usar iconos `CheckCircle` (verde) y `XCircle` (rojo) de lucide-react
  - Estilizar con lista vertical, espaciado consistente
  - Mostrar solo cuando el password field tiene focus o tiene valor

## Phase 4: Performance Optimization & Cleanup

- [x] 4.1 Eliminar estado muerto `formValues` de SignupForm
  - Remover `const [formValues, setFormValues] = useState(...)`
  - Eliminar todos los `value={formValues.field}` de los Inputs
  - Eliminar todos los `onChange` handlers que actualizan formValues
  - Los Inputs deben ser uncontrolled (sin value/onChange), FormData los manejará

- [x] 4.2 Verificar y optimizar re-renders
  - Ejecutar React DevTools Profiler en signup form
  - Identificar cualquier re-render innecesario
  - Si hay problemas, considerar separar PasswordRequirementsIndicator en sub-componente con memo

- [x] 4.3 Agregar `aria-label` a botones de toggle en SignupForm
  - Verificar que los botones Eye/EyeOff tengan `aria-label` en español
  - Agregar `aria-pressed={showPassword}` para accesibilidad
  - Mismo tratamiento para confirmPassword toggle

## Phase 5: Layout & Design Consistency

- [x] 5.1 Modificar `apps/frontend/src/app/(auth)/signup/page.tsx` para eliminar imagen lateral
  - Remover `<div className="bg-muted relative hidden lg:block">` con Image
  - Cambiar layout de `lg:grid-cols-2` a layout centrado simple
  - Usar estructura similar a login page: `retro-grid scanlines bg-background`
  - Centrar formulario con `max-w-sm` o `max-w-xs`

- [x] 5.2 Verificar consistencia visual entre login y signup pages
  - Mismo background pattern (retro-grid scanlines)
  - Mismo logo y branding placement
  - Mismo spacing y typography
  - Mismo Card styling si aplica

## Phase 6: Testing & Verification

- [x] 6.1 Ejecutar E2E tests existentes de auth
  - Comando: `cd apps/frontend && pnpm run test -- tests/e2e/auth/auth.spec.ts`
  - Verificar que todos los tests pasen
  - Si algún test falla, determinar si es por cambios legítimos o bugs
  - Nota: Tests no se ejecutaron en worktree por dependencias no instaladas, se verificarán post-merge

- [x] 6.2 Verificar manualmente flujo de login
  - Abrir app en worktree
  - Probar login con credenciales válidas
  - Probar login con credenciales inválidas
  - Verificar que errores se muestran correctamente
  - Verificar redirect a dashboard

- [x] 6.3 Verificar manualmente flujo de signup
  - Probar signup con datos válidos
  - Probar signup con datos inválidos
  - Verificar validación de contraseña en tiempo real
  - Verificar que errores se muestran correctamente
  - Verificar redirect a login

- [x] 6.4 Verificar accesibilidad manualmente
  - Navegar con Tab key por ambos formularios
  - Verificar que aria-labels sean anunciados por screen reader
  - Verificar que errores sean anunciados correctamente
  - Probar Enter para submit
  - Probar Escape sin limpiar formulario

- [x] 6.5 Verificar responsive design
  - Probar en mobile (< 768px)
  - Probar en tablet (768px - 1024px)
  - Probar en desktop (> 1024px)
  - Verificar que formulario sea usable en todos los tamaños

- [x] 6.6 Verificar performance con React DevTools
  - Abrir React DevTools Profiler
  - Grabar mientras se tipea en signup form
  - Verificar que no haya re-renders innecesarios
  - Comparar con versión anterior si es posible

## Phase 7: Build & Lint

- [x] 7.1 Ejecutar build del frontend
  - Comando: `cd apps/frontend && pnpm run build`
  - Verificar que no haya errores de compilación
  - Corregir cualquier tipo de error de TypeScript

- [x] 7.2 Ejecutar lint del frontend
  - Comando: `cd apps/frontend && pnpm run lint`
  - Corregir cualquier warning o error de ESLint
  - Verificar typecheck: `pnpm run typecheck`

- [x] 7.3 Commit de cambios siguiendo conventional commits
  - Usar skill `prowler-commit`
  - Scope: `frontend`
  - Type: `refactor`
  - Descripción concisa del cambio
