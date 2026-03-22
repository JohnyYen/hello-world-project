# Design: Settings Backend Integration

## Technical Approach

Expand the TeacherSettings model from 4 to 12 fields, implement dual-sync for theme (useTheme + backend), connect all UI fields to backend, and add Server Action for save functionality. Backend follows Clean Architecture (Service/UseCase pattern), frontend uses Server Components with client-side mutations via Server Actions.

## Architecture Decisions

### Decision: notification_frequency Value Mapping

**Choice**: Change backend value from "instant" to "realtime" to match frontend
**Alternatives considered**: Add mapping layer in frontend (instant → "En tiempo real")
**Rationale**: Single source of truth in backend; frontend display logic stays clean; avoids future mapping bugs

### Decision: Theme Dual-Sync Strategy

**Choice**: Use next-themes for immediate UI update, async backend sync via Server Action with debounce
**Alternatives considered**: (1) Pure server-side theme (slow), (2) LocalStorage only (no persistence), (3) Blocking backend call on theme toggle (UI lag)
**Rationale**: Provides instant feedback (perceived performance) while persisting to backend; debounce prevents API spam on rapid toggles

### Decision: Save Strategy

**Choice**: Server Action with Zod validation instead of direct API client call
**Alternatives considered**: (1) Direct API client from component, (2) Form with server component action
**Rationale**: Server Actions provide type safety, automatic revalidation, and follow Next.js 15 patterns; Zod ensures validation before DB operations

### Decision: New Fields as Nullable with Defaults

**Choice**: Add new columns as nullable with application-level defaults
**Alternatives considered**: (1) NOT NULL with DEFAULT values in DB, (2) Separate settings JSON column
**Rationale**: Backward compatibility for existing users; migration simpler (no data conversion); service layer handles defaults

## Data Flow

### Page Load Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SERVER COMPONENT                              │
│  ┌──────────────┐                                                  │
│  │ settings/    │                                                  │
│  │ page.tsx     │──imports──▶ getTeacherSettings()                │
│  └──────────────┘            │                                     │
│                               ▼                                     │
│                    ┌──────────────────┐                            │
│                    │ users.ts service │                            │
│                    └────────┬─────────┘                            │
│                             │                                       │
│                             ▼                                       │
│                    ┌──────────────────┐                            │
│                    │  UsersApi.get    │                            │
│                    │  /professors/    │                            │
│                    │  settings        │                            │
│                    └────────┬─────────┘                            │
└─────────────────────────────┼─────────────────────────────────────┘
                              │ returns TeacherSettingsData
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT COMPONENT                              │
│  ┌───────────────────┐    ┌────────────────────┐                    │
│  │ SettingsContent  │◀───│ initialSettings   │                    │
│  │ receives data    │    │ (12 fields)       │                    │
│  └───────────────────┘    └────────────────────┘                    │
│           │                                                        │
│           ▼                                                        │
│  ┌───────────────────┐    ┌────────────────────┐                    │
│  │ useTheme provider│◀───│ initialSettings   │                    │
│  │ sets theme       │    │ .theme            │                    │
│  └───────────────────┘    └────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Theme Toggle Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│ CLIENT                                                              │
│ ┌──────────────┐      ┌────────────────┐      ┌─────────────────┐  │
│ │ ThemeToggle  │─────▶│ useTheme.ts    │─────▶│ setTheme()     │  │
│ │ (component)  │      │ next-themes   │      │ (immediate UI) │  │
│ └──────────────┘      └────────────────┘      └────────┬────────┘  │
│                                                        │           │
│                                                        ▼           │
│                                              ┌─────────────────┐   │
│                                              │ updateTheme()   │   │
│                                              │ Server Action  │   │
│                                              │ (async,         │   │
│                                              │  debounced)    │   │
│                                              └────────┬────────┘   │
└───────────────────────────────────────────────────────┼────────────┘
                                                        │ PUT /settings
                                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│ BACKEND                                                             │
