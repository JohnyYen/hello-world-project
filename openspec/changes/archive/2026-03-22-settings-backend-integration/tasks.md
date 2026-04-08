# Tasks: Settings Backend Integration

## Phase 1: Backend Model Expansion + Migration

- [x] 1.1 Add 8 new nullable columns to `TeacherSettings` model in `apps/backend/src/users/domain/teacher_settings.py`: `auto_logout` (bool), `session_duration_minutes` (int), `remember_login` (bool), `color_theme` (str), `animations_enabled` (bool), `email_notifications` (bool), `date_format` (str), `timezone` (str)
- [x] 1.2 Generate Alembic migration via `alembic revision --autogenerate -m "add teacher_settings new fields"` in `apps/backend/`
- [x] 1.3 Verify migration file in `apps/backend/migrations/versions/` has correct nullable columns with no server defaults
- [x] 1.4 Update `create_for_user` method in `apps/backend/src/users/application/service/teacher_settings_service.py` to include application-level defaults for all 8 new fields

## Phase 2: Backend Schemas + Endpoints

- [x] 2.1 Add 8 new optional fields to `TeacherSettingsUpdate` Pydantic schema in `apps/backend/src/users/api/v1/schemas/teacher.py`
- [x] 2.2 Add 8 new fields to `TeacherSettingsResponse` Pydantic schema in `apps/backend/src/users/api/v1/schemas/teacher.py`
- [x] 2.3 Change `notification_frequency` validation from `"instant"` to `"realtime"` in the Pydantic schema + add Literal enum validation
- [x] 2.4 Map new fields in `get_teacher_settings_usecase.py` (`apps/backend/src/users/application/usecase/get_teacher_settings_usecase.py`)
- [x] 2.5 Handle new fields in `update_teacher_settings_usecase.py` (`apps/backend/src/users/application/usecase/update_teacher_settings_usecase.py`) — persist only provided fields, preserve unchanged

## Phase 3: API Client Updates

- [x] 3.1 Regenerate API client from updated OpenAPI spec (includes all 12 fields)
- [x] 3.2 Verify snake_case ↔ camelCase mapping for all new fields
- [x] 3.3 Restore package.json after regeneration

## Phase 4: Frontend Integration

- [x] 4.1 Add 8 new fields to `TeacherSettingsData` interface in `apps/frontend/src/app/dashboard/settings/page.tsx`
- [x] 4.2 Create Server Action `saveTeacherSettings` in `apps/frontend/src/app/actions/settings.ts` with Zod schema validation for all 12 fields
- [x] 4.3 Wire `SettingsContent` component (`apps/frontend/src/components/settings/settings-content.tsx`) to initialize all 8 new selects/toggles from `initialSettings`
- [x] 4.4 Connect "Guardar Cambios" button to call `saveTeacherSettings` Server Action with loading/success/error states
- [x] 4.5 Update `useTheme` hook (`apps/frontend/src/components/theme/useTheme.ts`) to sync theme changes via debounced Server Action
- [x] 4.6 Initialize `ThemeToggle` with `initialTheme` from backend on settings page
- [x] 4.7 Add toast notifications in Spanish: "Configuración guardada exitosamente" on success, error message on failure

## Phase 5: Verification & Fixes

- [x] 5.1 Verify API: GET returns all 12 fields
- [x] 5.2 Verify API: PUT persists partial update
- [x] 5.3 Fix: Add Literal enum validation on string fields
- [x] 5.4 Fix: Normalize "instant" to "realtime" in GET/PUT usecases
- [x] 5.5 Verify frontend with Playwright: settings load from API
- [x] 5.6 Verify verification report generated
- [x] 5.7 Update tasks.md with completion status
