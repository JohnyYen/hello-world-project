# feat(courses): profesor ve solo sus cursos + autoselección en creación + select de juegos

## Resumen Ejecutivo

Se implementan 3 reglas de negocio sobre el dominio de Cursos:

1. **Filtrado automático por profesor**: un profesor autenticado solo ve sus propios cursos en el listado; un admin ve todos.
2. **Autoselección de profesor**: al crear un curso, el profesor logueado se asigna automáticamente como profesor titular.
3. **Select de juegos en el formulario**: se agrega un campo select para asociar un juego al curso, usando el endpoint existente `GET /api/v1/games`.

---

## Estado Actual del Código

### Backend
- El modelo `Course` **ya posee** la columna `game_id` con FK a `games.id` (ver `course.py:17`), pero los schemas `CourseCreateRequest` y `CourseUpdateRequest` **no la exponen**.
- El endpoint `GET /api/v1/courses/management` recibe `professor_id` como query param opcional. Si no se envía, devuelve todos los cursos sin filtrar.
- El `CreateCourseUseCase` no autoselecciona al profesor logueado; espera que el frontend envíe `professor_ids`.
- El `CourseRepository.list_with_counts` ya soporta filtrar por `professor_id` (línea 440-448 de `course_repository.py`).

### Frontend
- El `CourseForm` envía `professorIds` como campo oculto; el usuario debe seleccionar profesores manualmente.
- No existe campo de juego en el form, en los tipos `CourseCreateRequest`/`CourseDetail`, ni en la tabla.

---

## CAMBIOS BACKEND

1. **`course_management.py` — Inyectar `current_user` y aplicar filtro automático**
   Agregar dependencia `get_current_user` (o el mecanismo de auth existente) al endpoint `GET /api/v1/courses/management`. Si el `current_user.role === "professor"`, resolver su `Professor.id` y pasarlo como `professor_id` al servicio automáticamente. Los admins no reciben filtro. El query param `professor_id` se mantiene como override explícito para admins.

2. **`course_management.py` — Exponer `game_id` en `CourseCreateRequest` y `CourseUpdateRequest`**
   Agregar `game_id: Optional[UUID] = Field(None, alias="gameId")` a ambos schemas en `schemas/course_management.py`. El `model_config` con `populate_by_name=True` ya existe y maneja los alias correctamente.

3. **`course.py` (modelo) — Eager-load del `game`**
   El modelo ya tiene `game = relationship("Game", back_populates="courses")`. Agregar `selectinload(Course.game)` en `get_by_id_with_relations` del repositorio para que el `CourseDetailResponse` incluya los datos del juego. También modificar `CourseResponse` para exponer `game_id`.

4. **`create_course_usecase.py` — Autoselección del profesor logueado**
   Agregar `current_user` como parámetro (inyectado por el endpoint). Si `current_user.role === "professor"`, llamar a `course_repo.get_professor_profile_ids([current_user.id])` para obtener su `Professor.id` e inyectarlo en `request.professor_ids` antes de crear las relaciones. No duplicar si el usuario ya lo incluyó manualmente.

---

## CAMBIOS FRONTEND

1. **`types/course.interface.ts` — Agregar `gameId` a interfaces y schemas**
   - `Course`: agregar `gameId: string | null`
   - `CourseDetail`: hereda el campo (redundante pero explícito)
   - `CourseCreateRequest`: agregar `gameId?: string | null`
   - `CourseUpdateRequest`: agregar `gameId?: string | null`

2. **`api/client.ts` — `coursesApi.list` ya no envía `professor_id`**
   Quitar cualquier envío explícito de `professor_id` en `coursesApi.list` (actualmente no lo envía en la URL, revisar `listByRole` para confirmar). El backend filtra automáticamente por el usuario autenticado.

3. **`components/courses/course-form.tsx` — Select de juegos + mensaje de profesor autoseleccionado**
   - Reemplazar el `UserMultiSelect` de "Profesores" en modo creación por un mensaje informativo fijo: *"Tú ya estás asignado como profesor titular"*.
   - Mantener un `UserMultiSelect` opcional para "Profesores adicionales" (sin el botón de búsqueda autobuscable del titular).
   - Agregar `<Select>` de juegos: cargar opciones desde `GET /api/v1/games` y enviar `gameId` en el campo oculto del form.

4. **`app/dashboard/courses/actions.ts` — Pasar `gameId` y eliminar validación de `professorIds` en creación**
   - En `createCourse`: agregar `gameId: formData.get("gameId")` al schema Zod y al body de la API.
   - En modo creación, **no validar** `professorIds` como obligatorio; siempre se autoselecciona en el backend. El campo `professorIds` puede seguir enviándose para profesores adicionales.

5. **`components/courses/course-table.tsx` — Mostrar columna "Juego"**
   Agregar columna que muestre `course.gameId ? course.game.title : "Sin juego"` (o solo el título o "—" si es null).

---

## MIGRACIÓN

- El modelo `Course` **ya incluye** `game_id: UUID` con FK `games.id` en `course.py:17`. Verificar si existe una migración de Alembic pendiente. Si no existe, crearla:

```bash
alembic revision --autogenerate -m "add game_id to courses"
```

- Si la migración ya existe, solo verificar que esté aplicada con `alembic upgrade head`.
- La columna es `nullable=True`, por lo que cursos existentes no se rompen.

---

## REGRESIONES

1. **Filtrado de cursos (listado general)**: Antes, un profesor podía ver todos los cursos si navegaba a la URL sin query param. Ahora verá solo los suyos. Se modifica comportamiento en producción sin flag feature-toggle.
2. **Campo `professor_ids` en creación**: Antes el formulario enviaba el array vacío o requería búsqueda. Ahora el backend lo autocompleta, por lo que el frontend puede enviar array vacío sin error.
3. **Campo `game_id`**: Antes no existía. Ahora es opcional (nullable). Los cursos existentes tendrán `game_id = null`.

---

## CRITERIOS DE ACEPTACIÓN

- [ ] **RN-1**: Un profesor autenticado que accede a `GET /api/v1/courses/management` sin query params recibe solo sus cursos. Un admin recibe todos los cursos.
- [ ] **RN-2**: El listado `GET /api/v1/courses/management` filtra por `professor_id` automáticamente basado en el JWT, sin necesidad de query param.
- [ ] **RN-3**: Al crear un curso, el `CreateCourseUseCase` agrega al profesor logueado a `professor_ids` automáticamente. El curso se crea con el profesor ya asignado.
- [ ] **RN-4**: El formulario de creación muestra un `<Select>` con los juegos de `GET /api/v1/games`. Al enviar el form, el curso se crea con `game_id` poblado. La tabla de cursos muestra la columna "Juego" con el título correspondiente.
