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
	docker compose -f docker-compose.dev.yml up -d

down:
	docker compose -f docker-compose.dev.yml down

build:
	docker compose -f docker-compose.dev.yml build --no-cache

restart:
	docker compose -f docker-compose.dev.yml restart odoo_dev

logs:
	docker compose -f docker-compose.dev.yml logs -f odoo_dev

shell:
	docker compose -f docker-compose.dev.yml exec odoo_dev bash

psql:
	docker compose -f docker-compose.dev.yml exec db_dev psql -U $${POSTGRES_USER:-odoo}

test:
	docker compose -f docker-compose.dev.yml run --rm odoo_dev \
		odoo --test-enable --test-tags /worklog -i worklog -d odoo_test --stop-after-init --log-level=test
