# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ["account.move",
                'l10n.hr.fiscal.mixin',
                'l10n.hr.xml.mixin']

    l10n_hr_nacin_placanja = fields.Selection(
        selection_add=[
            ('G', 'Cash (bills and coins)'),
            ('K', 'Credit or debit cards'),
            ('C', 'Bank Cheque'),
            ('O', 'Other payment means')
        ],
    )
    l10n_hr_fiskal_log_ids = fields.One2many(
        comodel_name='l10n.hr.fiskal.log',
        inverse_name='invoice_id',
        string='Fiskal message logs',
        help="Log of all messages sent and received for FINA"
    )



    def button_fiskaliziraj(self):
        self.ensure_one()
        if not self.l10n_hr_jir:
            self.fiskaliziraj()  # from 10n.hr.fixcal.mixin
        # TODO: nova shema ima metodu provjere da li je racun fiskaliziran!
        elif len(self.jir) >= 32:  # BOLE: JIR je 32+ znaka !
            #res = self.fiskaliziraj('provjera') # samo WSDL 1.4 ovog nema u 1.5 ?!
            raise UserError(_('No need to repeat fiscalisation process!'))

    def _l10n_hr_post_out_invoice(self):
        # singleton record! checked in super()
        super()._l10n_hr_post_out_invoice()
        # TODO selection or decision which to send ?
        # - possible not fiscalisation of invoices paid on transaction acc?
        # need to put smart options what and when not to send...
        if self.journal_id.l10n_hr_fiscalisation_active:
            self.fiskaliziraj()
