
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    # original fields modification
    code = fields.Char(size=16)   # DB: default size 5 mi se cini premalecki...

    # new fields needed for localization
    l10n_hr_prostor_id = fields.Many2one(
        comodel_name='l10n.hr.fiskal.prostor',
        string='Prostor',
        help='Business premise')
    l10n_hr_fiskal_uredjaj_ids = fields.Many2many(
        comodel_name='l10n.hr.fiskal.uredjaj',
        relation='l10n_hr_fiskal_uredjaj_account_journal_rel',
        column1='journal_id', column2='uredjaj_id',
        string='Dopusteni naplatni uredjaji')

    l10n_hr_default_nacin_placanja = fields.Selection(
        selection=[('T', 'TRANSAKCIJSKI RAČUN')],
        string="Default fiskal payment method",
        default="T")

    # BOLE: ovo mozda kao config opciju?
    # @api.multi
    # @api.depends('name', 'currency_id', 'company_id',
    #              'company_id.currency_id', 'prostor_id')
    # def name_get(self):
    #     """
    #     dodajem i naziv poslovnog prostora u name get
    #     :return:
    #     """
    #     res = []
    #     for journal in self:
    #         currency = journal.currency_id or journal.company_id.currency_id
    #         name = "%s (%s)" % (journal.name, currency.name)
    #         if journal.prostor_id:
    #             name += " - %s" % journal.prostor_id.oznaka_prostor
    #             uredjaj_sifre = [x.oznaka_uredjaj for x in journal.fiskal_uredjaj_ids
    #                              if journal.fiskal_uredjaj_ids]
    #             if uredjaj_sifre:
    #                 name += " %s" % str(uredjaj_sifre)
    #         res += [(journal.id, name)]
    #     return res


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

        if vals.get('l10n_hr_prostor_id') or vals.get('l10n_hr_fiskal_uredjaj_ids'):
            self._check_write_vals(vals)
        return super(AccountJournal, self).write(vals)

    def _check_write_vals(self, vals):
        prostor_id = vals.get('l10n_hr_prostor_id', False)
        if prostor_id:
            prostor = prostor_id and \
                      self.env['l10n.hr.fiskal.prostor'].browse(prostor_id)
            msg = "Prostor: %s " % prostor.name
            if prostor.sljed_racuna == 'P':
                if not prostor.sequence_id:
                    msg += " - nedostaje fiskalni sljed računa"
                    raise ValidationError(msg)

