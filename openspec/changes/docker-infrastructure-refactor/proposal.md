# Proposal: Docker Infrastructure Refactor

## Intent

The current Docker setup is fragmented with duplicate compose files and scattered environment variables across the monorepo. This causes:
- Inconsistent DB credentials between `infraestructure/docker/docker-compose.dev.yml` and `apps/backend/docker-compose.yml`
- Unclear ownership of environment configuration (3 separate `.env` files with different purposes)
- No production compose file exists
- Makefile references are misaligned with actual compose file locations

This refactor consolidates all Docker configuration into `infraestructure/docker/` for single source of truth.

## Scope

### In Scope
- Consolidate all Docker compose files into `infraestructure/docker/`
- Create separate `docker-compose.dev.yml` and `docker-compose.prod.yml` files
- Centralize all environment variables into `infraestructure/docker/.env` with proper defaults
- Remove duplicate `apps/backend/docker-compose.yml`
- Update Makefile to reference correct compose files
- Ensure all 4 services work: PostgreSQL, Backend, Frontend, Game export

### Out of Scope
- Game app development container (only export Dockerfile, no dev container)
- CI/CD pipeline modifications
- Kubernetes or cloud deployment configs
- Database migrations or schema changes

## Approach

### Option A: Single Compose with Overlays (Recommended)
Keep `docker-compose.dev.yml` as base, use `-f` flag to layer prod overrides. Simpler maintenance.

### Option B: Complete Separation
Fully separate `docker-compose.dev.yml` and `docker-compose.prod.yml` with no file sharing. More explicit but more duplication.

**Chosen Approach**: Option A - Single compose with overrides for maintainability.

### Implementation Steps:
1. Migrate `apps/backend/docker-compose.yml` service definitions to `infraestructure/docker/docker-compose.dev.yml`
2. Create `infraestructure/docker/docker-compose.prod.yml` with production images (no build context)
3. Consolidate all env vars into `infraestructure/docker/.env` with commented sections
4. Update Makefile docker commands to use `infraestructure/docker/docker-compose.dev.yml`
5. Delete redundant `apps/backend/docker-compose.yml` and empty `infraestructure/docker/.env`

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `infraestructure/docker/docker-compose.dev.yml` | Modified | Add missing services from apps/backend/, consolidate |
| `infraestructure/docker/docker-compose.prod.yml` | New | Production compose with pre-built images |
| `infraestructure/docker/.env` | Modified | Centralize all env vars with defaults |
| `apps/backend/docker-compose.yml` | Removed | Duplicate file to delete |
| `Makefile` | Modified | Update compose file paths |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Breaking existing dev workflows | Medium | Test all `make docker-*` commands before commit |
| Database connection failures | Low | Use same PostgreSQL 15, just relocate config |
| Lost custom env var overrides | Low | Audit all `.env` files before consolidation |

## Rollback Plan

1. Restore `apps/backend/docker-compose.yml` from git
2. Restore original Makefile targets
3. Move `.env` variables back to original locations
4. Revert any changes to `infraestructure/docker/docker-compose.dev.yml`

## Dependencies

- None - this is an internal infrastructure refactor

## Success Criteria

- [ ] `docker compose -f infraestructure/docker/docker-compose.dev.yml config` validates successfully
- [ ] All 4 services (postgresql_db, backend, frontend, game) defined in dev compose
- [ ] No duplicate compose files remain in apps/
- [ ] Makefile docker commands work without errors
- [ ] Environment variables centralized in single `.env` file
- [ ] Production compose file created with image-based deployment
