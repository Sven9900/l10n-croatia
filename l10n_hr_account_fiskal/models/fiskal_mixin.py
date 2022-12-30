from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from ..fiskal import fiskal


class FiscalFiscalMixin(models.AbstractModel):
    """
    Basic fields and methods for all fiscal classes
    - inherit for invoice, sale, procurment etc...
    """
    _name = 'l10n.hr.fiscal.mixin'
    _description = 'Croatia Fiscalisation base mixin'

    l10n_hr_zki = fields.Char(
        string='ZKI',
        readonly=True, copy=False)
    l10n_hr_jir = fields.Char(
        string='JIR',
        readonly=True, copy=False)
    l10n_hr_fiskal_user_id = fields.Many2one(
        comodel_name='res.users', string="Fiscal user",
        help="User who sent the fiscalisation message to FINA. Can be different from responsible person on invoice."
    )

    l10n_hr_vrijeme_xml = fields.Char(  # probably not needed but heck...
        string="XML time",
        help="Value from fiscalization msg stored as string",
        size=19, readonly=True, copy=False)
    l10n_hr_paragon_br = fields.Char(
        'Paragon nr.',
        readonly=True, copy=False,
        states={'draft': [('readonly', False)]},
        # TODO translateME!
        help="Paragon broj racuna, ako je racun izdan na paragon. "
             "Potrebno upisati prije potvrđivanja računa")
    l10n_hr_late_delivery = fields.Boolean(
        string="Late delivery",
        help="Checked if message could not be sent at time of invoicing"
    )

    def _l10n_hr_post_fiskal_check(self):
        """
        Inherit method from l10n_hr_account_base to validate fiscal data
        before posting out invoice in Croatia
        :return: list of errors if found, to be raised together
        """
        res = []
        if self.l10n_hr_nacin_placanja != 'T' and \
            not self.journal_id.l10n_hr_fiscalisation_active:
            res.append(_('Fiscalization is not active for %s!!' % self.journal_id.display_name))
        if self.l10n_hr_nacin_placanja != 'T' and \
            not self.l10n_hr_fiskal_user_id.partner_id.vat:
            res.append(_('User OIB is not not entered! It is required for fiscalisation'))
        if self.l10n_hr_nacin_placanja != 'T' and \
            not self.company_id.fiskal_cert_id:
            res.append(
                _('No fiscal certificate found, please install one '
                  'activate and select it on company setup!'))
        return res

    def _prepare_fisk_racun_taxes(self, racun, factory):
        tax_data = {
            "Pdv": {},
            "Pnp": {},
            "OstaliPor": [],
            "Naknade": [],
        }
        iznos_oslob_pdv, iznos_ne_podl_opor, iznos_marza = 0.00, 0.00, 0.00

        base_lines = self.invoice_line_ids.filtered(lambda line: line.display_type == 'product')
        base_line_values_list = [line._convert_to_tax_base_line_dict() for line in base_lines]

        for line in base_line_values_list:
            for tax in line['taxes']:
                # TODO: taxex with 0 percent have no tax line !!!
                # for now, let's assume we have tax lines with amount zero!
                if not tax.l10n_hr_fiskal_type:
                    raise ValidationError(_("Tax '%s' missing fiskal type!" % tax.name))
                fiskal_type = tax.l10n_hr_fiskal_type
                naziv = tax.name
                stopa = tax.amount  # if amount type == percent??
                osnovica = line['price_subtotal']
                iznos = osnovica * 100 / stopa
                if fiskal_type == 'Pdv':
                    if tax_data['Pdv'].get(stopa):
                        tax_data['Pdv'][stopa]['Osnovica'] += osnovica
                        tax_data['Pdv'][stopa]['Iznos'] += iznos
                    else:
                        tax_data['Pdv'][stopa] = {
                            'Osnovica': osnovica,
                            'Iznos': iznos
                        }
                elif fiskal_type == 'Pnp':
                    if tax_data['Pnp'].get(stopa):
                        tax_data['Pnp'][stopa]['Osnovica'] += osnovica
                        tax_data['Pnp'][stopa]['Iznos'] += iznos
                    else:
                        tax_data['Pnp'][stopa] = {
                            'Osnovica': osnovica,
                            'Iznos': iznos
                        }
                elif fiskal_type == 'OstaliPor':
                    tax_data['OstaliPor'].append({
                        "Naziv": naziv, "Stopa": stopa,
                        "Osnovica": osnovica, "Iznos": iznos})
                elif fiskal_type == 'Naknade':
                    tax_data['Naknade'].append({
                        "NazivN": naziv, "IznosN": iznos})
                elif fiskal_type == 'oslobodenje':
                    iznos_oslob_pdv += osnovica
                elif fiskal_type == 'ne_podlijeze':
                    iznos_ne_podl_opor += osnovica
                elif fiskal_type == 'marza':
                    iznos_marza += osnovica
        f_pdv = []
        for pdv in tax_data['Pdv']:
            _pdv = tax_data['Pdv'][pdv]
            porez = factory.type_factory.PorezType(
                Stopa=fiskal.format_decimal(pdv),
                Osnovica=fiskal.format_decimal(_pdv['Osnovica']),
                Iznos=fiskal.format_decimal(_pdv['Iznos'])
            )
            f_pdv.append(porez)
        if f_pdv:
            racun.Pdv = factory.type_factory.PdvType(Porez=f_pdv)
        f_pnp = []
        # for pnp in tax_data['Pnp']:
        #     _pnp = tax_data['Pnp'][pnp]
        #     porez = factory.type_factory.Porez
        #     porez.Stopa = fiskal.format_decimal(pnp)
        #     porez.Osnovica = fiskal.format_decimal(_pnp['Osnovica'])
        #     porez.Iznos = fiskal.format_decimal(_pnp['Iznos'])
        #     racun.Pnp.Porez.append(porez)
        #
        # for ost in tax_data['OstaliPor']:
        #     _ost = tax_data['OstaliPor'][ost]
        #     porez = factory.type_factory.Porez
        #     porez.Naziv = _ost['Naziv']
        #     porez.Stopa = fiskal.format_decimal(ost)
        #     porez.Osnovica = fiskal.format_decimal(_ost['Osnovica'])
        #     porez.Iznos = fiskal.format_decimal(_pnp['Iznos'])
        #     racun.OstaliPor.Porez.append(porez)
        #
        # if iznos_oslob_pdv:
        #     racun.IznosOslobPdv = fiskal.format_decimal(iznos_oslob_pdv)
        # if iznos_ne_podl_opor:
        #     racun.IznosNePodlOpor = fiskal.format_decimal(iznos_ne_podl_opor)
        # if iznos_marza:
        #     racun.IznosMarza = fiskal.format_decimal(iznos_marza)

        # for nak in tax_data['Naknade']:
        #     naziv, iznos = nak
        #     naknada = factory.type_factory.naknada
        #     naknada.NazivN = naziv
        #     naknada.IznosN = fiskal.format_decimal(iznos)
        #     racun.Naknade.append(naknada)
        return racun

    def _prepare_fisk_racun(self, factory, fiskal_data):
        racun = factory.type_factory.RacunType
        # 1. get company OIB
        #oib =   # pravi OIB -> should be in l10n_hr module !
        racun.Oib = self.company_id.partner_id.company_registry
        nak_dost = self.l10n_hr_late_delivery

        #dat_vrijeme = self.l10n_hr_vrijeme_izdavanja
        # if dat_vrijeme:
        #     dat_vrijeme = dat_vrijeme.replace(' ', 'T')
        #     if dat_vrijeme != fiskal_data['time']['datum_vrijeme']:
        #         # PAŽLJIVO SA OVIM!!! potrebno testirati slučajeve!!!
        #         nak_dost = True
        # else:
        #     self.vrijeme_izdavanja = fiskal_data['time']['datum_racun']
        #     dat_vrijeme = fiskal_data['time']['datum_vrijeme']
        racun.DatVrijeme = fiskal_data['time']['datum_vrijeme']
        racun.OznSlijed = self.l10n_hr_fiskal_uredjaj_id.prostor_id.sljed_racuna

        #br_rac = self.fiskalni_broj.split(self.company_id.fiskal_separator)

        racun.IznosUkupno = fiskal.format_decimal(self.amount_total)
        racun.NacinPlac = self.l10n_hr_nacin_placanja
        racun.OibOper = self.l10n_hr_fiskal_user_id.partner_id.vat
        racun.NakDost = nak_dost
        racun.ZastKod = self.l10n_hr_zki

        if self.l10n_hr_paragon_br:
            racun.ParagonBrRac = str(self.l10n_hr_paragon_br)

        racun.USustPdv = self.company_id.l10n_hr_fiskal_taxative
        racun.BrRac = factory.type_factory.BrojRacunaType(
            BrOznRac=fiskal_data['racun'][0],
            OznPosPr=fiskal_data['racun'][1],
            OznNapUr=fiskal_data['racun'][2]
        )
        if racun.USustPdv:
            # LELLEEE ovo nije dobro..
            # mozda nisam u sustavu pdv-a ali imam naknade ili Pnp???
            # treba razmisliti što ćemo sa ovima koji nisu u sustavu pdv-a!!!
            racun = self._prepare_fisk_racun_taxes(racun, factory)
        return racun

    def _create_fiskal_header(self, factory):
        msg_id  = uuid4()
        dt = datetime.now()
        return self.type_factory.ZaglavljeType(
            IdPoruke=message_id, DatumVrijeme=dt.strftime("%d.%m.%YT%H:%M:%S")
        )

    def fiskaliziraj(self, msg_type='racuni'):
        """
        Fiskalizira jedan izlazni racun ili point of sale račun
        msg_type : Racun,

        """
        if self.l10n_hr_jir and len(self.l10n_hr_jir) > 30:
            # existing in shema 1.4 not in 1.5!
            if msg_type != 'provjera':
                msg_type = 'provjera'
        time_start = self.company_id.get_l10n_hr_time_formatted()
        if not self.l10n_hr_fiskal_user_id:
            # MUST USE CURRENT user for fiscalization!
            # Except in case of paragon račun? or naknadna dostava?
            self.l10n_hr_fiskal_user_id = self._uid
        errors = self._l10n_hr_post_fiskal_check()
        if errors:
            msg = _("Fiscalisation not possible: \n")
            msg += '\n'.join(errors)
            raise ValidationError(msg)

        fiskal_data = self.company_id.get_fiskal_data()
        fiskal_data['time'] = time_start
        fis_racun = self.l10n_hr_fiskalni_broj.split(
            self.company_id.l10n_hr_fiskal_separator)
        assert len(fis_racun) == 3, "Invoice must be assembled using 3 values!"
        fiskal_data['racun'] = fis_racun
        if not self.l10n_hr_zki:
            # ZKI MORA UBJEK OSTATI ISTI
            # generiram ga samo ako još ne postoji
            # OVO je samo za racun, treba posebna metoda za PrateciDokument
            zki_datalist = [
                self.company_id.partner_id.company_registry,
                self.l10n_hr_vrijeme_izdavanja or time_start['datum_racun'],
                fis_racun[0],
                fis_racun[1],
                fis_racun[2],
                fiskal.format_decimal(self.amount_total)
                ]
            self.l10n_hr_zki = fiskal.generate_zki(
                zki_datalist=zki_datalist,
                key_str=self.company_id.l10n_hr_fiskal_cert_id.csr
            )
        fisk = fiskal.Fiskalizacija(fiskal_data=fiskal_data, odoo_object=self)
        if msg_type in ['racuni', 'provjera']:
            racun = self._prepare_fisk_racun(
                factory=fisk, fiskal_data=fiskal_data)
            zaglavlje = self._create_fiskal_header(fisk)

            with fisk.client.settings(raw_response=True):
                response = fisk.client.service.racuni(racun)

        self.company_id.create_fiskal_log(msg_type, fisk, response, time_start)
        if hasattr(response, 'Jir'):
            if not self.jir:
                self.jir = response.Jir
            else:
                pass
