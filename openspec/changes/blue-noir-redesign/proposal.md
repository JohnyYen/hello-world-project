# Proposal: Blue & Noir Redesign - Modern Minimalist Design

## Intent

Actualizar el diseño del frontend de un estilo retro/vintage (con flat-shadow, borders prominentes y scanlines) a un estilo moderno y minimalista con gradientes sutiles y sombras elegantes. El objetivo es mejorar la experiencia de usuario con una estética más limpia y profesional mientras se mantiene la paleta de colores Blue & Noir existente.

## Scope

### In Scope

1. **Actualización de globals.css**
   - Definir gradientes sutiles para background en modo light y dark
   - Implementar sombras elegantes (no flat)
   - Agregar variables para gradient mesh backgrounds
   - Definir efectos glassmorphism

2. **Componentes UI Actualizados**
   - Buttons: Eliminar flat-shadow, agregar gradiente sutil y shadow-sm
   - Cards: Cambiar de border-4 flat a shadow-lg con gradiente sutil
   - Inputs: Agregar focus ring con gradiente
   - Sidebar: Implementar glassmorphism (backdrop-blur, bg-opacity)
   - Sheets: Similar tratamiento glassmorphism

3. **Landing Page**
   - Hero section con gradient mesh background
   - Features con cards de gradiente sutil
   - Navbar con efecto glass

4. **Dashboard**
   - Metric cards con gradiente y sombras elegantes
   - Sidebar con glassmorphism
   - Mejora visual de charts y tablas

### Out of Scope

- Cambios en funcionalidad o lógica de negocio
- Modificación de APIs o estructura de datos
- Creación de nuevos pages/rutas
- Cambios en el backend

## Approach

### Fase 1: Actualización de Tokens y CSS
- Agregar nuevas variables CSS para gradientes y sombras en globals.css
- Mantener compatibilidad con la paleta blue/noir existente
- Definir efectos glassmorphism reutilizables

### Fase 2: Refactor de Componentes Base
- Button: Nuevo variant "gradient" con shadow-lg
- Card: Actualizar para usar shadow en lugar de flat-shadow
- Input: Mejorar focus states
- Sidebar: Aplicar glassmorphism con backdrop-blur

### Fase 3: Landing Page
- Implementar gradient mesh background con CSS
- Actualizar hero, features y navbar

### Fase 4: Dashboard
- Metric cards con gradiente sutil
- Glassmorphism en sidebar
- Mejora visual general

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `apps/frontend/src/app/globals.css` | Modificado | Nuevas variables para gradientes, sombras, glassmorphism |
| `apps/frontend/src/components/ui/button.tsx` | Modificado | Nuevos variants: gradient, glass |
| `apps/frontend/src/components/ui/card.tsx` | Modificado | Estilo moderno con shadow-lg |
| `apps/frontend/src/components/ui/input.tsx` | Modificado | Focus ring con gradiente |
| `apps/frontend/src/components/ui/sidebar.tsx` | Modificado | Glassmorphism effect |
| `apps/frontend/src/components/ui/sheet.tsx` | Modificado | Glassmorphism effect |
| `apps/frontend/src/components/landing/*` | Modificado | Gradient mesh y glass effects |
| `apps/frontend/src/app/(landing-page)/page.tsx` | Modificado | Landing page redesign |
| `apps/frontend/src/app/dashboard/*` | Modificado | Dashboard con metric cards modernas |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Breaking changes en componentes existentes | Medium | Mantener backward compatibility con variants existentes |
| Incompatibilidad con dark mode | Medium | Testear ambos modos thoroughly |
| Degradación de performance por efectos | Low | Usar CSS transforms, evitar animaciones heavies |
| Conflictos con estilos de shadcn/ui | Low | Usar overrides específicos, no modificar lib base |

## Rollback Plan

1. Reversar cambios en globals.css manteniendo solo variables blue/noir originales
2. Restaurar button.tsx y card.tsx a sus estilos anteriores (flat-shadow)
3. Eliminar variants de gradiente añadidos
4. No requiere migración de datos - es cambio puramente visual

## Dependencies

- Ninguna dependencia externa requerida
- Requiere que el proyecto frontend esté funcional

## Success Criteria

- [ ] Landing page muestra gradient mesh background correctamente
- [ ] Dashboard sidebar tiene efecto glassmorphism visible
- [ ] Buttons tienen nuevo variant con gradiente sutil
- [ ] Cards usan shadow-lg en lugar de flat-shadow
- [ ] Ambos modos (light/dark) funcionan correctamente
- [ ] UI text permanece en Español
- [ ] No hay console errors relacionados con los cambios
