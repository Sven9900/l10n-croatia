from odoo import api, fields, models, _


class FiskalLog(models.Model):
    _name = 'l10n.hr.fiskal.log'
    _description = 'Fiskal messages log'

    name = fields.Char(
        size=64, readonly=True,
        help="Unique communication mark")
    type = fields.Selection(
        selection=[
            ('racun', 'Fiskalizacija racuna'),
            ('rac_pon', 'Ponovljeno slanje racuna'),
            ('rac_prov', 'Provjera fiskalizacije računa'),  # NOVO!
            ('pd', 'Fiskalizacija prateceg dokumenta'),
            ('pd_rac', 'Fiskalizacija računa za prateći dokument'),
            ('echo', 'Test poruka '),
            ('other', 'Other types')],
        string='Message type',
        readonly=True)
    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='Invoice', readonly=True)
    fiskal_prostor_id = fields.Many2one(
        comodel_name='l10n.hr.fiskal.prostor',
        string='Premisse', readonly=True)
    fiskal_uredjaj_id = fields.Many2one(
        comodel_name='l10n.hr.fiskal.uredjaj',
        string='POS Device', readonly=True)
    sadrzaj = fields.Text(string='Sent message', readonly=True)
    odgovor = fields.Text(string='Reply', readonly=True)
    greska = fields.Text(string='Error', readonly=True)
    time_stamp = fields.Char(string='TimeStamp odgovora', readonly=True)
    time_obr = fields.Char(string='Vrijeme obrade', readonly=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Person',
        readonly=True,
        on_delete='restrict')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True)

