# -*- encoding: utf-8 -*-

import pytz
from tzlocal import get_localzone
from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class Company(models.Model):
    _inherit = "res.company"

    # Fields, DB: NAMJERNO SU SVI NAZIVI NA HRVATSKOM!

    l10n_hr_nkd_id = fields.Many2one(
        comodel_name='l10n.hr.nkd',
        string="NKD",
        help="Main occupation classified according to NKD-2007")



    @api.onchange('l10n_hr_nkd_id')
    def _onchange_nkd_id(self):
        self.l10n_hr_nkd = self.l10n_hr_nkd_id.code
