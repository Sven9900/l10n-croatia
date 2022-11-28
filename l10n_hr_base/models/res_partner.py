from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = 'res.partner'


    # l10n_hr - def _compute_company_registry(self):
    # def get_oib(self):
    #     self.ensure_one()
    #     if not self.vat:
    #         # no vat - no error
    #         return False
    #     vat = self.vat.upper()  # in case someone entered in lowercase?
    #     res = 'HR' in vat and vat.replace('HR', '') or vat
    #     return res
