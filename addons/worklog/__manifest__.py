{
    "name": "Worklog",
    "version": "18.0.0.3.0",
    "summary": "Track time spent on projects and technologies",
    "description": """
                   Track time spent on personal and professional projects.
                   Log entries per task and tag them by technology (Python, Docker, CI/CD, ...).
                       """,
    "author": "Iwan Gubler",
    "license": "LGPL-3",
    "website": "https://github.com/iwangub/odoo-lab",
    "category": "Productivity",
    "depends": [
        "web",
    ],
    "data": [
        "data/data.xml",
        "data/technology_data.xml",
        "security/worklog_security.xml",
        "security/ir.model.access.csv",
        "views/worklog_project_views.xml",
        "views/worklog_time_entry_views.xml",
        "views/worklog_technology_views.xml",
        "views/worklog_project_task_views.xml",
        "views/worklog_menus.xml",
    ],
    "installable": True,
    "application": True,
}
