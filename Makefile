# Hello World Project - Unified Development Commands

.PHONY: help dev dev-backend dev-frontend dev-docker test test-backend test-frontend lint lint-backend lint-frontend build build-frontend generate-api-client docker-up docker-down docker-logs clean clean-db stop

##@ Development
help: ## Show this help message
	@echo "Hello World Project - Makefile"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

dev: ## Start all services with Docker Compose
	docker compose -f infraestructure/docker/docker-compose.dev.yml up

dev-backend: ## Start backend with hot reload
	cd apps/backend && poetry run fastapi dev src/main.py --reload

dev-frontend: ## Start frontend with hot reload
	cd apps/frontend && pnpm dev

dev-docker: ## Start all services (alias for dev)
	docker compose -f infraestructure/docker/docker-compose.dev.yml up

##@ Database Seeding
seed-db: ## Seed database with test data (idempotent)
	./scripts/seed-database.sh

seed-db-reset: ## Reset and seed database (WARNING: destroys data)
	./scripts/seed-database.sh --reset

seed-db-help: ## Show database seeder help
	./scripts/seed-database.sh --help

seed-analytics: ## Seed analytics test data (students, courses by school year, sync events)
	docker cp apps/backend/src/src/shared/seed/seed_analytics_data.py hwp-backend:/app/src/shared/seed/seed_analytics_data.py
	docker exec hwp-backend bash -c "cd /app && export PYTHONPATH=/app && python3 src/shared/seed/seed_analytics_data.py"

##@ Testing
test: ## Run all tests
	$(MAKE) test-backend && $(MAKE) test-frontend

test-backend: ## Run backend tests
	cd apps/backend && poetry run pytest

test-frontend: ## Run frontend tests
	cd apps/frontend && pnpm test

##@ Linting
lint: ## Run all linters
	$(MAKE) lint-backend && $(MAKE) lint-frontend

lint-backend: ## Run backend linters
	cd apps/backend && poetry run ruff check . && poetry run ruff format --check .

lint-frontend: ## Run frontend linters
	cd apps/frontend && pnpm lint

##@ Building
build: ## Build all projects
	$(MAKE) build-frontend

build-frontend: ## Build frontend for production
	cd apps/frontend && pnpm build

##@ API Client
generate-api-client: ## Generate API client from OpenAPI spec
	bash scripts/generate-api-client.sh

##@ Docker
docker-up: ## Start all services
	docker compose -f infraestructure/docker/docker-compose.dev.yml up

docker-down: ## Stop all services
	docker compose -f infraestructure/docker/docker-compose.dev.yml down

stop: docker-down ## Stop all services (alias for docker-down)

docker-logs: ## Follow logs from all services
	docker compose -f infraestructure/docker/docker-compose.dev.yml logs -f

##@ Maintenance
clean: ## Clean cache and temp files
	@echo "Cleaning cache..."
	cd apps/frontend && rm -rf .next node_modules/.cache
	cd apps/backend && rm -rf __pycache__ .pytest_cache
	@echo "Done!"

##@ Database
clean-db: ## Clean database (WARNING: destroys all data)
	@echo "⚠️  Cleaning database..."
	cd apps/backend && uv run alembic downgrade base
	@echo "✅ Database cleaned!"
