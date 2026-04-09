# Proposal: Auth Pages Refactor - Spanish Translation & UX Improvement

## Intent

Refactorizar las páginas de login y signup para cumplir con los estándares del proyecto: texto completamente en español, patrones consistentes de Server Actions, accesibilidad mejorada, y diseño optimizado siguiendo el design system Indigo & Violet. Eliminar la imagen lateral del signup form y mejorar la experiencia de usuario con validación de contraseña en tiempo real.

## Scope

### In Scope
- Traducir TODO el texto de login y signup forms al español (labels, placeholders, descripciones, mensajes de error, enlaces)
- Refactorizar `LoginForm` para usar `loginAction` Server Action en lugar de `fetch` directo
- Eliminar estado muerto (`formValues`) de `SignupForm` para reducir re-renders innecesarios
- Eliminar imagen lateral en signup page, usar layout centrado consistente con login
- Corregir problemas de accesibilidad: ARIA descriptors correctos, aria-labels en botones de contraseña, loading states announces
- Agregar toggle show/hide de contraseña en login form (como ya tiene signup)
- Implementar validación visual de requisitos de contraseña en tiempo real (8+ chars, mayúscula, minúscula, número)
- Unificar manejo de errores entre login y signup (field-level errors + toast notifications)
- Optimizar rendimiento eliminando re-renders innecesarios

### Out of Scope
- Refactorizar sistema de logout dual (separate change)
- Optimizar `getServerUser` fallback chain con caching (separate change)
- Implementar forgot password flow (solo preparar link, no implementar)
- Agregar tests unitarios de auth services (separate change)
- Refactorizar `AuthContext` state management (separate change)

## Approach

1. **Unificar patrones**: Ambos formularios usarán `useActionState` con Server Actions (`loginAction` y `signupAction`)
2. **Eliminar código muerto**: Remover `formValues` de signup form (la action lee de FormData directamente)
3. **Traducción completa**: Reemplazar todo texto inglés por español, manteniendo tono profesional y consistente
4. **Accesibilidad**: 
   - Corregir `aria-describedby` para apuntar al elemento de error correcto
   - Agregar `aria-label` a todos los botones de icono
   - Usar `aria-live="polite"` para mensajes de error dinámicos
   - Mejorar focus states con `focus-visible` del design system
5. **UX Password**: 
   - Toggle visibility en ambos forms
   - Indicador visual de requisitos (checkmarks verdes/rojos en tiempo real)
   - Validación client-side antes de submit
6. **Layout consistente**: Ambas páginas con layout centrado, sin imagen lateral en signup
7. **Performance**: Eliminar estados que causan re-renders innecesarios, usar patrones React 19

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `apps/frontend/src/components/auth/login-form.tsx` | Modified | Refactor to use Server Action, add password toggle, fix accessibility, translate to Spanish |
| `apps/frontend/src/components/auth/signup-form.tsx` | Modified | Remove dead state, fix accessibility, translate to Spanish, improve password validation UX |
| `apps/frontend/src/app/(auth)/login/page.tsx` | Unchanged | Page layout already correct |
| `apps/frontend/src/app/(auth)/signup/page.tsx` | Modified | Remove lateral image, adjust layout to match login |
| `apps/frontend/src/lib/actions.ts` | Unchanged | Server actions already exist and are correct |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| LoginForm refactor rompe flujo de login actual | Medium | Mantener API route como fallback temporal, test E2E exhaustivo |
| Validación de contraseña en tiempo real causa re-renders | Low | Usar debounce si es necesario, profile con React DevTools |
| Traducción incorrecta o inconsistente | Low | Review manual del usuario (habla español nativo) |
| Cambios de ARIA rompen validación existente | Low | Test con screen reader, mantener atributos requeridos |
| Eliminar imagen afecta percepción de marca | Medium | Nuevo diseño debe ser visualmente atractivo con design system |

## Rollback Plan

1. Si hay problemas críticos después del merge:
   ```bash
   git revert <commit-hash>
   ```
2. Si solo algunos cambios causan problemas:
   - Revertir archivos individuales desde git history
   - Mantener traducciones y accesibilidad (mejoras seguras)
   - Revertir solo refactor de LoginForm si es problemático
3. Worktree actual permite probar en aislamiento antes de merge
4. E2E tests existentes deben pasar antes de considerar merge

## Dependencies

- Design system actual (shadcn/ui components) debe permanecer sin cambios
- Server Actions (`loginAction`, `signupAction`) ya existen en `actions.ts`
- E2E tests existentes en `tests/e2e/auth/auth.spec.ts` para validación
- No requiere cambios en backend ni API client

## Success Criteria

- [ ] Todo texto en login y signup forms está en español
- [ ] LoginForm usa `loginAction` Server Action (no `fetch` directo)
- [ ] SignupForm no tiene estado `formValues` muerto
- [ ] Imagen lateral eliminada de signup page
- [ ] Ambos forms tienen toggle show/hide de contraseña
- [ ] Validación visual de requisitos de contraseña en tiempo real funcionando
- [ ] Todos los campos tienen `aria-describedby` correcto apuntando a su mensaje de error
- [ ] Botones de icono tienen `aria-label` descriptivo
- [ ] Loading states son anunciados por screen readers (`aria-live`)
- [ ] E2E tests existentes pasan sin modificaciones (o con updates mínimas)
- [ ] No hay re-renders innecesarios verificados con React DevTools
- [ ] Layout consistente entre ambas páginas (centrado, responsive)
