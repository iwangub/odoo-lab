{
    "name": "Personal Time Tracker",
    "version": "18.0.0.1.0",
    "summary": "Lightweight personal project time tracking",
    "description": """
Track personal time spent on projects
    """,
    "author": "Iwan Gubler",
    "license": "LGPL-3",
    "website": "https://github.com",
    "category": "Productivity",
    "depends": [
        "web",
        "project",
    ],
    "data": [
        'data/data.xml',
        "security/personal_time_tracker_security.xml",
        "security/ir.model.access.csv",
        "views/time_entry_menus.xml",
        "views/time_entry_views.xml",
        #"views/project_project_views.xml",
    ],
    "installable": True,
    "application": True,
}
