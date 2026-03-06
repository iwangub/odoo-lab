from odoo import fields, models


class WorklogTechnology(models.Model):
    _name = "worklog.technology"
    _description = "Worklog technology"
    _order = "name"

    name = fields.Char(
        string="technology",
        required=True,
    )

    color = fields.Integer(
        string="Color",
        default=0,
    )
