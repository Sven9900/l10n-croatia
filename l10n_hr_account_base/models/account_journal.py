
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    # original fields modification
    code = fields.Char(size=16)   # DB: default size 5 mi se cini premalecki...

    # new fields needed for localization
    l10n_hr_prostor_id = fields.Many2one(
        comodel_name='l10n.hr.fiskal.prostor',
        string='Business premise',)
    l10n_hr_fiskal_uredjaj_ids = fields.Many2many(
        comodel_name='l10n.hr.fiskal.uredjaj',
        relation='l10n_hr_fiskal_uredjaj_account_journal_rel',
        column1='journal_id', column2='uredjaj_id',
        string='Allowed PoS Devices')

    l10n_hr_default_nacin_placanja = fields.Selection(
        selection=[('T', 'BANK TRANSACTION')],
        string="Default fiskal payment method for this journal",
        default="T")

    def write(self, vals):
        """
        TODO: provjere validnosti
            1 - prostor: izdavanje računa na nivou uređaja:
                - samo jedan dozvoljeni uređaj
            2 - prostor: izdavanje računa na nivou prostora:
                - svi uređaji moraju biti iz istog prostora, i aktivni!
                - provjeri da li ima sequence id, ako nema dodaj!
            3. Sekvenca: Smije imati prefix,
                trenutno jedino podržano od dinamickih: %(year)s i %(y)s
                drugi prefiksi trebaju dopunu

            -> preferirati : Koristi sekvence po razdobljima ali netreba kontrola!
        """

        # if vals.get('l10n_hr_prostor_id') or vals.get('l10n_hr_fiskal_uredjaj_ids'):
        #     self._check_write_vals(vals)
        return super(AccountJournal, self).write(vals)