│ ┌────────────────┐    ┌───────────────┐    ┌──────────────────────┐ │
│ │ PUT endpoint  │───▶│ UpdateUseCase │───▶│ TeacherSettingsRepo  │ │
│ │ /professors/  │    │               │    │ .update()            │ │
│ │ settings      │    └───────────────┘    └──────────────────────┘ │
│ └────────────────┘                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Save Changes Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│ CLIENT                                                              │
│ ┌──────────────────┐      ┌─────────────────────────────────────┐  │
│ │ SettingsContent │─────▶│ saveTeacherSettings() Server Action │  │
│ │ "Guardar Cambios│      │ (Zod validation)                     │  │
│ │ button          │      └──────────────┬──────────────────────┘  │
│ └──────────────────┘                     │                        │
│                                          │ PUT /professors/settings│
│                                          ▼                        │
│                               ┌─────────────────────────────────┐  │
│                               │ UsersApi.updateTeacherSettings │  │
│                               │ (api-client-ts)                 │  │
│                               └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `apps/backend/src/users/domain/teacher_settings.py` | Modify | Add 8 new columns (auto_logout, session_duration_minutes, remember_login, color_theme, animations_enabled, email_notifications, date_format, timezone) |
| `apps/backend/src/users/api/v1/schemas/teacher.py` | Modify | Add fields to TeacherSettingsUpdate/Response Pydantic schemas |
| `apps/backend/src/users/application/usecase/get_teacher_settings_usecase.py` | Modify | Map new fields to response |
| `apps/backend/src/users/application/usecase/update_teacher_settings_usecase.py` | Modify | Handle new fields in update |
| `apps/backend/src/users/application/service/teacher_settings_service.py` | Modify | Add create_for_user method with defaults for new fields |
| `apps/backend/migrations/versions/add_teacher_settings_fields.py` | Create | Alembic migration for new columns |
| `packages/api-client-ts/models/TeacherSettingsResponse.ts` | Modify | Add new fields to interface + snake_case mapping |
| `packages/api-client-ts/models/TeacherSettingsUpdate.ts` | Modify | Add new fields to interface + snake_case mapping |
| `apps/frontend/src/app/dashboard/settings/page.tsx` | Modify | Add new fields to TeacherSettingsData interface |
| `apps/frontend/src/components/settings/settings-content.tsx` | Modify | Connect all fields to initialSettings, add state + Server Action, wire "Guardar Cambios" button |
| `apps/frontend/src/components/theme/useTheme.ts` | Modify | Add backend sync capability with debounce |
| `apps/frontend/src/app/actions/settings.ts` | Create | Server Action for saveTeacherSettings with Zod validation |

## Interfaces / Contracts

### Backend API Contract

#### GET /professors/settings Response

```typescript
interface TeacherSettingsResponse {
  theme: string;                    // "light" | "dark"
  notificationsEnabled: boolean;
  notificationFrequency: string;   // "realtime" | "daily" | "weekly" | "disabled"
  interfaceLanguage: string;        // "es" | "en"
  // NEW FIELDS
  autoLogout: boolean;
  sessionDurationMinutes: number;   // 0 = permanent
  rememberLogin: boolean;
  colorTheme: string;               // "Indigo" | "Violeta" | "Esmeralda" | "Azul" | "Rosa" | "Naranja"
  animationsEnabled: boolean;
  emailNotifications: boolean;
  dateFormat: string;                // "ddmmyyyy" | "mmddyyyy" | "yyyymmdd"
  timezone: string;                 // "gmt-5" | "gmt-6" | "gmt-3" | "gmt0" | "gmt1"
}
```

#### PUT /professors/settings Request

```typescript
interface TeacherSettingsUpdate {
  theme?: string | null;
  notificationsEnabled?: boolean | null;
  notificationFrequency?: string | null;
  interfaceLanguage?: string | null;
  // NEW FIELDS
  autoLogout?: boolean | null;
  sessionDurationMinutes?: number | null;
  rememberLogin?: boolean | null;
  colorTheme?: string | null;
  animationsEnabled?: boolean | null;
  emailNotifications?: boolean | null;
  dateFormat?: string | null;
  timezone?: string | null;
}
```

### Frontend Type Contract

```typescript
interface TeacherSettingsData {
  theme: string;
  notificationsEnabled: boolean;
  notificationFrequency: string;
  interfaceLanguage: string;
  autoLogout: boolean;
  sessionDurationMinutes: number;
  rememberLogin: boolean;
  colorTheme: string;
  animationsEnabled: boolean;
  emailNotifications: boolean;
  dateFormat: string;
  timezone: string;
}
```

