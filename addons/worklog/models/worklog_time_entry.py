from odoo import api, fields, models
from odoo.exceptions import ValidationError


class WorklogTimeEntry(models.Model):
    _name = "worklog.time.entry"
    _description = "Worklog Time Entry"
    _order = "start_time desc"

    name = fields.Char(
        string="Description",
        required=True,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user,
        required=True,
    )

    project_id = fields.Many2one(
        comodel_name="worklog.project",
        string="Project",
        required=True,
    )

    technology_ids = fields.Many2many(
        comodel_name="worklog.technology",
        string="Technology",
    )

    start_time = fields.Datetime(
        string="Start Time",
        required=True,
        default=fields.Datetime.now,
    )

    end_time = fields.Datetime(
        string="End Time",
    )

    duration_hours = fields.Float(
        string="Duration (Hours)",
        compute="_compute_duration",
        store=True,
        digits=(16, 2),
    )

    live_duration_hours = fields.Float(
        string="Live Duration (Hours)",
        compute="_compute_live_duration",
        digits=(16, 2),
    )

    is_running = fields.Boolean(
        string="Running",
        default=False,
    )

    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                delta = record.end_time - record.start_time
                record.duration_hours = delta.total_seconds() / 3600.0
            else:
                record.duration_hours = 0.0

    @api.depends("start_time", "end_time", "is_running")
    def _compute_live_duration(self):
        now = fields.Datetime.now()
        for record in self:
            if not record.start_time:
                record.live_duration_hours = 0.0
                continue
            end_time = now if record.is_running or not record.end_time else record.end_time
            record.live_duration_hours = max((end_time - record.start_time).total_seconds(), 0) / 3600.0

    @api.constrains("start_time", "end_time")
    def _check_time_order(self):
        for record in self:
            if record.start_time and record.end_time and record.end_time < record.start_time:
                raise ValidationError("End Time must be after Start Time.")

    @api.constrains("user_id", "is_running")
    def _check_single_running_entry(self):
        for record in self.filtered("is_running"):
            running_count = self.search_count([
                ("id", "!=", record.id),
                ("user_id", "=", record.user_id.id),
                ("is_running", "=", True),
            ])
            if running_count:
                raise ValidationError("Only one running timer per user is allowed.")

    @api.constrains("user_id", "start_time", "end_time", "is_running")
    def _check_no_overlap(self):
        now = fields.Datetime.now()
        for record in self:
            if not record.user_id or not record.start_time:
                continue

            record_end = record.end_time or now
            # TODO: optimize
            overlaps = self.search([
                ("id", "!=", record.id),
                ("user_id", "=", record.user_id.id),
                ("start_time", "!=", False),
            ])
            for other in overlaps:
                other_end = other.end_time or now
                if other.start_time < record_end and record.start_time < other_end:
                    raise ValidationError(
                        "Time entries for the same user cannot overlap."
                    )

    @api.constrains("is_running", "end_time")
    def _check_running_end_time_consistency(self):
        for record in self:
            if record.is_running and record.end_time:
                raise ValidationError("Running entries cannot have an End Time.")

    def _stop_other_running_entries(self):
        for record in self:
            running_entries = self.search([
                ("user_id", "=", record.user_id.id),
                ("is_running", "=", True),
                ("id", "!=", record.id),
            ])
            if running_entries:
                running_entries.write({
                    "end_time": fields.Datetime.now(),
                    "is_running": False,
                })

    def action_start(self):
        now = fields.Datetime.now()
        for record in self:
            record._stop_other_running_entries()
            record.write({
                "start_time": now,
                "end_time": False,
                "is_running": True,
            })

    def action_stop(self):
        now = fields.Datetime.now()
        for record in self:
            if record.is_running:
                record.write({
                    "end_time": now,
                    "is_running": False,
                })

    def action_continue(self):
        self.ensure_one()
        self._stop_other_running_entries()

        new_entry = self.create({
            "name": self.name,
            "user_id": self.env.user.id,
            "project_id": self.project_id.id,
            "start_time": fields.Datetime.now(),
            "is_running": True,
        })

        return {
            "type": "ir.actions.act_window",
            "name": "Worklog Time Entry",
            "res_model": "worklog.time.entry",
            "view_mode": "form",
            "res_id": new_entry.id,
            "target": "current",
        }
