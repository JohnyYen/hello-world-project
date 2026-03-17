# Tasks: Docker Infrastructure Refactor

## Phase 1: Foundation (Environment & Configuration)

- [x] 1.1 Create `infraestructure/docker/.env` with all centralized environment variables (PostgreSQL, Backend, Frontend, Game)
- [x] 1.2 Create `infraestructure/docker/.env.example` template without secrets for developers
- [x] 1.3 Verify `.env` syntax and required variables match spec

## Phase 2: Core Implementation (Compose Files)

- [x] 2.1 Create `infraestructure/docker/docker-compose.prod.yml` production overlay with image-based services
- [x] 2.2 Modify `infraestructure/docker/docker-compose.dev.yml` to consolidate all 4 services (postgresql_db, backend, frontend, game)
- [x] 2.3 Add health checks to postgresql_db using `pg_isready` (per spec)
- [x] 2.4 Add health checks to backend service
- [x] 2.5 Add restart policies (`restart: unless-stopped`) to all services
- [x] 2.6 Configure `depends_on` with `condition: service_healthy` for backend→postgresql_db

## Phase 3: Verification

- [x] 3.1 Run `docker compose -f infraestructure/docker/docker-compose.dev.yml config` - must exit code 0
- [x] 3.2 Run `docker compose -f infraestructure/docker/docker-compose.prod.yml config` - must exit code 0
- [x] 3.3 Verify dev compose can use prod as base: `docker compose -f infraestructure/docker/docker-compose.prod.yml -f infraestructure/docker/docker-compose.dev.yml config`
- [x] 3.4 Verify all 4 services are listed: postgresql_db, backend, frontend, game
- [x] 3.5 Test service startup order with health checks (if docker available)

## Phase 4: Cleanup

- [x] 4.1 Delete `apps/backend/docker-compose.yml` - must NOT exist after refactoring
- [x] 4.2 Verify Makefile commands work with new compose paths
- [x] 4.3 Remove scattered `.env` files at `apps/backend/.env` and `apps/frontend/.env` from docker-compose variable sourcing

## Dependencies

- Phase 1 must complete before Phase 2.3-2.6 (env vars needed for health checks)
- Phase 2 must complete before Phase 3
- Phase 3 must pass before Phase 4