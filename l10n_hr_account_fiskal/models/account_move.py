# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"



    l10n_hr_nacin_placanja = fields.Selection(
        selection_add=[
            ('G', 'Cash (bills and coins)'),
            ('K', 'Credit or debit cards'),
            ('C', 'Bank Cheque'),
            ('O', 'Other payment means')
        ],

    )



