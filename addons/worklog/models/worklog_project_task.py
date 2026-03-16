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

    @api.model
    def _expand_states(self, values, domain):
        all_states = []
        for key, _ in self._fields['state'].selection:
            all_states.append(key)
        return all_states

