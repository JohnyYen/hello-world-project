# Proposal: Fix Signup/Login Critical Bugs

## Intent

Corrigir los errores críticos que impiden el registro e inicio de sesión de usuarios:
- SIGNUP siempre retorna "Email o usuario ya existe" incluso con datos únicos
- El error real es: `column "lms_id" is of type integer but expression is of type uuid`
- El modelo User tiene `lms_id` como UUID pero la DB espera INTEGER
- LOGIN falla porque no hay usuarios (signup nunca funciona)

## Scope

### In Scope
- Verificar el estado de las migraciones de Alembic (`alembic current`)
- Verificar el tipo real de la columna `lms_id` en la base de datos
- Corregir el tipo de columna en la DB (migración) O actualizar el modelo
- Mejorar los mensajes de error en el frontend para mostrar errores reales

### Out of Scope
- Funcionalidad de LMS integration
- Cambios en la lógica de autenticación (JWT)
- Mejoras adicionales de UX en el formulario

## Approach

1. **Diagnóstico**: Verificar migraciones de Alembic y estado actual de la DB
2. **Corrección**: Si la DB tiene INTEGER, crear migración para cambiar a UUID. Si el modelo está mal, actualizar el modelo y crear migración
3. **Mejora de errores**: Actualizar el frontend para mostrar el error real del backend en lugar del mensaje genérico

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `apps/backend/src/users/domain/user.py` | Modified | Modelo User con lms_id como UUID |
| `apps/backend/migrations/` | Modified | Migración para corregir tipo de columna |
| `apps/backend/src/users/application/service/user_service.py` | Modified | Puede necesitar logging del error real |
| `apps/frontend/src/lib/actions.ts` | Modified | Mejorar mensajes de error en signupAction |
| `apps/frontend/src/services/auth.ts` | Modified | Mejorar manejo de errores en register |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Migración fallida | Med | Hacer backup de la DB antes de ejecutar |
| Incompatibilidad con datos existentes | Baja | Verificar datos actuales de lms_id |
| Frontend no muestra error real | Baja | Agregar logging detallado en el backend |

## Rollback Plan

1. Revertir la migración ejecutando `alembic downgrade {revision}`
2. Revertir cambios en el modelo si es necesario
3. Restaurar el mensaje de error genérico en el frontend

## Dependencies

- PostgreSQL debe estar disponible y accesible
- Acceso a la base de datos para ejecutar migraciones

## Success Criteria

- [ ] Usuario puede registrarse con datos válidos
- [ ] Usuario puede iniciar sesión con credenciales válidas
- [ ] Error de tipo mismatch en lms_id está resuelto
- [ ] Frontend muestra mensajes de error claros y específicos