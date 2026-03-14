# Proposal: Retro Redesign

## Intent

El usuario solicita una mejora visual completa de la aplicación para adoptar un diseño coherente, sencillo y con un toque retro (años 80/90, computadoras antiguas). Actualmente, la aplicación utiliza un diseño moderno con componentes shadcn/ui. El objetivo es transformar la estética visual para evocar la nostalgia de las primeras interfaces de computadoras personales, manteniendo la funcionalidad y la usabilidad.

**Problema:** La interfaz actual carece de una identidad visual distintiva y no sigue el estilo retro solicitado.
**Solución:** Implementar un tema visual retro que incluya paleta de colores, tipografía, efectos (scanlines, bordes) y componentes adaptados al estilo.

## Scope

### In Scope
- Actualización de la paleta de colores global (CSS variables).
- Adaptación de la tipografía (fuente monoespaciada y sans-serif adecuada).
- Re-diseño de componentes de la librería `shadcn/ui` (Button, Card, Input, etc.) para el estilo retro.
- Aplicación de efectos visuales (scanlines, grid, sombras planas).
- Actualización de las páginas principales: Login, Dashboard, Páginas de Estudiantes, Configuración.
- Creación de un componente de diseño global (`ThemeProvider` o similar) para gestionar el modo claro/oscuro retro.

### Out of Scope
- Cambios en la lógica de negocio o la estructura de datos.
- Funcionalidad nueva (features).
- Reescritura completa del backend.

## Approach

Se utilizará Tailwind 4 con soporte para variables CSS (temas) para definir el estilo retro.
1.  **Definir Variables CSS Retro:** Establecer colores "crema", "ámbar", "slate" y efectos de "scanline" en `globals.css`.
2.  **Actualizar Componentes shadcn/ui:** Modificar los estilos de los componentes base (Button, Card, Input) para usar bordes gruesos, sombras planas y tipografía monoespaciada.
3.  **Aplicar Efectos Visuales:** Crear utilidades de utilidad (ej. `.retro-grid`, `.scanlines`) y aplicarlas a contenedores principales.
4.  **Refactorizar Páginas:** Ajustar los estilos de las páginas existentes para alinearse con el nuevo tema, manteniendo la estructura semántica de HTML.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `apps/frontend/src/app/globals.css` | Modified | Definición de variables CSS retro y utilidades de efectos. |
| `apps/frontend/src/components/ui/*` | Modified | Actualización de estilos de componentes shadcn/ui (Button, Card, Input, etc.). |
| `apps/frontend/src/app/(auth)/login/page.tsx` | Modified | Aplicación de estilos retro a la página de login. |
| `apps/frontend/src/app/dashboard/layout.tsx` | Modified | Aplicación de estilos retro al layout del dashboard. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Inconsistencia visual entre componentes | Medio | Revisar todos los componentes de la UI y estandarizar los estilos retro. |
| Problemas de accesibilidad (contraste de colores) | Bajo | Seleccionar colores con contraste adecuado y verificar con herramientas de accesibilidad. |
| Complejidad en la mantenibilidad de estilos | Medio | Utilizar variables CSS y utilidades de Tailwind para centralizar los estilos. |

## Rollback Plan

1.  Restaurar el archivo `apps/frontend/src/app/globals.css` desde el control de versiones.
2.  Restaurar los archivos de componentes `apps/frontend/src/components/ui/*` desde el control de versiones.
3.  Restaurar las páginas modificadas desde el control de versiones.

## Dependencies

- Next.js 15
- React 19
- Tailwind 4

## Success Criteria

- [ ] La aplicación muestra un diseño visual coherente con estilo retro (años 80/90).
- [ ] Los componentes de la UI (Button, Card, Input) tienen un aspecto retro distintivo.
- [ ] Las páginas de Login y Dashboard utilizan el nuevo tema visual.
- [ ] El modo oscuro/claro funciona correctamente con la paleta retro.