from odoo import fields, models
from datetime import datetime, timedelta


class WorklogTimeStatsMixin(models.AbstractModel):
    _name = "worklog.time.stats.mixin"
    _description = "Worklog Time Stats Mixin"

    today_hours = fields.Float(
        string="Today (Hours)",
        compute="_compute_today_hours",
        store=True,
        digits=(16, 2)
    )

    last_7_days_hours = fields.Float(
        string="Last 7 Days (Hours)",
        compute="_compute_last_7_days",
        store=True,
        digits=(16, 2)
    )

    last_30_days_hours = fields.Float(
        string="Last 30 Days (Hours)",
        compute="_compute_last_30_days",
        store=True,
        digits=(16, 2)
    )

    total_time_hours = fields.Float(
        string="Total Time (Hours)",
        compute="_compute_total_time_hours",
        store=True,
        digits=(16, 2),
    )

    def _compute_today_hours(self):
        night = datetime.today().replace(hour=3, minute=0, second=0, microsecond=0)
        for record in self:
            record.today_hours = sum(record.task_ids.time_entry_ids
                                     .filtered(lambda f: f.end_time and f.end_time > night)
                                     .mapped('duration_hours'))

    def _compute_last_7_days(self):
        for record in self:
            res = record._compute_days_back_hours(7)
            record.last_7_days_hours = res

    def _compute_last_30_days(self):
        for record in self:
            res = record._compute_days_back_hours(30)
            record.last_30_days_hours = res

    def _compute_days_back_hours(self, days):
        self.ensure_one()
        amount_days_back = datetime.today() - timedelta(days=days)
        time_entries = sum(
            self.task_ids.time_entry_ids
            .filtered(lambda f: f.end_time and f.end_time > amount_days_back)
            .mapped('duration_hours'))
        return time_entries

    def _compute_total_time_hours(self):
        for record in self:
            record.total_time_hours = sum(
                record.task_ids.time_entry_ids.mapped("duration_hours")
            )
