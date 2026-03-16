from odoo import fields, models, api


class WorklogTechnology(models.Model):
    _name = "worklog.technology"
    _description = "Worklog technology"
    _order = "name"
    _inherit = ['worklog.time.stats.mixin']

    name = fields.Char(
        string="Technology",
        required=True,
    )

    description = fields.Char(
        string="Description"
    )

    task_ids = fields.Many2many(
        comodel_name="worklog.project.task",
        string="Time Entries from Task",
        ondelete="cascade",
    )

    @api.depends("task_ids.time_entry_ids.duration_hours")
    def _compute_today_hours(self):
        return super()._compute_today_hours()

    @api.depends("task_ids.time_entry_ids.duration_hours")
    def _compute_last_7_days(self):
        return super()._compute_last_7_days()

    @api.depends("task_ids.time_entry_ids.duration_hours")
    def _compute_last_30_days(self):
        super()._compute_last_30_days()

    @api.depends("task_ids.time_entry_ids.duration_hours")
    def _compute_total_time_hours(self):
        return super()._compute_total_time_hours()
