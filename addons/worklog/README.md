# Personal Time Tracker (Odoo 18)

A lightweight module to track how much time you invest in your own side projects.

## Why this module

Most time trackers are heavy. This module keeps it simple:
- Create an entry, hit Start/Stop, done.
- See where your time goes across projects.
- Keep data clean with overlap checks and one running timer per user.

## Features

- One-click `Start`, `Stop`, and `Continue` actions.
- Exactly one running timer per user.
- Automatic overlap prevention for time entries.
- Live duration while a timer is running.

## Installation

1. Place module in your addons path.
2. Update apps list.
3. Install **Worklog**.

CLI example:

```bash
./odoo-bin -d <db_name> -i worklog
```

## Usage

1. Open `Worklog -> worklog`.
2. Create a time entry with description + project.
3. Use `Start` and `Stop` in the form header.

## License

LGPL-3
