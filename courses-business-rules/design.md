# Design: courses-business-rules

## Resumen Ejecutivo

Se implementan tres reglas de negocio sobre el dominio de Cursos:

**Filtrado automático por profesor**: actualmente el endpoint `GET /courses/management` devuelve todos los cursos si no se envía el query param `professor_id`. Un profesor puede ver datos de otros docentes. Con el cambio, el backend detecta el rol del usuario autenticado y, si es profesor, resuelve su `Professor.id` y aplica el filtro automáticamente antes de ejecutar la consulta. Los administradores continúan viendo todos los cursos sin interferencia.

**Autoselección de profesor en creación**: el `CreateCourseUseCase` recibe `current_user` y, si el rol es `professor`, agrega automáticamente su `Professor.id` al array de `professor_ids` antes de persistir las relaciones. No se duplica si el profesor ya lo incluyó explícitamente en el request. Con esto el frontend puede enviar `professorIds: []` sin generar un curso sin profesores. Un admin no recibe este comportamiento.

**Select de juegos en el formulario**: el modelo `Course` ya tiene la columna `game_id` con FK a `games.id`, pero los schemas Pydantic no la exponían y el frontend no tenía forma de asociar un juego. Se agrega `game_id: Optional[UUID]` a `CourseCreateRequest`, `CourseUpdateRequest` y `CourseResponse`, y un `<Select>` en el `CourseForm` que carga las opciones desde `GET /api/v1/games`. La asociación es opcional por negocio — existen cursos válidos sin juego — y se envía como `null` cuando se deja vacío.

El impacto de estos cambios afecta el flujo completo del listado de cursos, el formulario de creación y la tabla de listado, en ambos extremos de la pila (backend y frontend). No requiere migración de datos: la columna `game_id` ya existe tanto en el modelo SQLAlchemy como en PostgreSQL.

---

## Decisiones de Arquitectura

### D-1: `game_id` se expone en schemas pero no se fuerza en BD

**Choice**: Exponer `game_id` en schemas Pydantic como `Optional[UUID]`, columna PostgreSQL nullable.
**Alternativas**: Hacerla NOT NULL y migrar cursos existentes → `game_id = NULL`.
**Rationale**: La relación juego-curso es opcional por negocio. Cursos sin juego son válidos. Sin necesidad de migración de datos. Backward-compatible.

### D-2: Filtrado por profesor en el endpoint, no en el servicio

**Choice**: El filtrado se inyecta en el endpoint (`course_management.py`), no en `CourseService.list_courses_with_counts()`.
**Alternatives**: Mover la lógica al servicio.
**Rationale**: El servicio es genérico; el endpoint conoce la capa de autenticación. El servicio se puede reutilizar por otros endpoints (reportes) sin filtro. Más limpio.

### D-3: Autoselección de profesor en UseCase, no en endpoint

**Choice**: `CreateCourseUseCase` recibe `current_user` y autoselecciona internamente.
**Alternativas**: El endpoint armaría el `professor_ids` antes de llamar al usecase.
**Rationale**: La lógica de negocio "el profesor logueado siempre está asignado" pertenece al dominio de cursos, no a la capa de endpoint. El usecase es el único lugar donde se construye el objeto Course + relaciones.

### D-4: `game_id` se carga con `selectinload` en `get_course_with_game`, no en `get_by_id_with_relations`

**Choice**: Usar `CourseRepository.get_course_with_game()` en `_build_detail_response`, manteniendo `get_by_id_with_relations` sin el `game` load.
**Alternatives**: Agregar `selectinload(Course.game)` a `get_by_id_with_relations`.
**Rationale**: `get_by_id_with_relations` se usa en múltiples lugares (listado, detalle). Agregar `game` ahí infla la query en contextos donde no se necesita (listado). `get_course_with_game` es específico para el detalle donde sí se necesita.

### D-5: `UserMultiSelect` se reemplaza por mensaje fijo SOLO en modo creación

**Choice**: En modo edición se mantiene el `UserMultiSelect` (profesores adicionales), en modo creación se reemplaza por el mensaje fijo.
**Alternativas**: Eliminar `UserMultiSelect` completamente, solo dejar mensaje.
**Rationale**: Al editar, el profesor puede agregar/remover profesores adicionales, incluso removerse a sí mismo (out of scope para este cambio). La regla de autoselección aplica solo a la CREACIÓN.

