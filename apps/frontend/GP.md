# Frontend

## Estructura de carpetas

```
src/
├── adapters/              # Adaptadores de datos (student.adapter.ts, professor.adapter.ts)
├── app/                   # Next.js App Router
│   ├── (auth)/           # Route groups
│   │   ├── login/
│   │   └── signup/
│   ├── (landing-page)/   # Landing page pública
│   ├── dashboard/        # Panel de control
│   │   ├── students/
│   │   ├── metrics/
│   │   ├── reports/
│   │   ├── account/
│   │   ├── notifications/
│   │   ├── settings/
│   │   └── help/
│   ├── admin/            # Panel de administración
│   ├── docs/             # Documentación
│   ├── error.tsx         # Manejador global de errores
│   ├── not-found.tsx     # Página 404
│   ├── loading.tsx       # Estado de carga
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Estilos globales
├── components/
│   ├── ui/               # shadcn/ui components (button, card, input, etc.)
│   ├── auth/             # Componentes de autenticación
│   ├── landing/          # Componentes de landing page
│   ├── dashboard/        # Componentes del dashboard
│   ├── student/          # Componentes de gestión de estudiantes
│   ├── metrics/          # Componentes de métricas y gráficos
│   ├── reports/          # Componentes de reportes
│   ├── docs/             # Componentes de documentación
│   └── shared/           # Componentes compartidos
│       ├── navigation/   # Navegación (nav-main, nav-user, etc.)
│       └── providers.tsx # Proveedores de contexto
├── hooks/                # Custom React hooks (use-notifications, use-mobile)
├── lib/                  # Utilidades
│   ├── utils.ts          # cn() y utilidades
│   ├── colors.ts         # Sistema de colores
│   ├── actions.ts        # Server Actions (login, signup, createStudent)
│   ├── api-client.ts     # Cliente API
│   └── create-api-client.ts
├── services/             # Servicios de API (student, professor, progress)
├── types/                # TypeScript types/interfaces
│   ├── api.ts
│   ├── student.interface.ts
│   └── professor.interface.ts
└── adapters/             # Adaptadores de datos
```

## Convención de nombres

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| **Components** | PascalCase | `StudentTable`, `LoginForm` |
| **Hooks** | camelCase + `use` prefix | `useNotifications`, `useMobile` |
| **Types/Interfaces** | PascalCase | `Student`, `ApiResponse<T>` |
| **Constants** | UPPER_SNAKE_CASE | `COLORS`, `API_BASE_URL` |
| **Functions** | camelCase | `handleSubmit`, `loadStudentData` |
| **Server Actions** | camelCase + `Action` suffix | `loginAction`, `createStudentAction` |
| **Files (components)** | kebab-case | `student-table.tsx`, `login-form.tsx` |
| **Files (utils)** | camelCase | `utils.ts`, `colors.ts` |

### Imports (Orden de prioridad)

1. React/Next imports
2. Third-party libraries
3. `@/components/ui/*` (shadcn components)
4. `@/components/*` (custom components)
5. `@/hooks/*`, `@/lib/*`, `@/types/*`
6. Relative imports (`./` last)

```tsx
import { useState } from "react";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { StudentTable } from "@/components/student";
import { useNotifications } from "@/hooks/use-notifications";
import { cn } from "@/lib/utils";
import StudentForm from "./student-form";
```

## Linting, indentación, formateo

### ESLint Config

Archivo: `eslint.config.mjs`

```javascript
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  
  {
    rules: {
      // Reglas de calidad
      "no-unused-vars": "warn",
      "no-console": "warn", 
      "no-debugger": "error",
      "no-unreachable": "error",
      
      // React best practices
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
      
      // TypeScript rules
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unused-vars": "warn",
      
      // Accessibility
      "jsx-a11y/alt-text": "warn",
      "jsx-a11y/anchor-has-content": "warn",
    },
    linterOptions: {
      reportUnusedDisableDirectives: true,
    },
  },
];

export default eslintConfig;
```

### Formato

| Regla | Valor |
|-------|-------|
| **Semicolons** | Siempre |
| **Quotes** | Double quotes |
| **Indentación** | 2 espacios |
| **Trailing commas** | En multi-line objects/arrays |
| **Max line length** | 100 caracteres |

### TypeScript (Strict mode habilitado)