### Server Action Contract

```typescript
// apps/frontend/src/app/actions/settings.ts
"use server"

import { z } from "zod"

const TeacherSettingsSchema = z.object({
  theme: z.enum(["light", "dark"]).optional(),
  notificationsEnabled: z.boolean().optional(),
  notificationFrequency: z.enum(["realtime", "daily", "weekly", "disabled"]).optional(),
  interfaceLanguage: z.enum(["es", "en"]).optional(),
  autoLogout: z.boolean().optional(),
  sessionDurationMinutes: z.number().min(0).optional(),
  rememberLogin: z.boolean().optional(),
  colorTheme: z.enum(["Indigo", "Violeta", "Esmeralda", "Azul", "Rosa", "Naranja"]).optional(),
  animationsEnabled: z.boolean().optional(),
  emailNotifications: z.boolean().optional(),
  dateFormat: z.enum(["ddmmyyyy", "mmddyyyy", "yyyymmdd"]).optional(),
  timezone: z.enum(["gmt-5", "gmt-6", "gmt-3", "gmt0", "gmt1"]).optional(),
})

async function saveTeacherSettings(data: z.infer<typeof TeacherSettingsSchema>): Promise<{ success: boolean; message: string }> {
  // Validate → API call → Return result
}
```

### Field Mapping: Frontend ↔ API Client ↔ Backend

| Frontend (camelCase) | API Client (camelCase) | Backend (snake_case) | Type | Default |
|---------------------|----------------------|---------------------|------|---------|
| `theme` | `theme` | `theme` | string | "light" |
| `notificationsEnabled` | `notificationsEnabled` | `notifications_enabled` | boolean | true |
| `notificationFrequency` | `notificationFrequency` | `notification_frequency` | string | "realtime" |
| `interfaceLanguage` | `interfaceLanguage` | `interface_language` | string | "es" |
| `autoLogout` | `autoLogout` | `auto_logout` | boolean | false |
| `sessionDurationMinutes` | `sessionDurationMinutes` | `session_duration_minutes` | number | 60 |
| `rememberLogin` | `rememberLogin` | `remember_login` | boolean | true |
| `colorTheme` | `colorTheme` | `color_theme` | string | "Indigo" |
| `animationsEnabled` | `animationsEnabled` | `animations_enabled` | boolean | true |
| `emailNotifications` | `emailNotifications` | `email_notifications` | boolean | false |
| `dateFormat` | `dateFormat` | `date_format` | string | "ddmmyyyy" |
| `timezone` | `timezone` | `timezone` | string | "gmt-5" |

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | TeacherSettingsService default values, Zod schema validation | pytest with fixtures |
| Unit | useTheme debounce logic, Server Action validation | Jest unit tests |
| Integration | GET/PUT endpoints return new fields correctly | pytest + test client |
| Integration | Server Action flow | Manual E2E or Playwright |
| E2E | Full settings page load, toggle theme, save changes | Playwright |

## Migration / Rollout

### Migration Strategy

1. **Create migration**: `alembic revision --autogenerate -m "add teacher_settings new fields"`
2. **Add columns as nullable**: All 8 new fields nullable
3. **Deploy backend**: New columns available
4. **Deploy frontend**: Uses new fields (backward compatible if missing)
5. **Data backfill**: Service layer applies defaults for NULL values

### Default Values (Application Level)

| Field | Default |
|-------|---------|
| autoLogout | false |
| sessionDurationMinutes | 60 |
| rememberLogin | true |
| colorTheme | "Indigo" |
| animationsEnabled | true |
| emailNotifications | false |
| dateFormat | "ddmmyyyy" |
| timezone | "gmt-5" |

### Rollback Plan

1. `alembic downgrade -1` (remove columns)
2. Revert backend schemas to 4 fields
3. Revert frontend to use hardcoded values for new fields
4. Redeploy services

## Open Questions

- [ ] Should session_duration_minutes = 0 mean "permanent session" or "no session limit"? (Currently treating as permanent)
- [ ] Are there existing users that need data migration for notification_frequency = "instant" → "realtime"?
- [ ] Should the theme toggle trigger immediate backend save or wait for "Guardar Cambios" button? (Current design: immediate via debounced Server Action)
