
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"
    l10n_hr_default_nacin_placanja = fields.Selection(
        selection_add=[
            ('G', 'Cash (bills and coins)'),
            ('K', 'Credit or debit cards'),
            ('C', 'Bank Cheque'),
            ('O', 'Other payment means')
        ],
        )




