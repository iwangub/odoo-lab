# odoo-lab

Python Backend and DevOps portfolio — Odoo deployment with custom module development, Docker packaging, CI/CD automation, and configuration management.

**Live Environments:**
- Production: https://odoo.dev-lab.dev
- Staging: https://staging-odoo.dev-lab.dev

Both run on a Hetzner Cloud VM (Ubuntu 24.04), configured with Ansible and deployed via GitHub Actions.

## Architecture

```
                         ┌──────────────────────────────────────┐
                         │         Hetzner Cloud (cx23)         │
  GitHub Actions         │                                      │
  ┌──────────┐    SSH    │  ┌───────┐    ┌──────┐   ┌──────┐    │
  │ CI/CD    │──────────►│  │ nginx │───►│ Odoo │──►│  DB  │    │
  │          │   GHCR    │  │  :443 │    │ :8069│   │ PG14 │    │
  └──────────┘──────────►│  └───────┘    └──────┘   └──────┘    │
                         │       │       ┌──────────┐┌──────┐   │
  Ansible                │       └──────►│ Odoo Stg ││DB Stg│   │
  ┌──────────┐           │               │  :8069   ││ PG14 │   │
  │ Configure│──────────►│               └──────────┘└──────┘   │
  └──────────┘           └──────────────────────────────────────┘
```

## Stack

| Layer                | Technology                       |
|----------------------|----------------------------------|
| Application          | Odoo 18.0 (custom worklog module)|
| Database             | PostgreSQL 14                    |
| Containerization     | Docker + Compose     |
| Reverse Proxy        | nginx (SSL/TLS via Let's Encrypt)|
| CI/CD                | GitHub Actions (5 workflows)     |
| Configuration Mgmt   | Ansible (roles, cron, backups)   |
| Code Quality         | ruff (lint in CI)                |

## Module: Worklog

Lightweight time tracking for side projects — manage tasks, log hours, and track technology usage.

- **Projects** with Kanban board (Draft / Backlog / Do / Done)
- **Tasks** with 6-state pipeline (Draft / Backlog / Do / Staging / Prod / Done)
- **Time entries** with Start / Stop / Continue timer actions
- **Technology tags** (Python, Docker, Ansible, Terraform, ...) with aggregated time stats
- **Time stats** on projects, tasks, and technologies: today, last 7 days, last 30 days, total
- **Security**: users see only their own entries, admins see all
- **Daily cron** recomputes time aggregations at 03:00

## CI/CD

GitHub Actions workflows handle the full lifecycle:

| Workflow | Trigger | What it does                                                         |
|----------|---------|----------------------------------------------------------------------|
| `ci.yml` | Push to `18.0-dev` | Lint (`ruff`) + Odoo module tests with PostgreSQL                    |
| `deploy-staging.yml` | Manual | Build/push image, SSH deploy to staging, update module, health check |
| `deploy-prod.yml` | Manual | Build/push image, SSH deploy to prod, update module, health check    |
| `deploy-ansible.yml` | Manual | Run Ansible playbook for server setup (idempotent)                   |

```
Push to 18.0-dev ──► Lint ──► Test ──► (manual) Deploy Staging ──► (manual) Deploy Prod
```

## Infrastructure

### Ansible

Configures the server: sets up directories, deploys backup and replication scripts, installs cron jobs.

```bash
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
```

**Automated backups** run daily at 02:00 — PostgreSQL dump + filestore archive with 7-day retention. A separate replication script clones production data to staging on demand.

### Docker

Multi-stage build pulls [OCA web_dark_mode](https://github.com/OCA/web/tree/18.0/web_dark_mode) at build time and bundles the worklog addon. Production image: `ghcr.io/iwangub/odoo_lab`.


## Commands

```
make up        Start the stack (docker compose up -d)
make down      Stop and remove containers
make build     Rebuild the Odoo image (--no-cache)
make restart   Restart only the Odoo container
make logs      Follow Odoo logs
make shell     Shell inside the Odoo container
make psql      psql inside the database container
make test      Run Odoo module tests (worklog)
```

## Roadmap

- **Terraform** — Hetzner VM provisioning as code (replace manual server setup)
- **Loki + Grafana** — log aggregation and search (Odoo, nginx, Docker)
- **Prometheus + Grafana** — metrics collection (node_exporter, postgres_exporter)
- **Alerting** — Grafana alerts to Slack/Email on downtime or anomalies
- **Security hardening** — sudoers whitelist for deploy user (replace docker group membership)
- **k3s** — lightweight Kubernetes as orchestration layer (stretch goal)
