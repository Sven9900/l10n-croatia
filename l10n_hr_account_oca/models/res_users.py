# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Users(models.Model):
    _inherit = 'res.users'

    prostor_ids = fields.Many2many(
        comodel_name='fiskal.prostor',
        relation='fiskal_prostor_res_users_rel',
        column1='user_id', column2='prostor_id',
        string='Dozvoljeni prostori',
        help="Dozvoljeni prostori za izdavanje računa")
    default_uredjaj = fields.Many2one(
        comodel_name='fiskal.uredjaj',
        string='Zadani nap. uređaj',)

    uredjaj_ids = fields.Many2many(
        comodel_name='fiskal.uredjaj',
        relation='fiskal_uredjaj_res_users_rel',
        column1='user_id', column2='uredjaj_id',
        string='Dozvoljeni naplatni uređaji')

    @api.onchange('default_uredjaj')
    def _onchange_default_uredjaj(self):
        if self.default_uredjaj:
            allowed_premises = [p.id for p in self.prostor_ids]
            if not self.uredjaj_ids:
                raise UserError(
                    _('You have no allowed devices, '
                      'setting defualt is not possible!'))
            allowed_devices = [d.id for d in self.uredjaj_ids]
            uredjaj = self.default_uredjaj.id
            if uredjaj not in allowed_devices:
                raise UserError(
                    _("Selected device '%s' is not in allowed list!" %
                      self.default_uredjaj.name_get()[0][1]))

    def get_all_uredjaj(self):
        if not self.prostor_ids:
            self.uredjaj_ids = [(5)]
            self.default_uredjaj = False
        else:
            uredjaji = []
            for prostor in self.prostor_ids:
                for uredjaj in prostor.uredjaj_ids:
                    uredjaji.append(uredjaj.id)
            if uredjaji:
                self.uredjaj_ids = [(6, 0, uredjaji)]
                self.default_uredjaj = uredjaji[0]
