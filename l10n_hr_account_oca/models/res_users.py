# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Users(models.Model):
    _inherit = 'res.users'

    l10n_hr_prostor_ids = fields.Many2many(
        comodel_name='l10n.hr.fiskal.prostor',
        relation='l10n_hr_fiskal_prostor_res_users_rel',
        column1='user_id', column2='prostor_id',
        string='Dozvoljeni prostori',
        help="Dozvoljeni prostori za izdavanje računa")
    l10n_hr_default_uredjaj = fields.Many2one(
        comodel_name='l10n.hr.fiskal.uredjaj',
        string='Zadani nap. uređaj',)

    l10n_hr_uredjaj_ids = fields.Many2many(
        comodel_name='l10n.hr.fiskal.uredjaj',
        relation='l10n_hr_fiskal_uredjaj_res_users_rel',
        column1='user_id', column2='uredjaj_id',
        string='Dozvoljeni naplatni uređaji')

    @api.onchange('l10n_hr_default_uredjaj')
    def _onchange_l10n_hr_default_uredjaj(self):
        if self.l10n_hr_default_uredjaj:
            allowed_premises = [p.id for p in self.l10n_hr_prostor_ids]
            if not self.l10n_hr_uredjaj_ids:
                raise UserError(
                    _('You have no allowed devices, '
                      'setting defualt is not possible!'))
            allowed_devices = [d.id for d in self.l10n_hr_uredjaj_ids]
            uredjaj = self.l10n_hr_default_uredjaj.id
            if uredjaj not in allowed_devices:
                raise UserError(
                    _("Selected device '%s' is not in allowed list!" %
                      self.l10n_hr_default_uredjaj.name_get()[0][1]))

    def get_all_uredjaj(self):
        if not self.l10n_hr_prostor_ids:
            self.l10n_hr_uredjaj_ids = [(5)]
            self.l10n_hr_default_uredjaj = False
        else:
            uredjaji = []
            for prostor in self.l10n_hr_prostor_ids:
                for uredjaj in prostor.l10n_hr_uredjaj_ids:
                    uredjaji.append(uredjaj.id)
            if uredjaji:
                self.l10n_hr_uredjaj_ids = [(6, 0, uredjaji)]
                self.l10n_hr_default_uredjaj = uredjaji[0]
