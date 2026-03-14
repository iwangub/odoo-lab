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

    description = fields.Text(
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

    ### w/o MIXIN STARTSECTION

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
    # @api.depends("task_ids.time_entry_ids.duration_hours")
    # def _compute_total_time_hours(self):
    #     for record in self:
    #         record.total_time_hours = sum(
    #             record.task_ids.time_entry_ids.mapped("duration_hours")
    #         )

    ### w/o MIXIN ENDSECTION

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
