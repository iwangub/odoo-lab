from odoo import fields, models, api


class WorklogTechnology(models.Model):
    _name = "worklog.technology"
    _description = "Worklog technology"
    _order = "name"

    name = fields.Char(
        string="Technology",
        required=True,
    )

    entry_ids = fields.Many2many(
        comodel_name="worklog.time.entry",
        string="Time Entries",
    )

    description = fields.Char(
        string="Description"
    )

    invested_time_total_hours = fields.Float(
        string="Invested Time",
        compute="_compute_total_hours",
        store=True,
        digits=(16, 2),
    )

    # TODO: add type
    # TODO: add invested_time_last_7/30_days

    @api.depends('entry_ids.duration_hours')
    def _compute_total_hours(self):
        for rec in self:
            res = rec.entry_ids.mapped("duration_hours")
            rec.invested_time_total_hours = sum(res) if res else None
