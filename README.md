# odoo_lab

Odoo 18 DevOps portfolio project — custom module development, Docker packaging, and CI with GitHub Actions.

## Stack

| Layer      | Technology              |
|------------|-------------------------|
| App        | Odoo 18.0               |
| Database   | PostgreSQL 14           |
| Container  | Docker + Compose        |
| CI         | GitHub Actions          |
| Registry   | GitHub Container Registry (ghcr.io) |

## Architecture

```
┌─────────────────────────────────┐
│         docker-compose          │
│                                 │
│  ┌─────────┐    ┌────────────┐  │
│  │  odoo   │───▶│ postgresql │  │
│  │ :18.0   │    │    :14     │  │
│  └─────────┘    └────────────┘  │
│       │                         │
│  /mnt/extra-addons/worklog      │
└─────────────────────────────────┘
```

Custom module `worklog` is baked into the image at build time via `COPY addons/ /mnt/extra-addons/`.

## Module: worklog

Lightweight time tracking for projects and technologies.

- Log time entries per project (Odoo, Azure, Django, ...)
- Tag entries by technology (Python, Docker, CI/CD, ...)
- Computed total time per project
- Start / Stop / Continue timer actions
- One running timer per user enforced

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

1. Build the Docker image
2. Run Odoo module tests (`worklog` only)

```
push to 18.0-dev
       ↓
  Build image
       ↓
  Run tests
```

## Project Structure

```
odoo_lab/
├── .github/workflows/ci.yml   # GitHub Actions pipeline
├── addons/
│   └── worklog/               # Custom Odoo module
│       ├── models/
│       │   ├── worklog_entry.py
│       │   ├── worklog_project.py
│       │   └── worklog_tag.py
│       ├── views/
│       ├── security/
│       └── tests/
├── docker/
│   ├── Dockerfile
│   └── odoo.conf
├── docker-compose.yml
├── Makefile
└── .env.example
```
