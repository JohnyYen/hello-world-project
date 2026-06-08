# Hello World Project - Unified Development Commands

.PHONY: help dev dev-backend dev-frontend dev-docker test test-backend test-frontend lint lint-backend lint-frontend build build-frontend docker-up docker-down docker-logs clean clean-db stop

##@ Development
help: ## Show this help message
	@echo "Hello World Project - Makefile"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

dev: ## Start all services with Docker Compose
	docker compose -f infraestructure/docker/docker-compose.dev.no-game.yml up

dev-docker: ## Start all services (alias for dev)
	docker compose -f infraestructure/docker/docker-compose.dev.no-game.yml up

docker-up: ## Start all services
	docker compose -f infraestructure/docker/docker-compose.dev.no-game.yml up

docker-down: ## Stop all services
	docker compose -f infraestructure/docker/docker-compose.dev.no-game.yml down

stop: docker-down ## Stop all services (alias for docker-down)

docker-logs: ## Follow logs from all services
	docker compose -f infraestructure/docker/docker-compose.dev.no-game.yml logs -f

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
