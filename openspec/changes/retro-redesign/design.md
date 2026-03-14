# Technical Design: Retro Redesign

## 1. Estructura de archivos

### 1.1. Ubicación de estilos globales
- **Archivo**: `apps/frontend/src/app/globals.css`
  - Definición de variables CSS para el tema retro (colores, fuentes, espaciado).
  - Configuración de utilidades de Tailwind 4 (fondos, bordes, texto).
  - Definición de utilidades personalizadas para efectos (scanlines, grid).

### 1.2. Componentes de tema
- **Directorio**: `apps/frontend/src/components/theme/`
  - `ThemeProvider.tsx`: Componente proveedor de contexto para el tema (light/dark).
  - `useTheme.ts`: Hook personalizado para acceder al estado del tema.
  - `theme-toggle.tsx`: Botón para alternar entre modos.

### 1.3. Estilos de componentes UI
- **Directorio**: `apps/frontend/src/components/ui/`
  - Modificar archivos existentes de shadcn/ui (Button, Card, Input, etc.) para aplicar estilos retro.
  - Usar clases de utilidad de Tailwind definidas en `globals.css` (ej. `retro-btn`, `retro-card`).

### 1.4. Efectos visuales
- **Clases de utilidad** (en `globals.css`):
  - `.scanlines`: Efecto de líneas horizontales (pseudo-elementos).
  - `.retro-grid`: Patrón de fondo con cuadrícula sutil.
  - `.flat-shadow`: Sombra plana (sin desenfoque, solo desplazamiento).

## 2. Patrones de código

### 2.1. Aplicación de clases de Tailwind
- **Patrón**: Usar `@apply` dentro de componentes o clases de utilidad para mantener consistencia.
- **Ejemplo Button**:
  ```css
  .retro-btn {
    @apply border-4 border-black bg-amber-100 text-slate-900 px-4 py-2 font-mono uppercase tracking-wider shadow-none hover:bg-amber-200;
  }
  ```

### 2.2. Componentes con temas
- **Patrón**: Pasar clases condicionales basadas en el tema actual (light/dark).
- **Ejemplo**: `className={cn("bg-cream", theme === "dark" && "bg-slate-900")}`

### 2.3. Efectos con pseudo-elementos
- **Patrón**: Usar `::before` y `::after` para efectos como scanlines sin alterar el layout.
- **Ejemplo**:
  ```css
  .scanlines::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
      to bottom,
      transparent,
      transparent 2px,
      rgba(0, 0, 0, 0.1) 2px,
      rgba(0, 0, 0, 0.1) 4px
    );
    pointer-events: none;
    z-index: 9999;
  }
  ```

## 3. Decisiones técnicas

### 3.1. Variables CSS (Tailwind 4)
- **Uso**: Definir colores personalizados en `@theme` dentro de `globals.css`.
- **Implementación**:
  ```css
  @theme {
    --color-cream: #f4e4bc;
    --color-slate-dark: #2d2d2d;
    --color-amber-accent: #d97706;
    --font-mono-retro: 'Courier New', Courier, monospace;
  }
  ```

### 3.2. Componentes UI
- **Decisión**: Modificar componentes shadcn/ui existentes en lugar de crear nuevos, para mantener la estructura de código.
- **Enfoque**: Usar la propiedad `variant` para estilos retro (ej. `variant="retro"`).

### 3.3. Gestión del tema
- **Decisión**: Implementar un Context API simple para el tema (light/dark), compatible con Next.js 15 App Router.
- **Persistencia**: Usar `localStorage` para recordar la preferencia del usuario.

## 4. Implementación de efectos visuales

### 4.1. Patrón de cuadrícula (grid)
- **Técnica**: Usar `background-image` con `linear-gradient` para crear una cuadrícula sutil.
- **Código CSS**:
  ```css
  .retro-grid {
    background-image:
      linear-gradient(rgba(0, 0, 0, 0.1) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 0, 0, 0.1) 1px, transparent 1px);
    background-size: 20px 20px;
  }
  ```

### 4.2. Scanlines
- **Técnica**: Capa fija sobre la pantalla con `repeating-linear-gradient`.
- **Configuración**:
  - Opacidad baja (0.05-0.1) para no obstruir la lectura.
  - Alternar visibilidad mediante clase CSS (ej. `.scanlines-enabled`).

### 4.3. Sombras planas
- **Técnica**: Usar `box-shadow` con valores de desplazamiento pero sin desenfoque.
- **Ejemplo**:
  ```css
  .flat-shadow {
    box-shadow: 4px 4px 0px 0px rgba(0, 0, 0, 0.8);
  }
  ```

### 4.4. Animaciones de parpadeo (opcional)
- **Técnica**: Keyframes CSS para efecto de parpadeo en elementos destacados (ej. títulos).
- **Código**:
  ```css
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }
  .blink {
    animation: blink 2s infinite;
  }
  ```

## 5. Flujo de implementación (resumen)

1. **Definir variables CSS** en `globals.css` (`@theme`).
2. **Crear componentes de tema** (`ThemeProvider`, `useTheme`, `theme-toggle`).
3. **Actualizar componentes UI** con estilos retro (Button, Card, Input).
4. **Aplicar efectos visuales** (grid, scanlines) a contenedores principales.
5. **Refactorizar páginas** (Login, Dashboard) para usar el nuevo tema.

## 6. Verificación

- **Accesibilidad**: Verificar contraste de colores (WCAG AA).
- **Consistencia**: Revisar todos los componentes con el tema retro aplicado.
- **Rendimiento**: Los efectos de CSS deben ser eficientes (usar `transform` y `opacity` cuando sea posible).

---
**Estado**: Diseño técnico completado.
**Siguiente paso**: Crear el plan de tareas (tasks) para la implementación.
