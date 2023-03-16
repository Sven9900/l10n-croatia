from odoo import fields, models


class JoppdCodebook(models.Model):
    _name = "l10n.hr.joppd.codebook"
    _description = "JOPPD Codebook"

    code = fields.Char(required=True)
    name = fields.Char(required=True)
    usage = fields.Char(required=True)
    date_start = fields.Date()
    date_end = fields.Date()
    sequence = fields.Integer()
    period_year = fields.Boolean("Period year")

    def name_get(self):
        res = [(l.id, " - ".join((l.code, l.name)) if l.code else l.name) for l in self]
        return res
