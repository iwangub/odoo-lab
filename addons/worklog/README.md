# Worklog (Odoo 18)

A lightweight module to track how much time you invest in your side projects.

## Features

- **Projects** — Kanban board with four states: Draft, Backlog, Do, Done
- **Tasks** — each project has tasks with a six-state pipeline: Draft → Backlog → Do → Staging → Prod → Done
- **Time entries** — logged per task, with Start / Stop / Continue actions
- **Technologies** — tag tasks with technologies (Python, Docker, ...); see time stats per technology
- **Time stats** — today, last 7 days, last 30 days, and total hours on projects, tasks, and technologies

## Models

| Model | Description |
|---|---|
| `worklog.project` | Project with Kanban state |
| `worklog.project.task` | Task belonging to a project; holds time entries and technology tags |
| `worklog.time.entry` | Individual time entry with start/stop timer |
| `worklog.technology` | Technology tag with aggregated time stats |
| `worklog.time.stats.mixin` | Abstract mixin providing shared time stat fields |

## Installation

1. Place module in your addons path.
2. Update apps list.
3. Install **Worklog**.

CLI example:

```bash
./odoo-bin -d <db_name> -i worklog
```

## Usage

1. Open `Worklog → Projects` and create a project.
2. Open the project and add tasks.
3. From a task, create a time entry and hit `Start`.

## License

LGPL-3