### D-6: `gameTitle` se resuelve en el layer servidor del frontend

**Choice**: La página servidor (`page.tsx`) carga `GET /api/v1/games` y construye un `Record<string, string>` (map `id → title`) que se pasa como prop a `CourseTable` y `CourseForm`. El backend expone solo `gameId` en `CourseResponse`, no el título.
**Alternativas**: Exponer `game_title` en `CourseResponse` desde el backend (requiere JOIN al crear la respuesta de listado y detalle).
**Rationale**: Los juegos son datos de catálogo, cambian poco, y cargarlos en el servidor Next.js es más barato que agregar JOINs a cada consulta de cursos en el backend. Reduce el acoplamiento entre dominios.

---

## Flujo de Datos

### Filtrado de profesor (RN-1)

```ascii
Request GET /courses/management
       │
       ▼
Endpoint course_management.py
  └─ get_current_user() → User
       │
       ├─ role == "admin"  → sin filtro
       ├─ role == "professor"
       │    └─ course_repo.get_professor_profile_ids([user.id]) → Professor.id
       │         └─ list_with_counts(professor_id=Professor.id) → courses[]
       └─ PaginatedCourseListResponse
```

### Autoselección (RN-2)

```ascii
POST /courses/management { professorIds: [], gameId: "uuid-x" }
       │
       ▼
CreateCourseUseCase.execute(current_user=profesor)
  ├─ current_user.role == "professor"
  │    └─ get_professor_profile_ids([current_user.id])
  │         └─ professor_ids = [professorId] + request.professor_ids
  │              └─ bulk_create_professors(course.id, professor_ids)
  └─ CourseDetailResponse con professors[]
```

### Select de juegos (RN-3)

```ascii
CourseForm (creación)
  │
  ├─ page.tsx → GET /api/v1/games → games[]
  │    └─ <Select> opciones: [{id, title}, ...] + "Sin juego"
  │         └─ CourseForm recibe games por prop
  │
  ├─ submit form → FormData con gameId
  │    └─ createCourse action → courseSchema.parse()
  │         └─ POST /courses/management { gameId, ... }
  │              └─ CreateCourseUseCase → Course(game_id=gameId)
  │
  ▼
CourseDetailResponse → { ..., gameId: "uuid-x", ... }
  └─ CourseTable → columna "Juego" (lookup por gameTitle map)
```

---

## Cambios de Archivos

### Backend

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `apps/backend/src/course/api/v1/schemas/course_management.py` | Modificar | Agregar `game_id: Optional[UUID]` a `CourseCreateRequest` (después de `professor_ids`), `CourseUpdateRequest` (después de `is_active`), `CourseResponse` (después de `updated_at`). `model_config = {"populate_by_name": True}` ya existe. |
| `apps/backend/src/course/api/v1/endpoints/course_management.py` | Modificar | Inyectar `current_user = Depends(get_current_user)`. Si `role == "professor"`: resolver `Professor.id` vía `get_professor_profile_ids` y pasarlo como `professor_id` al servicio. |
| `apps/backend/src/course/application/usecase/create_course_usecase.py` | Modificar | Inyectar `current_user` en constructor. Autoseleccionar profesor si rol=professor (no duplicar). Usar `get_course_with_game` en `_build_detail_response`. |
| `apps/backend/alembic/versions/` | Verificar | La columna `game_id` ya existe en el modelo y PostgreSQL. Verificar con `alembic history --verbose` y `alembic upgrade head`. |

### Frontend

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `apps/frontend/src/types/course.interface.ts` | Modificar | Agregar `gameId: string \| null` en `Course`, `CourseCreateRequest`, `CourseUpdateRequest`. |
| `apps/frontend/src/app/dashboard/courses/actions.ts` | Modificar | Agregar `gameId` al Zod schema y al body de `createCourse`/`updateCourse`. |
| `apps/frontend/src/components/courses/course-form.tsx` | Modificar | Agregar `Select` de juegos recibido por prop. Reemplazar `UserMultiSelect` por mensaje fijo en modo creación. Mantener `UserMultiSelect` para "Profesores adicionales" en modo edición. |
| `apps/frontend/src/components/courses/course-table.tsx` | Modificar | Agregar columna "Juego" entre Período y Estudiantes. Ajustar `colSpan` de fila vacía de 6 a 7. Renderizar título o "—" usando lookup por `gameId`. |
| `apps/frontend/src/app/dashboard/courses/page.tsx` | Modificar | Llamar a `GET /api/v1/games` desde el componente servidor. Construir `Record<string, string>` de `id → title` y pasarlo como prop a `CourseTable` y `CourseForm`. |
| `apps/frontend/src/api/client.ts` | Verificar | Confirmar que `create` y `update` de `coursesApi` incluyan `gameId` en el tipo del body. |

