from odoo import api, fields, models


class WorklogProject(models.Model):
    _name = "worklog.project"
    _description = "Worklog Project"
    _order = "name"
    _inherit = ['worklog.time.stats.mixin']

    name = fields.Char(
        string="Project",
        required=True,
    )

    state = fields.Selection([
        ('1_draft', 'Draft'),
        ('2_backlog', 'Backlog'),
        ('3_do', 'Do'),
        ('4_done', 'Done'),
    ],
        string='Status',
        default="1_draft",
        required=True,
        group_expand='_expand_states',
    )

    description = fields.Html(
        string="Description",
    )

    task_count = fields.Integer(
        string="Tasks",
        compute="_compute_task_count",
    )

    task_ids = fields.One2many(
        comodel_name="worklog.project.task",
        inverse_name="project_id",
        string="Task Entries",
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

    @api.model
    def _expand_states(self, values, domain):
        all_states = []
        for key, _ in self._fields['state'].selection:
            all_states.append(key)
        return all_states

    def action_open_tasks(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'res_model': 'worklog.project.task',
            'view_mode': 'kanban,list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    @api.depends("task_ids")
    def _compute_task_count(self):
        for record in self:
            record.task_count = len(record.task_ids)
