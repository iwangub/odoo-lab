from odoo import fields, models


class WorklogTag(models.Model):
    _name = "worklog.tag"
    _description = "Worklog Tag"
    _order = "name"

    name = fields.Char(
        string="Tag",
        required=True,
    )

    color = fields.Integer(
        string="Color",
        default=0,
    )
