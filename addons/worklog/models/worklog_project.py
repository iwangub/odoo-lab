from odoo import api, fields, models


class WorklogProject(models.Model):
    _name = "worklog.project"
    _description = "Worklog Project"
    _order = "name"

    name = fields.Char(
        string="Project",
        required=True,
    )

    description = fields.Text(
        string="Description",
    )

    entry_ids = fields.One2many(
        comodel_name="worklog.time.entry",
        inverse_name="project_id",
        string="Entries",
    )

    total_time_hours = fields.Float(
        string="Total Time (Hours)",
        compute="_compute_total_time_hours",
        store=True,
        digits=(16, 2),
    )

    @api.depends("entry_ids.duration_hours")
    def _compute_total_time_hours(self):
        for project in self:
            project.total_time_hours = sum(
                project.entry_ids.mapped("duration_hours")
            )
