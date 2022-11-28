# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Nkd(models.Model):
    _name = 'l10n.hr.nkd'
    _description = 'HR NKD - national occupational calssification'


    code = fields.Char('Code', size=16, required=True)
    name = fields.Char('Name', required=True)

    def name_get(self):
        res = [((c.id, "%s - %s" % (c.code, c.name))) for c in self]
        return res

