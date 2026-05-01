COMPOSE_FILE=infra/docker/docker-compose.yml

up:
	docker compose -f $(COMPOSE_FILE) up --build

down:
	docker compose -f $(COMPOSE_FILE) down

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

ps:
	docker compose -f $(COMPOSE_FILE) ps

restart:
	docker compose -f $(COMPOSE_FILE) down
	docker compose -f $(COMPOSE_FILE) up --build

clean:
	docker compose -f $(COMPOSE_FILE) down -v

api-shell:
	docker exec -it knowledgeops_api bash

db-shell:
	docker exec -it knowledgeops_postgres psql -U postgres -d knowledgeops

migrate-current:
	cd apps/api && . .venv/bin/activate && python -m alembic current

migrate-up:
	cd apps/api && . .venv/bin/activate && python -m alembic upgrade head

migrate-new:
	cd apps/api && . .venv/bin/activate && python -m alembic revision --autogenerate -m "$(msg)"

backup-db:
	docker exec -t knowledgeops_postgres pg_dump -U postgres knowledgeops > backup.sql

restore-db:
	cat backup.sql | docker exec -i knowledgeops_postgres psql -U postgres -d knowledgeops

reset-db:
	docker compose -f infra/docker/docker-compose.yml down -v
	docker compose -f infra/docker/docker-compose.yml up --build -d
	sleep 5
	cd apps/api && . .venv/bin/activate && python -m alembic upgrade head
	docker compose -f infra/docker/docker-compose.yml ps

migrate-history:
	cd apps/api && . .venv/bin/activate && python -m alembic history

migrate-check:
	cd apps/api && . .venv/bin/activate && python -m alembic current
	cd apps/api && . .venv/bin/activate && python -m alembic history

test-api:
	cd apps/api && . .venv/bin/activate && pytest

test-api-cov:
	cd apps/api && . .venv/bin/activate && pytest --cov=app --cov-report=term-missing --cov-fail-under=30

test-unit:
	cd apps/api && . .venv/bin/activate && pytest -m unit

test-integration:
	cd apps/api && . .venv/bin/activate && pytest -m integration

lint-api:
	cd apps/api && . .venv/bin/activate && ruff check .

format-api:
	cd apps/api && . .venv/bin/activate && ruff format .