# Specs — courses-business-rules

**Estado**: ✅ Completado  
**Última actualización**: 2026-05-20

> Documento de especificaciones formales para el cambio de reglas de negocio de Cursos.
>
> **Fuente de verdad**: el código confirmado en `apps/backend/` y `apps/frontend/`, complementado por la propuesta `proposal.md`.
>
> **Estado de arte**: al momento de escribir estas specs ya existe `game_id` en el modelo y columna PostgreSQL, pero NO está expuesto en schemas de request/response ni en el frontend.

---

## UC-1 — Profesor solo ve sus cursos en el listado

### Problema
El endpoint `GET /api/v1/courses/management` recibe `professor_id` como query param opcional. Si no se envía, retorna **todos** los cursos de la plataforma. Un profesor no autenticado o malintencionado podría navegar a la ruta y ver datos de otros docentes.

### Regla de Negocio
> RN-1: Todo profesor autenticado recibe, sin requerir acción explícita, solo los cursos donde figura como profesor titular.  
> RN-2: Un administrador recibe todos los cursos sin filtro.  
> RN-3: El filtro es aplicado por el backend; el frontend NO envía `professor_id` en query params.

### Given/When/Then

**Escenario 1: Profesor accede al listado sin query params**

- **Given** un usuario autenticado con rol `"professor"`
- **When** accede a `GET /api/v1/courses/management` sin `professor_id` en query
- **Then** el backend resuelve `Professor.id` desde `User.id` vía `get_professor_profile_ids`
- **And** se aplica el filtro `Course.id IN (SELECT course_id FROM course_professors WHERE professor_id = <id>)`
- **And** NO se retornan cursos donde el profesor no esté asignado

**Escenario 2: Admin accede al listado sin query params**

- **Given** un usuario autenticado con rol `"admin"`
- **When** accede a `GET /api/v1/courses/management` sin `professor_id`
- **Then** el backend NO aplica ningún filtro de profesor
- **And** se retornan todos los cursos activos

**Escenario 3: Admin pasa `professor_id` explícitamente**

- **Given** un administrador
- **When** envía `GET /api/v1/courses/management?professor_id=<uuid>`
- **Then** se retornan los cursos de ese profesor específico (override)

**Escenario 4: Profesor envía `professor_id` explícitamente (override ignorado)**

- **Given** un profesor autenticado
- **When** envía `GET /api/v1/courses/management?professor_id=<uuid-de-otro>`
- **Then** el backend ignora el query param y aplica el filtro sobre su propio `Professor.id`

---

## UC-2 — Profesor autoseleccionado al crear curso

### Problema
Actualmente el `CourseForm` envía `professorIds: JSON.stringify([])` y el `CreateCourseUseCase` crea el curso sin profesores si el array está vacío. El profesor debe poder crear un curso sin tener que buscarse a sí mismo en el multiselect.

### Regla de Negocio
> RN-4: Al crear un curso, el `CreateCourseUseCase` inyecta automáticamente al profesor logueado en `professor_ids`, incluso si el frontend envía el array vacío.  
> RN-5: El profesor puede agregar profesores adicionales explícitamente (no duplicados).  
> RN-6: No hay modo de desasignar al profesor titular al crear el curso (siempre está incluido).

### Given/When/Then

**Escenario 1: Profesor crea curso sin enviar profesorIds**

- **Given** un profesor logueado creando un curso nuevo
- **And** envía `professorIds: []` desde el frontend
- **When** el `CreateCourseUseCase.execute()` procesa el request
- **Then** el sistema detecta rol = `"professor"`
- **And** convierte `current_user.id` → `Professor.id` vía `get_professor_profile_ids([current_user.id])`
- **And** agrega ese `professor_id` a la lista de `valid_professor_ids` antes de `bulk_create_professors`
- **And** el curso se crea con el profesor como profesor titular

**Escenario 2: Profesor crea curso agregándose a sí mismo explícitamente**

- **Given** un profesor logueado envía `professorIds: [<su-propio-user-id>]`
- **When** el usecase procesa el request
- **And** el `current_user.id` también es agregado automáticamente
- **Then** el sistema **no duplica** la entrada en `course_professors`
- **And** el curso tiene exactamente una entrada para ese profesor

