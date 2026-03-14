from odoo import fields, models, api
from datetime import datetime, timedelta


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

    ### w/o MIXIN STARTSECTION

    #
    # today_hours = fields.Float(
    #     string="Today (Hours)",
    #     compute="_compute_today_hours",
    #     # store=True, # TODO: enable store True when done
    #     digits=(16, 2)
    # )
    #
    # last_7_days_hours = fields.Float(
    #     string="Last 7 Days (Hours)",
    #     compute="_compute_last_7_days",
    #     # store=True, # TODO: enable store True when done
    #     digits=(16, 2)
    # )
    #
    # last_30_days_hours = fields.Float(
    #     string="Last 30 Days (Hours)",
    #     compute="_compute_last_30_days",
    #     # store=True, # TODO: enable store True when done
    #     digits=(16, 2)
    # )
    #
    # total_time_hours = fields.Float(
    #     string="Total Time (Hours)",
    #     compute="_compute_total_hours",
    #     store=True,
    #     digits=(16, 2),
    # )
    #
    # def _compute_today_hours(self): # same
    #     night = datetime.today().replace(hour=3, minute=0, second=0, microsecond=0)
    #     for record in self:
    #         record.today_hours = sum(record.task_ids.time_entry_ids
    #                                  .filtered(lambda f: f.end_time > night)
    #                                  .mapped('duration_hours'))
    #
    # #    @api.depends("task_ids.time_entry_ids.duration_hours")
    # def _compute_last_7_days(self):
    #     for record in self:
    #         res = record._compute_days_back_hours(7)
    #         record.last_7_days_hours = res
    #
    # #    @api.depends("task_ids.time_entry_ids.duration_hours")
    # def _compute_last_30_days(self):
    #     for record in self:
    #         res = record._compute_days_back_hours(30)
    #         record.last_30_days_hours = res
    #
    # def _compute_days_back_hours(self, days):
    #     self.ensure_one()
    #     amount_days_back = datetime.today() - timedelta(days=days)
    #     time_entries = sum(
    #         self.task_ids.time_entry_ids
    #         .filtered(lambda f: f.end_time > amount_days_back)
    #         .mapped('duration_hours'))
    #     return time_entries
    #
    # @api.depends('task_ids.time_entry_ids.duration_hours')
    # def _compute_total_hours(self):
    #     for record in self:
    #         res = record.task_ids.time_entry_ids.mapped("duration_hours")
    #         record.total_time_hours = sum(res) if res else 0.0

    ### w/o MIXIN ENDSECTIONS

    ### with MIXIN STARTSECTION

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

    ### with MIXIN ENDSECTION
