# Hello World Frontend 🌐

[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-61DAFB)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Package Manager](https://img.shields.io/badge/pnpm-F69220)](https://pnpm.io)

**Hello World Frontend** es la aplicación web desarrollada en **Next.js 15** que sirve como interfaz administrativa para profesores y estudiantes. Permite gestionar videojuegos educativos, seguir el progreso de estudiantes y configurar aspectos pedagógicos.

[![PRD](https://img.shields.io/badge/PRD-v0.1.0--draft-1a1b26)](PRD.md)

> **Documento de requisitos:** Consulta el [PRD](./PRD.md) para la especificación completa de funcionalidades, criterios de aceptación y flujos de usuario.

## 📖 Descripción del Proyecto

Hello World Frontend es el **centro de comando** del ecosistema Hello World — la interfaz administrativa desde donde los profesores orquestan experiencias educativas, monitorean el progreso en tiempo real y toman decisiones pedagógicas informadas.

El dashboard convierte a cada profesor en un **arquitecto del aprendizaje**, con herramientas para diseñar contenido, visibilidad total del progreso estudiantil y datos accionables — todo sin escribir código.

### Funcionalidades por Prioridad

**P0 — MVP/GA (Fase 1):**
- **Autenticación UI**: Login/registro con JWT vía cookies httpOnly, protección de rutas por rol
- **Dashboard de Progreso**: Métricas aggregate, listado de estudiantes con drill-down individual, detección de estudiantes atascados
- **Gestión de Cursos**: CRUD completo de juegos, niveles y configuración pedagógica
- **Configuración de Juegos/Niveles**: Metadatos, segmentos, reordenamiento drag & drop

**P1 — Post-MVP (Fase 2):**
- **Analytics Dashboard**: Gráficos Recharts con filtros, distribución de errores, tendencias de engagement
- **Exportación de Reportes**: Exportación CSV/PDF de progreso y analytics
- **Panel de Administración**: Gestión de usuarios, roles, logs de auditoría

**P2 — Futuro (Fase 3):**
- **UI de Sincronización LMS**: Conexión con Moodle/Canvas
- **Configuración de Accesibilidad**: Tamaño de fuente, alto contraste
- **Editor de Contenido con Vista Previa**: WYSIWYG-like para descripciones de nivel

### 🎯 Filosofía del Producto: Teacher Empowerment

El dashboard se fundamenta en un principio rector: **el profesor es el experto, la tecnología lo potencia, no lo reemplaza**.

| Principio | Manifestación |
|-----------|---------------|
| **Control pedagógico** | El profesor decide qué estudiantes acceden a qué contenido, cuándo y con qué parámetros |
| **Visibilidad total** | Cada clic, error y acierto del estudiante es visible — no más "no sé cómo le está yendo" |
| **Creación sin código** | Crear juegos, niveles y configuraciones educativas sin escribir una línea de código |
| **Decisiones basadas en datos** | Analítica que responde preguntas concretas: "¿quién está atascado?", "¿qué nivel es demasiado difícil?" |
| **Automatización de lo repetitivo** | Exportación de reportes, sincronización con LMS, gestión de usuarios |

**Personas objetivo:**

- **Profesor** (primaria) — Docente de computación, NO desarrollador. Necesita crear contenido y monitorear estudiantes diariamente.
- **Administrador** (secundaria) — Jefe de departamento o coordinador. Necesita visibilidad cross-classroom y reportes institucionales.

---

## 🛠️ Tech Stack

| Tecnología | Propósito |
|------------|-----------|
| **Next.js 15.5.4** | Framework React con App Router |
| **React 19.1.0** | Biblioteca de UI |
| **TypeScript 5** | Tipado estático |
| **Tailwind CSS 4** | Estilos |
| **shadcn/ui** | Componentes UI |
| **Zod 4** | Validación de esquemas |
| **pnpm** | Gestor de paquetes |
| **@dnd-kit** | Drag & Drop |
| **Recharts 2.15.4** | Gráficos y estadísticas |
| **Zustand 5** | Gestión de estado |
| **Vitest** | Testing unitario |
| **Playwright** | Testing E2E |
| **Vercel AI SDK** | (Preparado para features de IA) |

---

## 📁 Estructura del Proyecto

```
apps/frontend/
├── .next/                   # Build generado (no versionar)
├── .vscode/                 # Config de VS Code
├── public/                  # Archivos estáticos
├── src/
│   ├── adapters/            # Adaptadores y wrappers de API
│   ├── app/                 # App Router (Next.js 15)
│   │   ├── (auth)/         # Rutas de autenticación
│   │   │   ├── login/      # Login page
│   │   │   └── register/   # Registro page
│   │   ├── (landing-page)/ # Páginas de landing
│   │   ├── admin/          # Panel de admin
│   │   ├── dashboard/      # Dashboard principal
│   │   ├── actions/        # Server Actions
│   │   ├── docs/           # Documentación
│   │   ├── layout.tsx      # Root layout
│   │   ├── error.tsx       # Manejo de errores
│   │   ├── not-found.tsx   # Página 404
│   │   └── globals.css     # Estilos globales
│   ├── components/
│   │   ├── ui/             # Componentes shadcn/ui
│   │   ├── account/        # Componentes de cuenta
│   │   ├── auth/           # Componentes de autenticación
│   │   ├── charts/         # Componentes de gráficos
│   │   ├── dashboard/      # Componentes del dashboard
│   │   ├── docs/           # Componentes de documentación
│   │   ├── editor/         # Editor de contenido
│   │   ├── export/         # Funcionalidades de exportación
│   │   ├── landing/        # Componentes de landing
│   │   ├── metrics/        # Componentes de métricas
│   │   ├── reports/        # Reportes
│   │   ├── settings/       # Configuración
│   │   ├── shared/         # Componentes compartidos
│   │   ├── student/        # Componentes de estudiante
│   │   └── theme/          # Sistema de temas
│   ├── context/            # React Context providers
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utilidades
│   │   ├── utils.ts        # cn() utility
│   │   ├── api.ts          # Configuración de API
│   │   └── constants.ts    # Constantes globales
│   ├── services/           # Capa de servicios API
│   ├── types/              # Definiciones TypeScript
│   └── adapters/           # Adaptadores de datos/API
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

## 📊 Estado del Proyecto

Mapeo de funcionalidades contra el [PRD](./PRD.md):

| Feature | ID PRD | Prioridad | Fase | Estado |
|---------|--------|-----------|------|--------|
| Autenticación UI (Login/Registro) | F-01 | P0 | Fase 1 | 🟡 En desarrollo |
| Dashboard de Progreso Estudiantil | F-02 | P0 | Fase 1 | 🟡 En desarrollo |
| Gestión de Cursos (Creación/Edición) | F-03 | P0 | Fase 1 | 🟡 En desarrollo |
| Configuración de Juegos y Niveles | F-04 | P0 | Fase 1 | 🟡 En desarrollo |
| Analytics Dashboard (Gráficos) | F-05 | P1 | Fase 2 | ⬜ Planificado |
| Exportación de Reportes CSV/PDF | F-06 | P1 | Fase 2 | ⬜ Planificado |
| Panel de Administración | F-07 | P1 | Fase 2 | ⬜ Planificado |
| UI de Sincronización LMS | F-08 | P2 | Fase 3 | ⬜ Planificado |
| Configuración de Accesibilidad | F-09 | P2 | Fase 3 | ⬜ Planificado |
| Editor de Contenido con Vista Previa | F-10 | P2 | Fase 3 | ⬜ Planificado |

> **Leyenda:** 🟡 En desarrollo · ✅ Completado · ⬜ Planificado · 🔴 Bloqueado

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

# Type checking
pnpm run typecheck

# Tests unitarios
pnpm run test

# Tests en watch mode
pnpm run test:watch

# Tests con cobertura
pnpm run test:coverage
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

Mapeo completo de rutas contra el [PRD](./PRD.md) (Sección 6):

| Ruta | Descripción | Rol | PRD |
|------|-------------|-----|-----|
| `/` | Landing page pública | Todos | — |
| `/login` | Inicio de sesión | No auth | F-01 |
| `/register` | Registro de profesor | No auth | F-01 |
| `/dashboard` | Dashboard principal con resumen | Profesor | F-02 |
| `/dashboard/courses` | Gestión de cursos/juegos | Profesor | F-03 |
| `/dashboard/courses/[id]` | Detalle y configuración del juego | Profesor | F-03, F-04 |
| `/dashboard/students` | Lista de estudiantes | Profesor | F-02 |
| `/dashboard/students/[id]` | Progreso detallado del estudiante | Profesor | F-02 |
| `/dashboard/analytics` | Analytics y gráficos (P1) | Profesor | F-05 |
| `/dashboard/reports` | Exportación de reportes (P1) | Profesor | F-06 |
| `/dashboard/settings` | Configuración del profesor (P1) | Profesor | — |
| `/admin` | Panel de administración | Admin | F-07 |
| `/admin/users` | Gestión de usuarios (P1) | Admin | F-07 |
| `/admin/audit` | Logs de auditoría (P1) | Admin | F-07 |
| `/admin/settings` | Configuración del sistema (P2) | Admin | — |
| `/docs` | Documentación interna | Todos | — |

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [PRD.md](PRD.md) | Documento de requisitos del producto (autoritativo) |
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
