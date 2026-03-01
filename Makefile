.PHONY: up down build restart logs shell psql test help

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  up       Start the stack (detached)"
	@echo "  down     Stop and remove containers"
	@echo "  build    Rebuild the Odoo image"
	@echo "  restart  Restart the Odoo service"
	@echo "  logs     Follow Odoo logs"
	@echo "  shell    Open a shell inside the Odoo container"
	@echo "  psql     Open psql inside the database container"
	@echo "  test     Run Odoo module tests"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build --no-cache

restart:
	docker compose restart odoo

logs:
	docker compose logs -f odoo

shell:
	docker compose exec odoo bash

psql:
	docker compose exec db psql -U $${POSTGRES_USER:-odoo}

test:
	docker compose run --rm odoo \
		odoo --test-enable --test-tags /worklog -i worklog -d odoo_test --stop-after-init --log-level=test
