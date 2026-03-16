# Hello World Frontend 🌐

[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-61DAFB)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Package Manager](https://img.shields.io/badge/pnpm-F69220)](https://pnpm.io)

**Hello World Frontend** es la aplicación web desarrollada en **Next.js 15** que sirve como interfaz administrativa para profesores y estudiantes. Permite gestionar videojuegos educativos, seguir el progreso de estudiantes y configurar aspectos pedagógicos.

## 📖 Descripción del Proyecto

El frontend proporciona:

- **Panel de Profesores**: Crear y gestionar videojuegos, niveles y configuraciones
- **Panel de Estudiantes**: Ver progreso, acceder a juegos, dejar feedback
- **Dashboard**: Estadísticas y métricas de aprendizaje
- **Sistema de Autenticación**: Login seguro con JWT
- **Diseño Responsive**: Adaptable a diferentes dispositivos

---

## 🛠️ Tech Stack

| Tecnología | Propósito |
|------------|-----------|
| **Next.js 15** | Framework React con App Router |
| **React 19** | Biblioteca de UI |
| **TypeScript 5** | Tipado estático |
| **Tailwind CSS 4** | Estilos |
| **shadcn/ui** | Componentes UI |
| **Zod 4** | Validación de esquemas |
| **pnpm** | Gestor de paquetes |
| **@dnd-kit** | Drag & Drop |
| **Recharts** | Gráficos y estadísticas |
| **Vercel AI SDK** | (Preparado para features de IA) |

---

## 📁 Estructura del Proyecto

```
apps/frontend/
├── .next/                   # Build generado (no versionar)
├── .vscode/                 # Config de VS Code
├── public/                  # Archivos estáticos
├── src/
│   ├── app/                 # App Router (Next.js 15)
│   │   ├── (auth)/         # Rutas de autenticación
│   │   │   ├── login/      # Login page
│   │   │   └── register/   # Registro page
│   │   ├── (dashboard)/    # Rutas protegidas
│   │   │   ├── admin/      # Panel de admin
│   │   │   ├── professor/  # Panel de profesor
│   │   │   └── student/    # Panel de estudiante
│   │   ├── api/            # API Routes (Server Actions)
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Home page
│   ├── components/
│   │   ├── ui/             # Componentes shadcn/ui
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   └── ...
│   │   ├── auth/           # Componentes de auth
│   │   ├── dashboard/      # Componentes del dashboard
│   │   └── game/           # Componentes de juego
│   ├── hooks/              # Custom React hooks
│   │   ├── use-auth.ts     # Hook de autenticación
│   │   └── use-game.ts     # Hook de estado de juego
│   ├── lib/                # Utilidades
│   │   ├── utils.ts        # cn() utility
│   │   ├── api.ts          # Configuración de API
│   │   └── constants.ts    # Constantes globales
│   ├── services/           # Capa de servicios API
│   │   ├── auth-service.ts
│   │   ├── game-service.ts
│   │   └── user-service.ts
│   ├── types/              # Definiciones TypeScript
│   │   ├── user.types.ts
│   │   ├── game.types.ts
│   │   └── api.types.ts
│   └── styles/
│       └── globals.css     # Estilos globales
├── .env                    # Variables de entorno
├── .env.example            # Ejemplo de variables
├── components.json         # Config de shadcn/ui
├── eslint.config.mjs      # Config de ESLint
├── next.config.ts         # Config de Next.js
├── package.json            # Dependencias
├── postcss.config.mjs     # Config de PostCSS
├── tailwind.config.ts     # Config de Tailwind
├── tsconfig.json          # Config de TypeScript
└── README.md              # Este archivo
```

---

## 🚀 Getting Started

### Prerrequisitos

- **Node.js 18+**
- **pnpm** (gestor de paquetes)
- **Backend corriendo** (ver `apps/backend/README.md`)

### Instalación

1. **Instalar pnpm** (si no lo tienes):
   ```bash
   npm install -g pnpm
   ```

2. **Clonar y navegar al proyecto:**
   ```bash
   git clone https://github.com/tu-usuario/hello-world-project.git
   cd hello-world-project/apps/frontend
   ```

3. **Instalar dependencias:**
   ```bash
   pnpm install
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con la URL del backend
   ```

5. **Ejecutar el servidor de desarrollo:**
   ```bash
   pnpm run dev
   ```

6. **Abrir en el navegador:**
   ```
   http://localhost:3000
   ```

---

## 📝 Scripts Disponibles

```bash
# Desarrollo (con Turbopack)
pnpm run dev

# Build de producción
pnpm run build

# Iniciar producción
pnpm run start

# Linting
pnpm run lint

# type-check
pnpm run type-check
```

---

## 🔐 Autenticación

### Flujo de Login

1. Usuario ingresa credenciales en `/login`
2. Frontend envía credentials al backend
3. Backend retorna JWT token
4. Frontend almacena token en cookies/httpOnly
5. Token se incluye en headers de requests subsiguientes

### Roles de Usuario

| Rol | Ruta | Permisos |
|-----|------|----------|
| `admin` | `/admin` | Gestión completa del sistema |
| `professor` | `/professor` | Crear/editar juegos, ver estudiantes |
| `student` | `/student` | Ver progreso, jugar |

### Ejemplo de Server Action

```typescript
'use server'

import { z } from 'zod'

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export async function loginAction(formData: FormData) {
  const data = LoginSchema.parse({
    email: formData.get('email'),
    password: formData.get('password'),
  })
  
  const response = await fetch(`${process.env.API_URL}/auth/login`, {
    method: 'POST',
    body: new URLSearchParams(data),
  })
  
  if (!response.ok) {
    throw new Error('Credenciales inválidas')
  }
  
  return response.json()
}
```

---

## 🎨 Convenciones de Código

### Componentes React

```typescript
// ✅ CORRECTO: Server Component por defecto
export async function DashboardPage() {
  const data = await fetchData()
  return <Dashboard data={data} />
}

// ❌ INCORRECTO: "use client" solo cuando es necesario
'use client'

export function ClientComponent() {
  const [state, setState] = useState(0)
  return <button onClick={() => setState(s => s + 1)}>Click</button>
}
```

### Estilos con Tailwind

```typescript
// ✅ CORRECTO: Usar cn() utility
import { cn } from '@/lib/utils'

<div className={cn(
  "base-class",
  isActive && "active-class",
  variant === 'primary' ? "bg-blue-500" : "bg-gray-500"
)} />

// ❌ INCORRECTO: var() en className
<div className="bg-[var(--primary)]" />
```

### Validación con Zod

```typescript
// ✅ CORRECTO: Esquemas explícitos
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2).max(100),
  email: z.string().email(),
  role: z.enum(['admin', 'professor', 'student']),
})

// ✅ CORRECTO: Tipos derivados
type User = z.infer<typeof UserSchema>
```

### TypeScript

```typescript
// ✅ CORRECTO: Interfaces para objetos
interface User {
  id: string
  name: string
  email: string
}

// ✅ CORRECTO: Types para unions
type UserRole = 'admin' | 'professor' | 'student'

// ✅ CORRECTO: Return types explícitos
function getUser(id: string): Promise<User> {
  return fetch(`/api/users/${id}`).then(res => res.json())
}

// ❌ INCORRECTO: any
const data: any = fetchData()
```

---

## 🔌 Integración con API

### API Client

El proyecto usa el paquete `@workspace/api-client-ts` para comunicarse con el backend:

```typescript
import { ApiClient } from '@workspace/api-client-ts'

const api = new ApiClient({
  baseUrl: process.env.NEXT_PUBLIC_API_URL!,
})

// Ejemplo de uso
const user = await api.users.getById('123')
const games = await api.games.list()
```

### Server Actions

Todas las mutaciones usan Server Actions:

```typescript
// src/app/api/games/create-game.ts
'use server'

import { z } from 'zod'
import { api } from '@/services/api'

const CreateGameSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().optional(),
  subject: z.string().optional(),
})

export async function createGame(formData: FormData) {
  const gameData = CreateGameSchema.parse({
    title: formData.get('title'),
    description: formData.get('description'),
    subject: formData.get('subject'),
  })
  
  await api.games.create(gameData)
  revalidatePath('/professor/games')
}
```

---

## 🧪 Testing

### Configuración de Tests

El proyecto está preparado para testing con **Playwright** y Vitest.

```bash
# Ejecutar tests E2E
pnpm run test:e2e

# Ejecutar tests con coverage
pnpm run test:coverage
```

---

## 📱 UI/UX

### Componentes shadcn/ui

El proyecto usa **shadcn/ui** como base de componentes:

| Componente | Uso |
|------------|-----|
| Button | Botones de acción |
| Card | Contenedores de contenido |
| Dialog | Modales y popups |
| Input | Campos de formulario |
| Select | Dropdowns |
| Table | Listas y data grids |
| Tabs | Navegación por pestañas |
| Toast | Notificaciones |

### Tema

El proyecto usa un tema **Blue-Noir** con acentos en azul y negro. Los colores se configuran en Tailwind.

---

## 🌐 Rutas del Frontend

```
/                           # Landing page (público)
/login                      # Login de usuario
/register                   # Registro (profesor)
/dashboard                  # Redirect según rol
/dashboard/admin            # Panel de admin
/dashboard/professor        # Panel de profesor
/dashboard/professor/games # Gestión de juegos
/dashboard/professor/students # Gestión de estudiantes
/dashboard/student         # Panel de estudiante
/dashboard/student/progress # Ver progreso
```

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [docs/api.md](../packages/api-client-ts/docs/) | Documentación del API Client |
| [AGENTS.md](AGENTS.md) | Guías para agentes IA |
| [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) | Optimizaciones de rendimiento |

---

## 🤝 Contribuciones

1. Fork el repositorio
2. Crea tu rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega feature'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### Normas de Contribución

- ✅ UI en **español**
- ✅ Server Actions para mutaciones
- ✅ Zod para validación
- ✅ cn() para clases de Tailwind
- ✅ TypeScript estricto
- ❌ NO `useMemo` / `useCallback` (confía en React Compiler)
- ❌ NO `any` (usa `unknown` o genéricos)

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

---

## 🌍 Links

- **Website**: [hello-world-project.dev](https://hello-world-project.dev)
- **Backend**: [github.com/.../apps/backend](https://github.com/tu-usuario/hello-world-project/apps/backend)
- **Game**: [github.com/.../apps/game](https://github.com/tu-usuario/hello-world-project/apps/game)
- **API Client**: [github.com/.../packages/api-client-ts](https://github.com/tu-usuario/hello-world-project/packages/api-client-ts)