- Siempre usar tipos de retorno explícitos en funciones
- Preferir `interface` sobre `type` para shapes de objetos
- Usar `type` para unions, tuples, mapped types
- Evitar `any` - usar `unknown` o generics

```tsx
// ✅ Correcto
interface StudentProps {
  id: string;
  name: string;
}

function processStudent(student: StudentProps): string {
  return student.name;
}

// ❌ Incorrecto
function processStudent(student: any) {
  return student.name;
}
```

## Manejo de errores

### Error Boundaries (Next.js App Router)

**`src/app/error.tsx`** - Error global de la aplicación:

```tsx
"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle, RefreshCw } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // eslint-disable-next-line no-console -- Log error for error reporting
    console.error("Application Error:", error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="max-w-md w-full">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-destructive/10">
            <AlertCircle className="h-6 w-6 text-destructive" />
          </div>
          <CardTitle className="text-2xl">Algo salió mal</CardTitle>
          <CardDescription>
            Ha ocurrido un error inesperado en la aplicación.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {process.env.NODE_ENV === "development" && (
            <div className="rounded-md bg-muted p-3">
              <p className="text-sm font-mono text-muted-foreground">
                {error.message}
              </p>
              {error.digest && (
                <p className="text-xs text-muted-foreground mt-1">
                  Error ID: {error.digest}
                </p>
              )}
            </div>
          )}
          
          <div className="flex flex-col gap-2">
            <Button onClick={reset} className="w-full">
              <RefreshCw className="mr-2 h-4 w-4" />
              Intentar nuevamente
            </Button>
            <Button 
              variant="outline" 
              onClick={() => window.location.href = "/"}
              className="w-full"
            >
              Volver al inicio
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

**`src/app/not-found.tsx`** - Página 404:

```tsx
"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FileQuestion, Home } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="max-w-md w-full">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-muted">
            <FileQuestion className="h-6 w-6 text-muted-foreground" />
          </div>
          <CardTitle className="text-2xl">Página no encontrada</CardTitle>
          <CardDescription>
            La página que buscas no existe o ha sido movida.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col gap-2">
            <Button asChild className="w-full">
              <a href="/dashboard">
                <Home className="mr-2 h-4 w-4" />
                Ir al Dashboard
              </a>
            </Button>
            <Button 
              variant="outline" 
              onClick={() => window.history.back()}
              className="w-full"
            >
              Volver atrás
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

### Server Actions Pattern

```tsx
"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";

const schema = z.object({
  email: z.string().email(),
});

export type ActionState = {
  message?: string;
  errors?: Record<string, string[]>;
  success?: boolean;
};

export async function myAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validated = schema.safeParse({
      email: formData.get("email"),
    });
    
    if (!validated.success) {
      return {
        success: false,
        message: "Validation failed",
        errors: validated.error.flatten().fieldErrors,
      };
    }
    
    // Business logic here
    revalidatePath("/path");
    return { success: true, message: "Success!" };
    
  } catch (_error) {
    return {
      success: false,
      message: "Something went wrong",
    };
  }
}
```

### Principios de manejo de errores

- Usar `try/catch` en funciones async
- Prefijar variables catch no usadas con `_` (e.g., `_error`)
- Retornar estados de error, no lanzar en Server Actions
- Usar Sonner toast para errores visibles al usuario

```tsx
try {
  await riskyOperation();
} catch (_error) {
  toast.error("Operation failed");
}
```

---

# Pruebas

> **Estado actual**: No hay framework de pruebas configurado.

### Recomendación para implementar pruebas

Para agregar pruebas al proyecto, instalar uno de los siguientes frameworks:

**Opción 1: Vitest + React Testing Library (Recomendado)**

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

**Opción 2: Jest + React Testing Library**

```bash
npm install -D jest @testing-library/react @testing-library/jest-dom jest-environment-jsdom
```

**Opción 3: Playwright (E2E)**

```bash
npm install -D @playwright/test
```

### Estructura de pruebas sugerida

```
src/
├── __tests__/            # Tests unitarios
│   ├── components/
│   ├── hooks/
│   └── lib/
├── e2e/                  # Tests E2E (Playwright)
└── test/
    └── setup.ts          # Configuración de tests
```

### Configuración de Vitest (recomendada)

`vitest.config.ts`:

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

`src/test/setup.ts`:

```typescript
import '@testing-library/jest-dom';
```

### Scripts a agregar en `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test"
  }
}
```
