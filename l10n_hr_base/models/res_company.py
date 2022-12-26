# -*- encoding: utf-8 -*-

import pytz
from tzlocal import get_localzone
from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Company(models.Model):
    _inherit = "res.company"


    l10n_hr_nkd = fields.Char(
        string="NKD",
        help="Šifra glavne djelatnosti prema NKD-2007"
    )
    l10n_hr_mirovinsko = fields.Char(
        string='Mirovinsko',
        help='Broj obveznika uplaćivanja mirovinskog osiguranja')
    l10n_hr_zdravstveno = fields.Char(
        string='Zdravstveno',
        help='Broj obveze uplaćivanja zdravstvenog osiguranja')
    l10n_hr_maticni_broj = fields.Char(string='Matični broj')



    def get_l10n_hr_time_formatted(self):
        # odoo16 - date/time) fields are WITH TZ info! diff from previous versions!

        user_tz = self.env.user.tz or self.env.context.get('tz')
        user_pytz = pytz.timezone(user_tz) if user_tz else pytz.utc
        tstamp = datetime.now().astimezone(user_pytz)
        time_now = tstamp.replace(tzinfo=None)
        return {
            'datum': tstamp.strftime('%d.%m.%Y'),                   # datum_regular SAD
            'datum_vrijeme': tstamp.strftime('%d.%m.%YT%H:%M:%S'),  # format za zaglavlje FISKAL XML poruke
            'datum_meta': tstamp.strftime('%Y-%m-%dT%H:%M:%S'),     # format za metapodatke xml-a ( JOPPD...)
            'datum_racun': tstamp.strftime('%d.%m.%Y %H:%M'),    # format za ispis na računu
            'time_stamp': tstamp,                                   # timestamp, za zapis i izračun vremena obrade
            'odoo_datetime': time_now.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        }

