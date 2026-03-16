# odoo-lab

Python Backend and DevOps portfolio — custom module development, Docker packaging, and CI/CD with GitHub Actions.

## Stack

| Layer         | Technology              |
|---------------|-------------------------|
| App           | Odoo 18.0               |
| Database      | PostgreSQL 14           |
| Container     | Docker + Compose        |
| Reverse Proxy | nginx                   |
| CI/CD         | GitHub Actions          |

## Bundled add-ons

The image includes a second add-on pulled at build time via a multi-stage Docker build:

- **[web_dark_mode](https://github.com/OCA/web/tree/18.0/web_dark_mode)** (OCA) — optional dark theme; install it from the Apps menu if you want it.

## Module: Worklog

Lightweight time tracking for side projects, create tasks, and check used technologies.

- Manage projects with a Kanban board (Draft → Backlog → Do → Done)
- Break projects down into tasks with their own Kanban pipeline (Draft → Backlog → Do → Staging → Prod → Done)
- Log time entries per task
- Tag tasks with technologies (Python, Docker, ...)
- Time stats on projects, tasks, and technologies: today, last 7 days, last 30 days, total
- Start / Stop / Continue timer actions on time entries

## Prerequisites

- Docker + Docker Compose
- make

## Quick Start

```bash
cp .env.example .env
# edit .env: set POSTGRES_PASSWORD

make up
```

Open http://localhost:8069

## Commands

```bash
make up       # Start the stack
make down     # Stop and remove containers
make build    # Rebuild the Odoo image (--no-cache)
make restart  # Restart only the Odoo container
make logs     # Follow Odoo logs
make shell    # Shell inside the Odoo container
make psql     # psql inside the database container
make test     # Run Odoo module tests (worklog)
```

## CI Pipeline

On every push to `18.0-dev`:

1. Lint with `ruff`
2. Build the Docker image
3. Run Odoo module tests (`worklog` only)
