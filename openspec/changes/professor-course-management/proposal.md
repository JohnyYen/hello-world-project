# Proposal: Gestión de Cursos para Profesores

## Intent

Los profesores necesitan gestionar los cursos académicos desde la plataforma: crear cursos, asignar estudiantes y profesores, y administrar inscripciones. Actualmente los modelos `Course`, `CourseEnrollment` y `CourseProfessor` existen en la base de datos pero NO hay endpoints CRUD ni interfaz web para administrarlos. El único endpoint existente es `GET /courses` (dentro del router de reports) que lista cursos con conteo de estudiantes. Esta propuesta cierra esa brecha entregando gestión completa de cursos.

## Scope

### In Scope

**Backend — API REST (`/api/v1/courses`)**

1. `GET /api/v1/courses/` — Listar cursos con paginación, conteo de estudiantes y profesores asignados
2. `POST /api/v1/courses/` — Crear curso con asignación de estudiantes y profesores en una sola operación
3. `GET /api/v1/courses/{id}` — Obtener detalle de curso con estudiantes y profesores
4. `PUT /api/v1/courses/{id}` — Actualizar curso (campos + estudiantes/profesores)
5. `DELETE /api/v1/courses/{id}` — Eliminar curso (soft delete, desasigna estudiantes/profesores)
6. `GET /api/v1/courses/{id}/students` — Listar estudiantes inscritos en un curso
7. `POST /api/v1/courses/{id}/students` — Inscribir estudiante(s) a un curso
8. `DELETE /api/v1/courses/{id}/students/{student_id}` — Desinscribir estudiante de un curso
9. `GET /api/v1/users/?role=student` — Listar estudiantes disponibles (filtrar usuarios por rol student)
10. `GET /api/v1/users/?role=professor` — Listar profesores disponibles

**Frontend — Dashboard Web**

11. Nuevo item en sidebar: "Cursos" con icono `BookOpen`
12. Ruta `/dashboard/cursos` — Tabla de cursos con acciones: Crear, Editar, Ver detalle, Eliminar
13. Ruta `/dashboard/cursos/{id}` — Detalle de curso con tabla de estudiantes asignados y botones para asignar/desasignar
14. Modal/página de creación/edición de curso con: campos del curso + multi-select de estudiantes + multi-select de profesores

**Arquitectura**

15. Migración de Alembic (si es necesario para nuevos campos o constraints)
16. Servicios (CourseService) y casos de uso (CreateCourseUseCase, UpdateCourseUseCase, ManageEnrollmentUseCase) siguiendo Clean Architecture
17. Schemas Pydantic v2 para request/response
18. Router independiente para course management (separado del router de reports existente)

### Out of Scope

- Importación masiva de estudiantes vía CSV/Excel
- Sincronización con LMS externo para cursos
- Reportes avanzados por curso (ya existen en el router de reports)
- Calendario académico o visualización tipo timeline
- Permisos granulares por curso (quién puede ver/editar cada curso)
- Notificaciones a estudiantes al ser asignados/desasignados
- Historial de cambios en el curso

## Approach

**Backend-first, luego frontend**, siguiendo Clean Architecture:

### Fase 1 — Backend Infrastructure

1. **CourseRepository** — Extender el repositorio existente con métodos para:
   - `create_with_assignments(data, student_ids, professor_ids)` — transaccional
   - `get_by_id_with_relations(id)` — eager loading de enrollments y course_professors
   - Manejo de CourseEnrollment y CourseProfessor como joins

2. **CourseService** — CRUD básico usando BaseService + validaciones de dominio:
   - Validar que school_year/period_label no se dupliquen
   - Soft delete en cascada (marcar enrollments como eliminados)
   - Validar que student_id y professor_id existan antes de asignar

3. **UseCases** — Lógica de negocio:
   - `CreateCourseUseCase` — orquesta creación del curso + asignaciones
   - `UpdateCourseUseCase` — actualiza curso + sincroniza asignaciones
   - `ManageEnrollmentUseCase` — inscribir/desinscribir estudiantes

4. **Endpoints (/api/v1/courses/)** — Router separado del de reports:
   - Endpoints CRUD delegando a UseCases
   - Endpoints de enrollment delegando a ManageEnrollmentUseCase

5. **User filtering** — Extender endpoint existente de usuarios (o crear uno nuevo en auth/user domain) para soportar filtro por `?role=student` y `?role=professor`