**Escenario 3: Profesor crea curso con profesores adicionales**

- **Given** un profesor logueado envía `professorIds: [<user-id-de-compañero>]`
- **When** el usecase procesa el request
- **Then** el curso se crea con el profesor logueado Y el profesor adicional
- **And** ambos tienen entradas separadas en `course_professors`

**Escenario 4: Admin crea curso**

- **Given** un administrador autenticado (`role = "admin"`)
- **When** crea un curso
- **Then** el usecase NO agrega ningún profesor automáticamente
- **And** usa solo los `professorIds` enviados por el frontend

---

## UC-3 — Select de juegos en el formulario de crear/editar curso

### Problema
El modelo `Course` ya tiene `game_id: UUID FK → games.id` en la tabla PostgreSQL, pero los schemas Pydantic `CourseCreateRequest`, `CourseUpdateRequest`, `CourseResponse` y `CourseDetailResponse` lo excluyen. El frontend no permite seleccionar un juego y la tabla de cursos no muestra la columna correspondiente.

### Regla de Negocio
> RN-7: Todo curso puede estar asociado opcionalmente a un juego del catálogo de la plataforma.  
> RN-8: `game_id` es `nullable`: cursos existentes sin juego se mantienen válidos.  
> RN-9: La asociación juego → curso es 1:N (un juego puede ser asignado a múltiples cursos).  
> RN-10: El frontend carga las opciones desde `GET /api/v1/games` cada vez que abre el formulario (sin cache obligatoria del lado del cliente).

### Given/When/Then

**Escenario 1: Formulario de creación carga opciones de juegos**

- **Given** el usuario abre el modal "Crear Curso"
- **When** el `CourseForm` se monta en modo creación
- **Then** se dispara `GET /api/v1/games` (o se recibe como prop desde el servidor)
- **And** se renderiza un `<Select>` con la lista de juegos disponibles
- **And** el `<Select>` muestra "Sin juego" como opción default (`value = ""`)

**Escenario 2: Profesor asocia un juego al crear curso**

- **Given** el modal de creación abierto con juegos cargados
- **And** el profesor selecciona "Aventura Espacial" (gameId = `<uuid-1>`)
- **When** envía el formulario
- **Then** el body incluye `gameId: "<uuid-1>"`
- **And** el `CourseCreateRequest` recibe y valida `game_id`
- **And** el `Course` se guarda con `game_id = <uuid-1>`
- **And** el `CourseDetailResponse` retorna `CourseResponse` con `game_id` poblado

**Escenario 3: Profesor deja el juego vacío al crear**

- **Given** el modal de creación abierto
- **And** el profesor no selecciona ningún juego (valor default = `""`)
- **When** envía el formulario
- **Then** `game_id` se envía como `null` o ausente del body
- **And** el curso se crea con `game_id = NULL` en la base

**Escenario 4: Editor modifica juego de un curso existente**

- **Given** un curso con `game_id = NULL`
- **When** un profesor abre el modal de edición y selecciona un juego
- **Then** el `CourseUpdateRequest` incluye `game_id: <uuid>`
- **And** el registro en `courses` se actualiza con el nuevo `game_id`

**Escenario 5: Tabla de cursos muestra columna Juego**

- **Given** la lista de cursos se renderiza en `course-table.tsx`
- **When** cada curso tiene o no un `gameId` asociado
- **Then** la tabla muestra una columna "Juego"
- **And** si `gameId` existe: muestra el título del juego
- **And** si `gameId` es `null`: muestra "—" o "Sin juego"

---

## Implementation — Backend

### B-1: `CourseCreateRequest` y `CourseUpdateRequest` — agregar `game_id`

**Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`

```python
# Agregar a CourseCreateRequest (después de professor_ids):
game_id: Optional[UUID] = Field(None, alias="gameId")

# Agregar a CourseUpdateRequest (después de is_active):
game_id: Optional[UUID] = Field(None, alias="gameId")
```

**Nota**: `CourseUpdateRequest` usa `model_config = {"populate_by_name": True}` ya existente; el alias `gameId` se mapea a `game_id` en el modelo internamente sin intervención adicional.

---

### B-2: `CourseResponse` y `CourseDetailResponse` — exponer `game_id`

**Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`

