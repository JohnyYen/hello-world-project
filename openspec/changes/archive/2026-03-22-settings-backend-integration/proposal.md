# Proposal: Settings Backend Integration

## Intent

La página de configuración del frontend muestra ~15 campos pero el backend solo soporta 4 campos básicos. Además, el campo `notification_frequency` tiene valores incompatibles ("instant" vs "realtime") y el tema no se persiste en el backend.

El objetivo es expandir el modelo del backend para soportar todos los campos del frontend Y garantizar que cada campo mostrado en UI esté sincronizado bidireccionalmente con el backend.

## Scope

### In Scope
1. Expandir modelo TeacherSettings con 8 nuevos campos
2. Corregir mapeo de notification_frequency
3. Theme dual-sync (useTheme + backend)
4. Botón "Guardar Cambios" funcional
5. Actualizar API client

### Out of Scope
- Funcionalidad de seguridad (2FA, cambiar contraseña)
- Integraciones con LMS (Google Classroom, Moodle)
- Migraciones de base de datos (se harán como parte del scope)

## Approach

Expandir modelo → Actualizar schemas → Conectar frontend → Migration

## Affected Areas

| Area | Impact |
|------|--------|
| `apps/backend/src/users/domain/teacher_settings.py` | Modified |
| `apps/backend/src/users/api/v1/schemas/teacher.py` | Modified |
| `apps/backend/src/users/application/usecase/` | Modified |
| `apps/frontend/src/app/dashboard/settings/page.tsx` | Modified |
| `apps/frontend/src/components/settings/settings-content.tsx` | Modified |
| `apps/frontend/src/components/theme/useTheme.ts` | Modified |
| `apps/frontend/src/app/actions/settings.ts` | New |
| `packages/api-client-ts/` | Regenerated |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Breaking existing API | Medium | Backward compatibility con campos opcionales |
| Migration conflicts | Low | Valores por defecto seguros |
| useTheme + API race | Medium | Debounce en llamadas API |

## Rollback Plan

1. Revert migration: `alembic downgrade -1`
2. Revert schemas: Volver a 4 campos originales
3. Revert frontend: Restaurar valores hardcoded

## Success Criteria

- [x] GET /settings devuelve todos los 12 campos
- [x] PUT /settings guarda todos los campos correctamente
- [x] Theme toggle refleja cambios inmediatamente Y persiste al backend
- [x] notification_frequency muestra "instant" como "En tiempo real"
- [x] Botón "Guardar Cambios" muestra feedback de éxito
- [x] Valores por defecto correctos para nuevos usuarios