### Fase 2 — Frontend

6. **Sidebar** — Agregar item "Cursos" en `app-sidebar.tsx`
7. **Página de listado** (`/dashboard/cursos/page.tsx`) — Server Component que carga datos, renderiza tabla client-side
8. **Página de detalle** (`/dashboard/cursos/[id]/page.tsx`) — Server Component con tabla de estudiantes asignados
9. **Formulario crear/editar** — Client Component con multi-select de estudiantes y profesores

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `apps/backend/src/course/api/v1/router.py` | Modified | Agregar nuevo router de course management |
| `apps/backend/src/course/api/v1/endpoints/` | New | Endpoints CRUD y enrollment |
| `apps/backend/src/course/api/v1/schemas/` | New | Schemas Pydantic para request/response de cursos |
| `apps/backend/src/course/application/service/` | New | CourseService con lógica CRUD |
| `apps/backend/src/course/application/usecase/` | New | UseCases: CreateCourse, UpdateCourse, ManageEnrollment |
| `apps/backend/src/course/infrastructure/course_repository.py` | Modified | Agregar métodos transaccionales y con relaciones |
| `apps/backend/src/course/domain/` | Unchanged | Modelos existentes son suficientes |
| `apps/frontend/src/components/dashboard/app-sidebar.tsx` | Modified | Agregar item "Cursos" |
| `apps/frontend/src/app/dashboard/cursos/` | New | Páginas de listado y detalle |
| `apps/frontend/src/components/cursos/` | New | Componentes: tabla, formulario, multi-select |
| `packages/api-contract/openapi.json` | Modified | Reflejar nuevos endpoints |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Conflict with existing `GET /courses` in reports router | High | Crear router separado con prefix `/api/v1/courses` que incluya ambos sub-routers (reports + management) |
| Orphaned enrollments on course soft delete | Medium | Soft delete de CourseEnrollment y CourseProfessor en cascada dentro del UseCase |
| Repository usa Integer IDs pero modelos existentes usan UUID | Low | Los modelos Course/Enrollment heredan de Base que usa UUID; verificar consistencia en CourseRepository que tiene type hints con `int` |
| DuplicaciÃ³n de cÃ³digo entre Service y UseCase | Low | Usar Service para CRUD simple, UseCase solo cuando hay orchestracion multi-entidad |
| Multi-select UI compleja para estudiantes/profesores | Medium | Usar shadcn/ui Command + Popover para multi-select, con debounced search |

## Rollback Plan

1. **Backend**: Remover el nuevo router de `course/api/v1/router.py` y eliminar los archivos de endpoints/usecases/services creados
2. **Frontend**: Remover las rutas `cursos/` del dashboard y restaurar `app-sidebar.tsx`
3. **Base de datos**: Si se agregÃ³ migraciÃ³n, ejecutar `alembic downgrade -1` para revertirla
4. **API Contract**: Revertir cambios en `openapi.json`

## Dependencies

- Modelos existentes: `Course`, `CourseEnrollment`, `CourseProfessor` (ya migrados)
- `BaseRepository` — CRUD genÃ©rico ya implementado
- `BaseService` — Capa de servicio genÃ©rica ya implementada
- PatrÃ³n de endpoints existente en `course/api/v1/endpoints/course_reports.py`
- UI components: shadcn/ui Table, Dialog, Command, Popover (ya instalados en el proyecto)
- API Client: workspace/api-client-ts para consumo desde frontend

## Success Criteria

- [ ] Todos los endpoints CRUD de cursos responden correctamente verificados con pytest
- [ ] CreaciÃ³n de curso con asignaciÃ³n de estudiantes y profesores funciona en un solo POST
- [ ] InscripciÃ³n y desinscripciÃ³n de estudiantes en un curso funciona correctamente
- [ ] Filtro `?role=student` y `?role=professor` en endpoint de usuarios funciona
- [ ] Sidebar muestra "Cursos" y navega a `/dashboard/cursos`
- [ ] Listado de cursos en frontend muestra datos correctos con acciones Crear/Editar/Eliminar
- [ ] Formulario de crear/editar curso permite seleccionar estudiantes y profesores
- [ ] Detalle de curso muestra estudiantes asignados con opciÃ³n de desasignar
- [ ] Soft delete de curso desasigna todos los estudiantes/profesores relacionados
- [ ] UI text en espaÃ±ol, `cn()` utility usada, Server Actions para mutaciones