```python
class CourseResponse(BaseModel):
    # ... campos existentes ...
    game_id: Optional[UUID] = Field(None, alias="gameId")

class CourseDetailResponse(CourseResponse):
    # ... campos existentes ...
    # Hereda game_id de CourseResponse automáticamente
```

---

### B-3: Endpoint `GET /api/v1/courses/management` — inyectar `current_user`, filtrar por profesor

**Archivo**: `apps/backend/src/course/api/v1/endpoints/course_management.py`

```python
# 1. Importar get_current_user y el enum de roles
from src.auth.infrastructure.dependencies import get_current_user
from src.shared.domain.enums import UserRole  # o donde esté definido

# 2. Modificar la firma del endpoint:
@router.get("", response_model=PaginatedCourseListResponse)
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    professor_id: Optional[UUID] = None,
    school_year: Optional[str] = None,
    current_user: User = Depends(get_current_user),  # NUEVO
):
    # 3. Si es profesor, resolver su Professor.id automáticamente:
    if current_user.role == "professor" and not professor_id:
        professor_id_map = await course_repo.get_professor_profile_ids([current_user.id])
        professor_id = professor_id_map.get(current_user.id)
    
    courses, total = await course_repo.list_with_counts(
        professor_id=professor_id,
        school_year=school_year,
        skip=skip,
        limit=limit,
    )
    # ... resto del método ...
```

**Nota**: `get_professor_profile_ids([current_user.id])` ya existe en `course_repository.py:132`. Devuelve `dict[User.id, Professor.id]`. Si el usuario no tiene perfil de profesor (edge case), retorna `{}` → `professor_id` queda `None` → el endpoint retorna vacío o todos, según la lógica existente.

---

### B-4: `CreateCourseUseCase` — autoselección del profesor logueado

**Archivo**: `apps/backend/src/course/application/usecase/create_course_usecase.py`

```python
from src.course.infrastructure.course_repository import CourseRepository
from src.shared.domain.enums import UserRole  # o donde esté definido

class CreateCourseUseCase:
    def __init__(self, db: AsyncSession, course_repo: CourseRepository, current_user: User):
        self.db = db
        self.course_repo = course_repo
        self.current_user = current_user  # NUEVO

    async def execute(self, request: CourseCreateRequest) -> CourseDetailResponse:
        async with self.db.begin():
            # ... validación de duplicado existente ...

            course_data = request.model_dump(
                exclude={"student_ids", "professor_ids"},
                by_alias=False,
            )
            # game_id ahora viene en request (lo incluye model_dump por defecto)
            course = Course(**course_data)
            self.db.add(course)
            await self.db.flush()

            # Autoselección de profesor si el usuario es profesor
            professor_ids = list(request.professor_ids) if request.professor_ids else []
            if self.current_user.role == "professor":
                professor_id_map = await self.course_repo.get_professor_profile_ids(
                    [self.current_user.id]
                )
                my_professor_id = professor_id_map.get(self.current_user.id)
                if my_professor_id and my_professor_id not in professor_ids:
                    professor_ids.append(my_professor_id)

            if professor_ids:
                await self.course_repo.bulk_create_professors(course.id, professor_ids)

            # ... resto del método (estudiantes, build response) ...
```

**Nota**: `get_profile_id_by_user_id` en `course_repository.py:502` es un método auxiliar que podría usarse como alternativa para un solo ID en lugar de `get_professor_profile_ids([id])`.

---

### B-5: Migración Alembic — verificar existencia de `game_id`

**Comando**:
```bash
cd apps/backend && alembic revision --autogenerate -m "add game_id to courses" 2>/dev/null || echo "Migración ya existe o sin cambios"
alembic upgrade head
```

**Criterio**: Si la migración ya fue aplicada previamente (verificar historial de migraciones), no crear una nueva. El campo `game_id` en `course.py:17` ya existe — `alembic upgrade head` debe nocambiar nada.

---

## Implementation — Frontend

### F-1: `types/course.interface.ts` — agregar `gameId`

