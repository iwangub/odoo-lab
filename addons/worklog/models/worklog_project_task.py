from odoo import api, fields, models
from datetime import datetime, timedelta


class WorklogProjectTask(models.Model):
    _name = "worklog.project.task"
    _description = "Worklog Project Task"
    _order = "state"
    _inherit = ['worklog.time.stats.mixin']

    name = fields.Char(
        string="Task",
        required=True,
    )

    sequence = fields.Integer(
        default=10,
    )

    project_id = fields.Many2one(
        comodel_name="worklog.project",
        string="Project",
        required=True,
        ondelete="cascade",
    )

    time_entry_ids = fields.One2many(
        string="Time Entries",
        comodel_name="worklog.time.entry",
        inverse_name="task_id"
    )

    technology_ids = fields.Many2many(
        comodel_name="worklog.technology",
        string="Technologies",
    )

    state = fields.Selection([
        ('1_draft', 'Draft'),
        ('2_backlog', 'Backlog'),
        ('3_do', 'Do'),
        ('4_staging', 'Staging'),
        ('5_prod', 'Prod'),
        ('6_done', 'Done'),
    ],
        string='Status',
        default="1_draft",
        required=True,
        group_expand='_expand_states',
    )

    notes = fields.Char(
        string="Notes"
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
    #     compute="_compute_total_time_hours",
    #     store=True,
    #     digits=(16, 2),
    # )
    #
    # def _compute_today_hours(self):
    #     night = datetime.today().replace(hour=3, minute=0, second=0, microsecond=0)
    #     for record in self:
    #         record.today_hours = sum(record.time_entry_ids
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
    #
    # def _compute_days_back_hours(self, days):
    #     self.ensure_one()
    #     amount_days_back = datetime.today() - timedelta(days=days)
    #     time_entries = sum(
    #         self.time_entry_ids
    #         .filtered(lambda f: f.end_time > amount_days_back)
    #         .mapped('duration_hours'))
    #     return time_entries
    #
    #
    # @api.depends('time_entry_ids')
    # def _compute_total_time_hours(self):
    #     for record in self:
    #         total_hours = sum(record.time_entry_ids.mapped('duration_hours'))
    #         record.total_time_hours = total_hours if total_hours else 0.0

    ### w/o MIXIN ENDSECTION

    ### with MIXIN STARTSECTION

    @api.depends("time_entry_ids.duration_hours")
    def _compute_today_hours(self):
        night = datetime.today().replace(hour=3, minute=0, second=0, microsecond=0)
        for record in self:
            record.today_hours = sum(record.time_entry_ids
                                     .filtered(lambda f: f.end_time and f.end_time > night)
                                     .mapped('duration_hours'))

    @api.depends("time_entry_ids.duration_hours")
    def _compute_last_7_days(self):
        return super()._compute_last_7_days()

    @api.depends("time_entry_ids.duration_hours")
    def _compute_last_30_days(self):
        super()._compute_last_30_days()

    def _compute_days_back_hours(self, days):
        self.ensure_one()
        amount_days_back = datetime.today() - timedelta(days=days)
        time_entries = sum(
            self.time_entry_ids
            .filtered(lambda f: f.end_time and f.end_time > amount_days_back)
            .mapped('duration_hours'))
        return time_entries

    @api.depends("time_entry_ids.duration_hours")
    def _compute_total_time_hours(self):
        for record in self:
            record.total_time_hours = sum(
                record.time_entry_ids.mapped("duration_hours")
            )

    ### with MIXIN ENDSECTION

    @api.model
    def _expand_states(self, values, domain):
        all_states = []
        for key, _ in self._fields['state'].selection:
            all_states.append(key)
        return all_states
    # return [key for key, _ in self._fields['state'].selection]

    # state_order = fields.Integer(
    #     compute="_compute_state_order",
    #     store=True,
    # )

    # @api.depends("state")
    # def _compute_state_order(self):
    #     for record in self:
    #         states = {
    #             "backlog": 1,
    #             "do": 2,
    #             "staging": 3,
    #             "prod": 4,
    #             "done": 5,
    #         }
    #         record.state_order = states[record.state]
