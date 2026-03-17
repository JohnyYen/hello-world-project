# Docker Infrastructure Specification

## Purpose

This specification defines the Docker-based development and production infrastructure for the Hello World Project monorepo. It establishes a unified, centralized configuration system that eliminates duplication, ensures consistency across environments, and provides a single source of truth for all containerized services.

## ADDED Requirements

### Requirement: Unified Compose File Structure

The infrastructure SHALL maintain exactly two compose files in `infraestructure/docker/`:
- `docker-compose.dev.yml` - Development environment with build contexts and hot-reload volumes
- `docker-compose.prod.yml` - Production environment with pre-built images

#### Scenario: Development compose file exists and is valid

- GIVEN the `infraestructure/docker/docker-compose.dev.yml` file exists
- WHEN running `docker compose -f infraestructure/docker/docker-compose.dev.yml config`
- THEN the command MUST exit with code 0 and produce valid configuration

#### Scenario: Production compose file exists and is valid

- GIVEN the `infraestructure/docker/docker-compose.prod.yml` file exists
- WHEN running `docker compose -f infraestructure/docker/docker-compose.prod.yml config`
- THEN the command MUST exit with code 0 and produce valid configuration

#### Scenario: Dev compose uses production as base via override

- GIVEN both `docker-compose.dev.yml` and `docker-compose.prod.yml` exist
- WHEN running `docker compose -f infraestructure/docker/docker-compose.prod.yml -f infraestructure/docker/docker-compose.dev.yml config`
- THEN the resulting configuration MUST be valid for development (override behavior)

---

### Requirement: Centralized Environment Variables

All environment variables for all services SHALL be defined in a single file: `infraestructure/docker/.env`

The centralized `.env` file MUST include the following variable groups:

**PostgreSQL Configuration:**
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password  
- `POSTGRES_DB` - Database name
- `POSTGRES_HOST` - Database host (for service-to-service communication)

**Backend Configuration:**
- `DATABASE_URL` - Full PostgreSQL connection string
- `SECRET_KEY` - Application secret for JWT/sessions
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `BACKEND_PORT` - Port for backend service (default: 8000)

**Frontend Configuration:**
- `NEXT_PUBLIC_API_URL` - Backend API URL accessible from browser
- `JWT_SECRET` - Secret for JWT verification in frontend
- `JWT_EXPIRES_IN` - JWT expiration duration
- `JWT_REFRESH_EXPIRES_IN` - Refresh token expiration duration
- `FRONTEND_PORT` - Port for frontend service (default: 3000)

**Game Configuration:**
- `GAME_PORT` - Port for exported game (if applicable)

#### Scenario: Centralized .env file loads all variables

- GIVEN the file `infraestructure/docker/.env` exists with all required variables
- WHEN running `docker compose -f infraestructure/docker/docker-compose.dev.yml config`
- THEN the output MUST include all environment variables from the `.env` file

#### Scenario: Variables can be overridden at runtime

- GIVEN `infraestructure/docker/.env` defines `POSTGRES_DB=hwp_db`
- WHEN running `POSTGRES_DB=custom_db docker compose -f infraestructure/docker/docker-compose.dev.yml config`
- THEN the resulting configuration MUST use `custom_db` instead of `hwp_db`

---

### Requirement: Service Network Configuration

All services MUST communicate over a shared Docker network named `hwp-network`.

The network configuration MUST ensure:
- Services CAN reach each other by container name
- External access is controlled via port mappings only
- Database is NOT exposed to the public internet

#### Scenario: Backend connects to PostgreSQL

- GIVEN all services are running in `hwp-network`
- WHEN the backend service connects to `postgresql_db:5432`
- THEN the connection MUST succeed because both containers share the network

#### Scenario: Frontend accesses backend API

- GIVEN frontend is running and backend is running
- WHEN frontend makes HTTP request to `http://backend:8000`
- THEN the request MUST succeed (internal network communication)

---

### Requirement: Volume Management for Persistence

The infrastructure MUST define the following named volumes:

- `postgresql_data` - PostgreSQL database files (MUST persist across restarts)
- `frontend_cache` - Next.js build cache (SHOULD persist for faster rebuilds)

#### Scenario: Database data persists across restarts

- GIVEN PostgreSQL container has `postgresql_data` volume mounted at `/var/lib/postgresql/data`
- WHEN the container is stopped and started again
- THEN all previously created databases and data MUST remain intact

#### Scenario: Anonymous volumes are avoided

- GIVEN the compose files are defined
- WHEN inspecting volume configurations
- THEN there MUST be no anonymous volumes (volumes without explicit names)

---

### Requirement: Service Health and Startup Order

Services with dependencies MUST use Docker's `depends_on` with `condition: service_healthy` to ensure proper startup order.

The health check configuration MUST be defined for:
- `postgresql_db` - Uses `pg_isready` to verify database readiness
- All services with dependencies SHOULD have appropriate health checks