---

## Contratos / Interfaces

### Backend — Cambios en schemas Pydantic

```python
# CourseCreateRequest
game_id: Optional[UUID] = Field(None, alias="gameId")

# CourseUpdateRequest
game_id: Optional[UUID] = Field(None, alias="gameId")

# CourseResponse
game_id: Optional[UUID] = Field(None, alias="gameId")
# CourseDetailResponse hereda automáticamente
```

### Frontend — Cambios en tipos TypeScript

```typescript
// Course
gameId: string | null;

// CourseCreateRequest / CourseUpdateRequest
gameId?: string | null;
```

### Contrato de página servidor → CourseTable / CourseForm

```typescript
// gamesMap: Record<string, string> — id → título
// Se construye en page.tsx desde la respuesta de GET /api/v1/games
interface CoursesPageProps {
  gamesMap: Record<string, string>;
  // ... resto de props existentes
}
```

---

## Estrategia de Testing

| Layer | Qué probar | Enfoque |
|-------|-----------|---------|
| Unit | `CreateCourseUseCase` autoselecciona profesor cuando rol=professor | Mock de `get_professor_profile_ids`, verificar que el profesor esté en `bulk_create_professors` |
| Unit | `CreateCourseUseCase` NO agrega profesor si rol=admin | Mock de rol=admin, verificar que `professor_ids` sea solo el del request |
| Unit | `CreateCourseUseCase` no duplica si el profesor ya está en `professor_ids` | Mock con profesor ya incluido, verificar que no haya duplicado |
| Integration | `GET /courses/management` sin `professor_id` → profesor recibe solo sus cursos | Test de integración con DB en memoria + JWT simulado |
| Integration | `GET /courses/management` sin `professor_id` → admin recibe todos | Test de integración con DB en memoria + JWT admin |
| Integration | `POST /courses/management` con `gameId` → `CourseDetailResponse` con `game_id` poblado | Test de integración con BD |
| E2E (Playwright) | Página `/dashboard/courses`: profesor solo ve sus cursos | Verificar que cursos de otros profesores no aparezcan en el DOM |
| E2E (Playwright) | Crear curso: select de juegos visible y funcional | Interactuar con el select, verificar opciones cargadas |
| E2E (Playwright) | Crear curso: mensaje "Tú ya estás asignado como profesor titular" aparece | Verificar texto en el DOM en modo creación |
| E2E (Playwright) | Tabla muestra columna "Juego" con título o "—" | Verificar encabezado y contenido de celdas |

---

## Migración

**No se requiere migración de datos.**

La columna `game_id` en la tabla `courses` ya existe en el modelo (`course.py:17`) y en PostgreSQL. El `alembic upgrade head` no debe introducir cambios.

Verificar con:

```bash
cd apps/backend && alembic history --verbose
alembic upgrade head
```

Si por algún motivo no aparece una migración para `game_id`, crearla, pero no se espera que sea necesario:

```bash
cd apps/backend && alembic revision --autogenerate -m "add game_id to courses"
alembic upgrade head
```

---

## Preguntas Abiertas

- [ ] **`gameTitle` en Course**: ¿Necesita `CourseResponse` exponer el título del juego además de `gameId`? Para la columna de la tabla es ideal tenerlo directo. **Decisión tomada**: el frontend hace lookup — `page.tsx` carga `GET /api/v1/games` y construye `Record<string, string>` antes de renderizar. No hay cambios adicionales en el backend.
- [ ] **Tests existentes de `create_course_usecase.py`**: ¿Hay tests existentes en `apps/backend/tests/course/` que necesiten actualizarse por el nuevo parámetro `current_user` en el constructor? Verificar antes de implementar.
