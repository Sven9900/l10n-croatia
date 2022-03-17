from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = 'res.partner'

    def get_oib(self):
        self.ensure_one()
        vat = self.vat.upper()  # in case someone entered in owercase?
        res = 'HR' in vat and vat.replace('HR', '') or vat
        return res
