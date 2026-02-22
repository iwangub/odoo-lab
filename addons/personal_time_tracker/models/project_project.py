from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = "project.project"

    personal_time_entry_ids = fields.One2many(
        "personal.time.entry",
        "project_id",
        string="Personal Time Entries",
    )

    total_personal_time = fields.Float(
        string="Total Time (Hours)",
        compute="_compute_total_personal_time",
        store=True,
        digits=(16, 2),
    )

    @api.depends("personal_time_entry_ids.duration_hours")
    def _compute_total_personal_time(self):
        for project in self:
            project.total_personal_time = sum(
                project.personal_time_entry_ids.mapped("duration_hours")
            )