```typescript
export interface Course {
  id: string;
  name: string;
  description: string | null;
  schoolYear: string;
  periodLabel: string;
  startDate: string;
  endDate: string;
  isActive: boolean;
  gameId: string | null;              // NUEVO
  studentCount: number;
  professorCount: number;
  createdAt: string | null;
  updatedAt: string | null;
}

export interface CourseDetail extends Course {
  students: StudentEnrollment[];
  professors: ProfessorAssignment[];
}

export interface CourseCreateRequest {
  name: string;
  description?: string;
  schoolYear: string;
  periodLabel: string;
  startDate: string;
  endDate: string;
  gameId?: string | null;             // NUEVO
  studentIds: string[];
  professorIds: string[];
}

export interface CourseUpdateRequest {
  name?: string;
  description?: string;
  schoolYear?: string;
  periodLabel?: string;
  startDate?: string;
  endDate?: string;
  gameId?: string | null;             // NUEVO
  studentIds?: string[];
  professorIds?: string[];
  isActive?: boolean;
}
```

---

### F-2: `actions.ts` — agregar `gameId` a schema Zod + cuerpo de petición

**Archivo**: `apps/frontend/src/app/dashboard/courses/actions.ts`

```typescript
// 1. Extender courseSchema para incluir gameId (string | null)
const courseSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  schoolYear: z.string().regex(/^\d{4}-\d{4}$/, "Formato inválido. Use YYYY-YYYY"),
  periodLabel: z.string().min(1),
  startDate: z.string().min(1),
  endDate: z.string().min(1),
  gameId: z.string().uuid().nullable().optional(),  // NUEVO
  studentIds: z.string().transform((val) => {
    try { return JSON.parse(val) as string[] } catch { return [] }
  }),
  professorIds: z.string().transform((val) => {
    try { return JSON.parse(val) as string[] } catch { return [] }
  }),
}).refine(/* ... mismo refine de fechas ... */);

// 2. En createCourse y updateCourse, extraer gameId:
const { gameId, studentIds, professorIds, ...fields } = validated.data;

await coursesApi.create(
  {
    ...fields,
    description: fields.description || undefined,
    gameId: gameId ?? null,       // NUEVO
    studentIds,
    professorIds,
  },
  token
);

// updateCourse: mismo patrón
await coursesApi.update(
  courseId,
  {
    ...fields,
    description: fields.description || undefined,
    gameId: gameId ?? null,       // NUEVO
    studentIds,
    professorIds,
  },
  token
);
```

---

### F-3: `course-form.tsx` — select de juegos + mensaje de profesor autoseleccionado

**Archivo**: `apps/frontend/src/components/courses/course-form.tsx`

**Campos de state nuevos**:
```typescript
const [selectedGameId, setSelectedGameId] = useState<string | null>(
  course?.gameId ?? null
);
```

**Carga de juegos** (puede venir por prop `games: GameOption[]` o por server action):
```typescript
// Opción A — gamingOptions viene por prop desde la página (recomendado)
interface CourseFormProps {
  // ... existentes ...
  games: Array<{ id: string; title: string }>;  // NUEVO
}

// Opción B — fetch client-side (no recomendado, rompe Server Actions pattern)
// Usar Server Action que retorne los juegos
```

**Mensaje de profesor autoseleccionado — modo CREACIÓN**:
```tsx
{/* En modo creación: reemplazar UserMultiSelect de profesores por */}
{!course && (
  <div className="space-y-2">
    <Label className="text-sm text-slate-500">Profesor titular</Label>
    <div className="flex items-center gap-2 rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2.5 bg-slate-50 dark:bg-slate-900/40">
      <GraduationCap className="h-4 w-4 text-indigo-500" />
      <span className="text-sm text-slate-700 dark:text-slate-300">Tú ya estás asignado como profesor titular</span>
    </div>
  </div>
)}

{/* En modo edición: mantener UserMultiSelect para profesores adicionales */}
{course && (
  <UserMultiSelect
    label="Profesores adicionales"
    options={professorOptions}
    selected={selectedProfessorIds}
    onChange={setSelectedProfessorIds}
    placeholder="Agregar profesores adicionales..."
    searchPlaceholder="Buscar profesores..."
    emptyMessage="No se encontraron profesores"
  />
)}
```

