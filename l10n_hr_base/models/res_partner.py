from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = 'res.partner'

    def get_oib(self):
        self.ensure_one()
        if not self.vat:
            # no vat - no error
            return False
        vat = self.vat.upper()  # in case someone entered in lowercase?
        res = 'HR' in vat and vat.replace('HR', '') or vat
        return res
