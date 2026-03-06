# odoo_lab

Odoo 18 DevOps portfolio project — custom module development, Docker packaging, and CI with GitHub Actions.

## Stack

| Layer      | Technology              |
|------------|-------------------------|
| App        | Odoo 18.0               |
| Database   | PostgreSQL 14           |
| Container  | Docker + Compose        |
| CI         | GitHub Actions          |

## Module: Worklog

Lightweight time tracking for projects and technologies.

- Log time entries per project (odoo_lab, weather-app, ...)
- Link entries to technologies (Python, Docker, Django, ...)
- Computed total time per project
- Start / Stop / Continue timer actions
- One running timer per user enforced
- Module baked into the image at build time

## Prerequisites

- Docker + Docker Compose
- make

## Quick Start

```bash
cp .env.example .env
# edit .env and set POSTGRES_PASSWORD and ADMIN_PASSWORD

make up
```

Open http://localhost:8069

## Commands

```bash
make up       # Start the stack
make down     # Stop and remove containers
make build    # Rebuild the Odoo image
make restart  # Restart the Odoo service
make logs     # Follow Odoo logs
make shell    # Shell inside the Odoo container
make psql     # psql inside the database container
make test     # Run Odoo module tests
```

## CI Pipeline

On every push to `18.0-dev`:

1. Lint with `ruff`
2. Build the Docker image
3. Run Odoo module tests (`worklog` only)