#### Scenario: Backend starts only after PostgreSQL is healthy

- GIVEN `backend` service depends on `postgresql_db` with `condition: service_healthy`
- WHEN starting the stack with `docker compose up`
- THEN backend container MUST NOT start until `pg_isready` returns success

#### Scenario: Frontend starts after backend is running

- GIVEN `frontend` service depends on `backend`
- WHEN starting the stack
- THEN frontend container MUST start after backend container is running (not necessarily healthy)

---

### Requirement: Port Mapping Configuration

The following ports MUST be exposed for each service:

| Service | Host Port | Container Port | Protocol |
|---------|-----------|----------------|----------|
| postgresql_db | 5432 | 5432 | TCP |
| backend | 8000 | 8000 | TCP |
| frontend | 3000 | 3000 | TCP |
| game | 8080 | 8080 | TCP (if exported) |

#### Scenario: All services accessible on localhost

- GIVEN all services are running
- WHEN accessing `localhost:5432`, `localhost:8000`, `localhost:3000`
- THEN each port MUST respond with the appropriate service

---

### Requirement: Duplicate Compose File Removal

The file `apps/backend/docker-compose.yml` MUST NOT exist after refactoring.

#### Scenario: Duplicate compose file is removed

- GIVEN the refactoring is complete
- WHEN checking if `apps/backend/docker-compose.yml` exists
- THEN the file MUST NOT exist

---

### Requirement: Makefile Integration

The Makefile MUST reference only `infraestructure/docker/docker-compose.dev.yml` for all docker commands.

#### Scenario: Makefile docker commands work

- GIVEN the Makefile exists
- WHEN running `make docker-up`, `make docker-down`, or `make docker-logs`
- THEN each command MUST use `infraestructure/docker/docker-compose.dev.yml`

---

## MODIFIED Requirements

### Requirement: Service Definition Consolidation

The `docker-compose.dev.yml` MUST include ALL services from both existing compose files.

**Previously:** `infraestructure/docker/docker-compose.dev.yml` had 3 services (postgresql_db, backend, frontend), and `apps/backend/docker-compose.yml` had 2 services (backend, db) with DIFFERENT configurations.

**New:** Single `docker-compose.dev.yml` MUST contain exactly 4 services:
- `postgresql_db` - PostgreSQL 15 database
- `backend` - FastAPI application
- `frontend` - Next.js application  
- `game` - Godot export (build-only, no dev container per proposal scope)

#### Scenario: All four services are defined

- GIVEN `docker-compose.dev.yml` is valid
- WHEN running `docker compose -f infraestructure/docker/docker-compose.dev.yml config --services`
- THEN the output MUST list: postgresql_db, backend, frontend, game

---

## REMOVED Requirements

### Requirement: Scattered Environment Variables

(Reason: Environment variables were spread across 3 separate `.env` files with different purposes - this caused inconsistent credentials between dev and what apps expected)

The scattered `.env` files at:
- `apps/backend/.env`
- `apps/frontend/.env`

MUST NOT be used for docker-compose variable sourcing after refactoring.

### Requirement: Duplicate Backend Service Definition

(Reason: The duplicate `apps/backend/docker-compose.yml` had conflicting backend port (8080 vs 8000) and database credentials (postgres/postgres vs hwp_user/hwp_password) which caused confusion and connection failures)

The `apps/backend/docker-compose.yml` file is REMOVED entirely.

---

## Technical Details Summary

### Compose File Locations

```
infraestructure/docker/
├── docker-compose.dev.yml    # Development with build contexts
├── docker-compose.prod.yml   # Production with image references
└── .env                      # Centralized environment variables
```

### Service Definitions

**postgresql_db:**
- Image: `postgres:15`
- Ports: `5432:5432`
- Volume: `postgresql_data:/var/lib/postgresql/data`
- Health Check: `pg_isready -U ${POSTGRES_USER}`
- Environment: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

**backend:**
- Build: `../../apps/backend` with `Dockerfile.dev`
- Ports: `8000:8000`
- Volume: `../../apps/backend:/app` (hot reload)
- Depends On: `postgresql_db` (service_healthy)
- Environment: DATABASE_URL (from centralized .env)

**frontend:**
- Build: `../../apps/frontend` with `Dockerfile.dev`
- Ports: `3000:3000`
- Volume: `../../apps/frontend:/app` (hot reload)
- Depends On: `backend`
- Environment: NEXT_PUBLIC_API_URL (from centralized .env)

**game:**
- Build: `../../apps/game` with `Dockerfile`
- Purpose: Export-only, no runtime container in dev compose
- No ports exposed in dev (build artifact only)

### Network

- Network Name: `hwp-network`
- Driver: `bridge` (default)

### Volumes

| Volume Name | Driver | Purpose |
|-------------|--------|---------|
| postgresql_data | local | Database persistence |
| frontend_cache | local | Next.js cache (optional) |