**Select de juegos**:
```tsx
{/* Select de juegos */}
<div className="space-y-2">
  <Label htmlFor="gameId">Juego asociado</Label>
  <Select
    value={selectedGameId ?? "none"}
    onValueChange={(v) => setSelectedGameId(v === "none" ? null : v)}
    disabled={isPending}
  >
    <SelectTrigger id="gameId" className="w-full">
      <SelectValue placeholder="Seleccionar juego (opcional)" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="none">Sin juego</SelectItem>
      {games.map((g) => (
        <SelectItem key={g.id} value={g.id}>{g.title}</SelectItem>
      ))}
    </SelectContent>
  </Select>
</div>
```

**Campo oculto `gameId`**:
```tsx
<input
  type="hidden"
  name="gameId"
  value={selectedGameId ?? ""}
/>
```

---

### F-4: `course-table.tsx` — agregar columna "Juego"

**Archivo**: `apps/frontend/src/components/courses/course-table.tsx`

**Ajuste de colSpan**: cambio de `colSpan={6}` a `colSpan={7}` en la fila vacía.

**Nueva fila de headers**:
```tsx
<TableHead className="font-semibold text-slate-700 dark:text-slate-300">
  Juego
</TableHead>
```

Nueva posición: entre "Período" y "Estudiantes" (o al final, según preferencia).

**Nueva celda de datos**:
```tsx
{/* Columna Juego — entre Período y Estudiantes */}
<TableCell>
  <Link href={`/dashboard/courses/${course.id}`} className="block outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 rounded">
    {course.gameId ? (
      <span className="text-sm text-slate-700 dark:text-slate-300 bg-indigo-50 dark:bg-indigo-900/30 px-2 py-1 rounded-md border border-indigo-100 dark:border-indigo-800/50">
        {course.gameTitle || course.gameId.slice(0, 8)}
      </span>
    ) : (
      <span className="text-slate-400 dark:text-slate-500">—</span>
    )}
  </Link>
</TableCell>
```

> **Nota**: Para que `gameTitle` esté disponible en `Course`, el backend debe exponerlo en `CourseResponse`. Alternativamente, el frontend puede hacer un lookup mediante un `Record<string, string>` pasado por props desde la página servidor.

---

## Task Breakdown

### T-1 — Backend: `CourseCreateRequest` + `game_id`
**Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`  
`[ ]` Agregar `game_id: Optional[UUID] = Field(None, alias="gameId")` a `CourseCreateRequest` (línea 17, después de `professor_ids`).  
`[ ]` Verificar que `model_config = {"populate_by_name": True}` esté presente (ya existe en línea 18, sin cambios).

---

### T-2 — Backend: `CourseUpdateRequest` + `game_id`
**Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`  
`[ ]` Agregar `game_id: Optional[UUID] = Field(None, alias="gameId")` a `CourseUpdateRequest` (después de `is_active` en línea 38).  
`[ ]` El `model_config` existente (línea 39) ya cubre el alias.

---

