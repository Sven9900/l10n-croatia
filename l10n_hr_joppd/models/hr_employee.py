from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    l10n_hr_oib = fields.Char(
        string="OIB",
        related="address_home_id.company_registry",
    )
    l10n_hr_joppd_b2_id = fields.Many2one(
        string="Šifra prebivališta/boravišta",
        comodel_name="l10n.hr.joppd.codebook",
        domain=[("usage", "in", ["city", "country"])],
    )
    l10n_hr_joppd_b3_id = fields.Many2one(
        string="Šifra mjesta rada",
        comodel_name="l10n.hr.joppd.codebook",
        domain=[("usage", "in", ["city", "country"])],
    )
