# Tasks — courses-business-rules

## Backend Tasks

### T-1: `CourseCreateRequest` — agregar `game_id`
- **Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`
- **Estado**: ✅ Completado
- **Descripción**: Agregar `game_id: Optional[UUID] = Field(None, alias="gameId")` a `CourseCreateRequest` (después de `professor_ids`).

### T-2: `CourseUpdateRequest` — agregar `game_id`
- **Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`
- **Estado**: ✅ Completado
- **Descripción**: Agregar `game_id: Optional[UUID] = Field(None, alias="gameId")` a `CourseUpdateRequest` (después de `is_active`).

### T-3: `CourseResponse` — exponer `game_id`
- **Archivo**: `apps/backend/src/course/api/v1/schemas/course_management.py`
- **Estado**: ✅ Completado
- **Descripción**: `game_id` ya existe en `CourseResponse`. `get_by_id_with_relations` ya carga `Course.game`.

### T-4: Endpoint `GET /courses/management` — filtrado automático por profesor
- **Archivo**: `apps/backend/src/course/api/v1/endpoints/course_management.py`
- **Estado**: ✅ Completado
- **Descripción**: Inyectar `current_user = Depends(get_current_user)`. Si `role == "professor"`: resolver `Professor.id` y aplicar filtro.

### T-5: `CreateCourseUseCase` — autoselección de profesor
- **Archivo**: `apps/backend/src/course/application/usecase/create_course_usecase.py`
- **Estado**: ✅ Completado
- **Descripción**: Inyectar `current_user` en constructor. Autoseleccionar profesor si rol=professor (sin duplicar).

### T-6: Migración Alembic
- **Archivo**: `apps/backend/alembic/versions/`
- **Estado**: ✅ Completado
- **Descripción**: La columna `game_id` ya existe en el modelo y migraciones. No se requiere acción.

## Frontend Tasks

### T-7: Tipos TypeScript — agregar `gameId`
- **Archivo**: `apps/frontend/src/types/course.interface.ts`
- **Estado**: ⏳ Pendiente
- **Descripción**: Agregar `gameId: string | null` a `Course`, `CourseCreateRequest`, `CourseUpdateRequest`.

### T-8: Schema Zod + actions — agregar `gameId`
- **Archivo**: `apps/frontend/src/app/dashboard/courses/actions.ts`
- **Estado**: ⏳ Pendiente
- **Descripción**: Agregar `gameId` a `courseSchema` y a los body de `createCourse`/`updateCourse`.

### T-9: `CourseForm` — select de juegos + mensaje profesor
- **Archivo**: `apps/frontend/src/components/courses/course-form.tsx`
- **Estado**: ⏳ Pendiente
- **Descripción**: Agregar prop `games`, reemplazar `UserMultiSelect` por mensaje en modo creación, agregar `<Select>` de juegos.

### T-10: `CourseTable` — columna "Juego"
- **Archivo**: `apps/frontend/src/components/courses/course-table.tsx`
- **Estado**: ⏳ Pendiente
- **Descripción**: Agregar columna "Juego" entre Período y Estudiantes. Ajustar `colSpan` de 6 a 7.

### T-11: Página de cursos — cargar juegos
- **Archivo**: `apps/frontend/src/app/dashboard/courses/page.tsx`
- **Estado**: ⏳ Pendiente
- **Descripción**: Llamar a `GET /api/v1/games` y pasar `games` como prop a `CourseTable` y `CourseForm`.

### T-12: `api/client.ts` — tipos de `coursesApi`
- **Archivo**: `apps/frontend/src/api/client.ts`
- **Estado**: ⏳ Pendiente
- **Descripción**: Verificar que `create` y `update` incluyan `gameId` en el tipo del body.

---

## Estado General

- **Total tareas**: 12
- **Completadas**: 0
- **Pendientes**: 12
- **En progreso**: 0