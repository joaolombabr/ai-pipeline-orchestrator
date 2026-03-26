.PHONY: up down build logs shell migrate

# Sobe todos os containers
up:
	docker compose up -d --build

# Derruba todos os containers
down:
	docker compose down

# Derruba e remove volumes (reset total)
reset:
	docker compose down -v --remove-orphans

# Build sem cache
build:
	docker compose build --no-cache

# Logs em tempo real
logs:
	docker compose logs -f

# Logs só da API
logs-api:
	docker compose logs -f api

# Logs só do worker
logs-worker:
	docker compose logs -f worker

# Shell dentro do container da API
shell:
	docker compose exec api bash

# Status dos containers
ps:
	docker compose ps

# Restart apenas da API
restart-api:
	docker compose restart api

# Abre o banco no psql
db:
	docker compose exec db psql -U pipeline_user -d pipeline_db
