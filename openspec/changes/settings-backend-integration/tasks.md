# Tasks: Settings Backend Integration

## Phase 1: Backend Model Expansion + Migration

- [ ] 1.1 Add 8 new nullable columns to `TeacherSettings` model in `apps/backend/src/users/domain/teacher_settings.py`: `auto_logout` (bool), `session_duration_minutes` (int), `remember_login` (bool), `color_theme` (str), `animations_enabled` (bool), `email_notifications` (bool), `date_format` (str), `timezone` (str)
- [ ] 1.2 Generate Alembic migration via `alembic revision --autogenerate -m "add teacher_settings new fields"` in `apps/backend/`
- [ ] 1.3 Verify migration file in `apps/backend/migrations/versions/` has correct nullable columns with no server defaults
- [ ] 1.4 Update `create_for_user` method in `apps/backend/src/users/application/service/teacher_settings_service.py` to include application-level defaults for all 8 new fields

## Phase 2: Backend Schemas + Endpoints

- [ ] 2.1 Add 8 new optional fields to `TeacherSettingsUpdate` Pydantic schema in `apps/backend/src/users/api/v1/schemas/teacher.py`
- [ ] 2.2 Add 8 new fields to `TeacherSettingsResponse` Pydantic schema in `apps/backend/src/users/api/v1/schemas/teacher.py`
- [ ] 2.3 Change `notification_frequency` validation from `"instant"` to `"realtime"` in the Pydantic schema
- [ ] 2.4 Map new fields in `get_teacher_settings_usecase.py` (`apps/backend/src/users/application/usecase/get_teacher_settings_usecase.py`)
- [ ] 2.5 Handle new fields in `update_teacher_settings_usecase.py` (`apps/backend/src/users/application/usecase/update_teacher_settings_usecase.py`) — persist only provided fields, preserve unchanged

## Phase 3: API Client Updates

- [ ] 3.1 Add 8 new optional fields to `TeacherSettingsUpdate` interface in `packages/api-client-ts/models/TeacherSettingsUpdate.ts`
- [ ] 3.2 Add 8 new fields to `TeacherSettingsResponse` interface in `packages/api-client-ts/models/TeacherSettingsResponse.ts`
- [ ] 3.3 Verify snake_case ↔ camelCase mapping for all new fields in the API client serialization layer

## Phase 4: Frontend Integration

- [ ] 4.1 Add 8 new fields to `TeacherSettingsData` interface in `apps/frontend/src/app/dashboard/settings/page.tsx`
- [ ] 4.2 Create Server Action `saveTeacherSettings` in `apps/frontend/src/app/actions/settings.ts` with Zod schema validation for all 12 fields
- [ ] 4.3 Wire `SettingsContent` component (`apps/frontend/src/components/settings/settings-content.tsx`) to initialize all 8 new selects/toggles from `initialSettings`
- [ ] 4.4 Connect "Guardar Cambios" button to call `saveTeacherSettings` Server Action with loading/success/error states
- [ ] 4.5 Update `useTheme` hook (`apps/frontend/src/components/theme/useTheme.ts`) to accept initial theme from backend and sync changes via debounced Server Action
- [ ] 4.6 Initialize `useTheme` with `initialSettings.theme` from backend on settings page load
- [ ] 4.7 Add toast notifications in Spanish: "Configuración guardada exitosamente" on success, "Error al guardar la configuración" on failure

## Phase 5: Testing

- [ ] 5.1 Write pytest unit test: `TeacherSettingsService.create_for_user` returns correct defaults for all 8 new fields
- [ ] 5.2 Write pytest integration test: `GET /professors/settings` returns all 12 fields for existing teacher
- [ ] 5.3 Write pytest integration test: `PUT /professors/settings` persists partial update without overwriting other fields
- [ ] 5.4 Write pytest integration test: `PUT /professors/settings` with `notificationFrequency: "instant"` normalizes to `"realtime"`
- [ ] 5.5 Write pytest integration test: `PUT /professors/settings` with invalid `dateFormat` returns 422
- [ ] 5.6 Verify frontend: run `npm run lint` and `npm run typecheck` in `apps/frontend/`
- [ ] 5.7 Verify backend: run `pytest` in `apps/backend/`
