# -*- coding: utf-8 -*-

from datetime import datetime as dt
from . import poziv_na_broj as pnbr
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class AccountMove(models.Model):
    _inherit = "account.move"

    def getP1_P4data(self, what):
        res = ''
        if what == 'partner_code':
            res = self.partner_id.ref or str(self.partner_id.id)
        elif what == 'partner_id':
            res = str(self.partner_id.id)
        elif what == 'invoice_no':
            res = self.name
        elif what == 'fiskal_no':  # and 'fiskal_separator' in self.comapny_id.fields_get(): ??
            # samo za HR fiskalni broj uz lokalizaciju
            separator = self.company_id.fiskal_separator
            if not self.fiskalni_broj:
                self._set_fiskal_number()
            res = self.fiskalni_broj.split(separator)[0]
        elif what == 'invoice_ym':
            res = dt.strftime(self.invoice_date, "%Y%m")
        elif what == 'invoice_y':
            res = dt.strftime(self.invoice_date, "%Y")
        elif what == 'delivery_ym':
            res = dt.strftime(self.date_delivery, "%Y%m")
        return pnbr.get_only_numeric_chars(res)

    def pnbr_get(self):
        model = self.journal_id.invoice_reference_model

        P1 = self.getP1_P4data(self.journal_id.P1_pnbr or '')
        P2 = self.getP1_P4data(self.journal_id.P2_pnbr or '')
        P3 = self.getP1_P4data(self.journal_id.P3_pnbr or '')
        P4 = self.getP1_P4data(self.journal_id.P4_pnbr or '')

        res = pnbr.reference_number_get(model, P1, P2, P3, P4)

        model = 'HR' + model
        return ' '.join((model, res))

    def _get_invoice_reference_00_hr(self):
        return self.pnbr_get()

    def _get_invoice_reference_01_hr(self):
        return self.pnbr_get()

    def _get_invoice_reference_99_hr(self):
        return self.pnbr_get()

    # def _get_invoice_computed_reference(self):
    #     if self.journal_id.invoice_reference_type == 'hr':
    #         return self.pnbr_get()
    #     return super(AccountMove, self)._get_invoice_computed_reference()
