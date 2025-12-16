.PHONY: help install dev test build up down logs clean

# Variables
DOCKER_COMPOSE = docker-compose
BACKEND_SERVICE = backend
POSTGRES_SERVICE = postgres
REDIS_SERVICE = redis

help:  ## Show this help message
	@echo 'Management commands for TPMS:'
	@echo ''
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install dependencies
	pip install -r requirements.txt

dev:  ## Run development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:  ## Run tests
	pytest tests/ -v --tb=short

test-coverage:  ## Run tests with coverage
	pytest tests/ -v --tb=short --cov=app --cov-report=html

build:  ## Build Docker images
	$(DOCKER_COMPOSE) build

up:  ## Start all services
	$(DOCKER_COMPOSE) up -d

down:  ## Stop all services
	$(DOCKER_COMPOSE) down

restart:  ## Restart all services
	$(DOCKER_COMPOSE) restart

logs:  ## Show logs for all services
	$(DOCKER_COMPOSE) logs -f

logs-backend:  ## Show logs for backend service
	$(DOCKER_COMPOSE) logs -f $(BACKEND_SERVICE)

logs-postgres:  ## Show logs for postgres service
	$(DOCKER_COMPOSE) logs -f $(POSTGRES_SERVICE)

logs-redis:  ## Show logs for redis service
	$(DOCKER_COMPOSE) logs -f $(REDIS_SERVICE)

migrate:  ## Run database migrations
	alembic upgrade head

migrate-create:  ## Create new migration
	alembic revision --autogenerate -m "$(message)"

shell:  ## Open shell in backend container
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) /bin/bash

psql:  ## Open psql shell
	$(DOCKER_COMPOSE) exec $(POSTGRES_SERVICE) psql -U tpms -d tpms_db

redis-cli:  ## Open redis-cli
	$(DOCKER_COMPOSE) exec $(REDIS_SERVICE) redis-cli

clean:  ## Clean up Docker resources
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f

format:  ## Format code with black
	black app/ tests/

lint:  ## Run linting with flake8
	flake8 app/ tests/

type-check:  ## Run type checking with mypy
	mypy app/

pre-commit:  ## Run pre-commit hooks
	pre-commit run --all-files

deploy:  ## Deploy application
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d

rollback:  ## Rollback to specific version
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml down
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d

status:  ## Show service status
	$(DOCKER_COMPOSE) ps

health:  ## Check service health
	curl -f http://localhost:8000/health || exit 1

celery-worker:  ## Run Celery worker
	celery -A app.core.celery worker --loglevel=info

celery-beat:  ## Run Celery beat
	celery -A app.core.celery beat --loglevel=info

celery-flower:  ## Run Celery Flower
	celery -A app.core.celery flower --port=5555

backup-db:  ## Backup database
	$(DOCKER_COMPOSE) exec $(POSTGRES_SERVICE) pg_dump -U tpms tpms_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:  ## Restore database from backup
	$(DOCKER_COMPOSE) exec -i $(POSTGRES_SERVICE) psql -U tpms -d tpms_db < $(file)