### T-3 — Backend: `CourseResponse` + `CourseDetailResponse` — exponer `game_id`
**Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`  
`[ ]` Agregar `game_id: Optional[UUID] = Field(None, alias="gameId")` a `CourseResponse` (después de `updated_at`, línea 79).  
`[ ]` `CourseDetailResponse` hereda el campo automáticamente; no requiere modificación adicional.  
`[ ]` Verificar que `get_by_id_with_relations()` cargue `selectinload(Course.game)` — agregar si falta y reemplazar por `get_course_with_game()` en `_build_detail_response`.

---

### T-4 — Backend: Endpoint `GET /api/v1/courses/management` — filtrado automático por profesor
**Archivo**: `apps/backend/src/course/api/v1/endpoints/course_management.py`  
`[ ]` Importar `get_current_user` y tipo `User`.  
`[ ]` Agregar `current_user: User = Depends(get_current_user)` a la firma del endpoint.  
`[ ]` Si `current_user.role == "professor"` y no hay `professor_id` explícito: resolver `Professor.id` desde `get_professor_profile_ids([current_user.id])` y asignarlo.  
`[ ]` Pasar `professor_id` resuelto (o `None`) a `course_repo.list_with_counts()`.  
`[ ]` Confirmar que un admin omite el filtro.

---

### T-5 — Backend: `CreateCourseUseCase` — autoselección de profesor
**Archivo**: `apps/backend/src/course/application/usecase/create_course_usecase.py`  
`[ ]` Inyectar `current_user: User` en el constructor del usecase.  
`[ ]` En `execute()`: antes de crear relaciones de `course_professors`, si `current_user.role == "professor"`:
  - Obtener `Professor.id` del usuario actual (`get_professor_profile_ids`)  
  - Si está en el array: no duplicar  
  - Si NO está: agregarlo al array de `valid_professor_ids`
`[ ]` Asegurarse de que el endpoint pase `current_user` al instanciar el usecase.

---

### T-6 — Backend: Migración Alembic
`[ ]` Verificar si ya existe migración aplicada para `game_id`: `alembic history --verbose`.  
`[ ]` Si NO existe: `alembic revision --autogenerate -m "add game_id to courses"`  
`[ ]` Aplicar: `alembic upgrade head`

---

### T-7 — Frontend: Tipos (`course.interface.ts`)
**Archivo**: `apps/frontend/src/types/course.interface.ts`  
`[ ]` Agregar `gameId: string | null` a `Course` (línea 14).  
`[ ]` Agregar `gameId?: string | null` a `CourseCreateRequest` (línea 44, después de `endDate`).  
`[ ]` Agregar `gameId?: string | null` a `CourseUpdateRequest` (línea 55, después de `endDate`).

---

### T-8 — Frontend: Schema Zod + actions (`actions.ts`)
**Archivo**: `apps/frontend/src/app/dashboard/courses/actions.ts`  
`[ ]` Agregar `gameId: z.string().uuid().nullable().optional()` a `courseSchema`.  
`[ ]` En `createCourse`: extraer `gameId` del validated.data, convertir `""` a `null`, enviar en body.  
`[ ]` En `updateCourse`: mismo tratamiento.  
`[ ]` `courseInlineSchema`: agregar `gameId` también (si se usa en actualización inline).

---

### T-9 — Frontend: `CourseForm` — select de juegos + mensaje profesor
**Archivo**: `apps/frontend/src/components/courses/course-form.tsx`  
`[ ]` Agregar `games` a `CourseFormProps` (lista de `{ id: string; title: string }`).  
`[ ]` Cargar juegos mediante prop desde el componente padre (página del dashboard).  
`[ ]` Reemplazar `UserMultiSelect` de "Profesores" en modo **creación** por mensaje fijo `"Tú ya estás asignado como profesor titular"`.  
`[ ]` Mantener `UserMultiSelect` de "Profesores adicionales" en modo **edición**.  
`[ ]` Agregar `<Select>` de juegos con valor `selectedGameId`.  
`[ ]` Agregar `<input type="hidden" name="gameId" value={...} />` antes del submit.  
`[ ]` Sincronizar `selectedGameId` en `useEffect` cuando cambie la prop `course`.

---

### T-10 — Frontend: `course-table.tsx` — columna "Juego"
**Archivo**: `apps/frontend/src/components/courses/course-table.tsx`  
`[ ]` Agregar `<TableHead>` de "Juego" en la fila de headers (después de "Período").  
`[ ]` Ajustar `colSpan` de la fila vacía de `{6}` a `{7}`.  
`[ ]` Renderizar celda con título del juego (`course.gameTitle` o lookup por `gameId`) o "—".

---

### T-11 — Frontend: Página de cursos — cargar y pasar juegos al `CourseTable` y `CourseForm`
**Archivo**: `apps/frontend/src/app/dashboard/courses/page.tsx` (o Server Component que envuelve CourseTable)  
`[ ]` Llamar a `GET /api/v1/games` desde el componente servidor.  
`[ ]` Pasar `games` como prop a `<CourseTable>` y `<CourseForm>`.  
`[ ]` De ser necesario, enriquir cada `Course` con `gameTitle` mediante la lista de juegos antes de pasarlo a `CourseTable`.

---

### T-12 — Frontend: `api/client.ts` — `coursesApi` incluye `gameId`
**Archivo**: `apps/frontend/src/api/client.ts`  
`[ ]` Verificar que la firma de `create` y `update` en `coursesApi` incluya `gameId` en el tipo del body.  
`[ ]` Si hay un tipo estricto en el cliente, actualizarlo.  
`[ ]` Confirmar que `list` de cursos no envía `professor_id` (backend filtra automáticamente).

---

## Regresiones y Criterios de Aceptación

### Regresión 1 — Filtrado de cursos (listado general)
- **Antes**: sin `professor_id` en query, un profesor veía todos los cursos.  
- **Ahora**: profesor ve solo los suyos automáticamente.  
- **Impacto**: Cambio de comportamiento en producción sin feature-flag.  
- **Mitigación**: Comunicar a stakeholders; verificar con QA que un admin vea todos los cursos sin problema.

### Regresión 2 — Campo `professor_ids` en creación
- **Antes**: el frontend enviaba `professorIds: []` y el curso se creaba sin profesores.  
- **Ahora**: el backend autocompleta con el profesor logueado → el array vacío es válido.  
- **Mitigación**: NC. El comportamiento mejorado no rompe nada.

### Regresión 3 — Campo `game_id`
- **Antes**: no existía en request/response.  
- **Ahora**: opcional (`nullable`). Cursos existentes tienen `game_id = NULL` → se muestran como "—" en tabla.  
- **Mitigación**: Backward compatible al 100%. Sin impacto en datos existentes.

---

### Criterios de Aceptación (AC)

| ID | Criterio | Verificable mediante |
|----|----------|----------------------|
| AC-1 | Profesor autenticado en `GET /courses/management` sin query params → recibe solo sus cursos | E2E / integration test |
| AC-2 | Admin en `GET /courses/management` sin query params → recibe todos los cursos | E2E / integration test |
| AC-3 | `CreateCourseUseCase` agrega al profesor logueado automáticamente al crear | Unit test en `create_course_usecase.py` |
| AC-4 | Profesor se agrega a sí mismo explícitamente → no se duplica | Unit test |
| AC-5 | `CourseCreateRequest` acepta `gameId` y lo guarda en BD | Integration test |
| AC-6 | `CourseUpdateRequest` acepta `gameId` y actualiza el registro | Integration test |
| AC-7 | `CourseResponse` incluye `gameId` en la respuesta | Integration test |
| AC-8 | Select de juegos aparece en el formulario al abrirlo | E2E Playwright test |
| AC-9 | Al seleccionar un juego y enviar, el curso se crea con `game_id` poblado | E2E Playwright test |
| AC-10 | La tabla de cursos muestra la columna "Juego" con título o "—" | E2E Playwright test |
| AC-11 | Migración Alembic aplicada exitosamente en ambiente de prueba | `alembic upgrade head` sin errores |
| AC-12 | Admin → `GET /courses/management?professor_id=<x>` → retorna cursos del profesor X | Integration test |

---

## Archivos Afectados — Resumen

| Ruta | Tipo de cambio |
|------|----------------|
| `apps/backend/src/course/api/v1/schemas/course_management.py` | Modificar schemas (T-1, T-2, T-3) |
| `apps/backend/src/course/api/v1/endpoints/course_management.py` | Modificar endpoint list + inject user (T-4) |
| `apps/backend/src/course/application/usecase/create_course_usecase.py` | Inyectar current_user + autoselección (T-5) |
| `apps/backend/alembic/versions/` | Nueva migración (si aplica) (T-6) |
| `apps/frontend/src/types/course.interface.ts` | Agregar `gameId` en interfaces (T-7) |
| `apps/frontend/src/app/dashboard/courses/actions.ts` | Schema Zod + gameId en body (T-8) |
| `apps/frontend/src/components/courses/course-form.tsx` | Select juegos + mensaje profesor (T-9) |
| `apps/frontend/src/components/courses/course-table.tsx` | Columna "Juego" (T-10) |
| `apps/frontend/src/app/dashboard/courses/page.tsx` | Pasar `games` como prop (T-11) |
| `apps/frontend/src/api/client.ts` | Tipos de `coursesApi` incluyen `gameId` (T-12) |
