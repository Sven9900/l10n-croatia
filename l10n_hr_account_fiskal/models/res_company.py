# Copyright 2020 Decodio Applications Ltd (https://decod.io)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import os
from lxml import etree
from ..fiskal import fiskal
from odoo import api, fields, models, _
from odoo.exceptions import MissingError, ValidationError


SCHEMA_HELP = """
verzija: 1.3 Datum verzije: 04.07.2016.
- u WSDL-u dodana nova metoda "provjera"
- u schemi dodani novi elementi "ProvjeraZahtjev" i "ProvjeraOdgovor"

verzija: 1.4 Datum verzije: 27.04.2017.
- u WSDL-u izbačena metoda "poslovniProstor"
-u schemi izbačeni elementi "PoslovniProstorZahtjev",
   "PoslovniProstorOdgovor"i ostalo vezano za prijavu poslovnih prostora

verzija: 1.5 Datum verzije: 20.12.2019.
- u WSDL-u dodane dvije metode "prateciDokumenti" i "racuniPD"
- u schemi dodani elementi "PrateciDokumentiZahtjev",
   "PrateciDokumentiOdgovor", "RacunPDZahtjev",
   "RacunPDOdgovor" i ostalo vezano za nove elemente.

"""


class Company(models.Model):
    _inherit = "res.company"

    @staticmethod
    def _get_fiskal_path(sub=None):
        """
        :param sub: additional sub path needed as a string
           - fina_cert/demo
           - fina_cert/prod
        :return:
        """
        file_path = os.path.dirname(os.path.realpath(__file__))
        fiskal_path = file_path.replace("models", "fiskal/")
        return fiskal_path

    @api.model
    def _get_schema_selection(self):
        fiskal_path = self._get_fiskal_path()
        fiskal_path += "schema"
        res = [(s, s) for s in os.listdir(fiskal_path)]
        return res


    l10n_hr_fiskal_cert_id = fields.Many2one(
        comodel_name="l10n.hr.fiskal.certificate",
        string="Fiscal certificate", tracking=1,
        domain="[("state", "=", "active")]",
        help="Officialy issued by Croatian FINA Agency, imported and activated"
    )
    l10n_hr_fiskal_spec = fields.Char(
        string="Special", size=1000,
        help="OIB informatičke tvrtke koja održava software, "
             "za demo cert mora odgovarati OIBu sa demo certifikata",
        )
    l10n_hr_fiskal_schema = fields.Selection(
        selection=_get_schema_selection,
        string="Fiskalizaction schema",
        help=SCHEMA_HELP
    )
    l10n_hr_fiskal_taxative = fields.Boolean(
        string="In taxation system", default=True, tracking=1
    )

    def _get_log_vals(self, msg_type, msg_obj, response, time_start, origin):
        """
        Inherit in other modules with proper super to add values
        """
        time_stop = self.get_l10n_hr_time_formatted()
        t_obrada = time_stop["time_stamp"] - time_start["time_stamp"]
        time_obr = "%s.%s s" % (t_obrada.seconds, t_obrada.microseconds)
        error_log = ""
        if hasattr(response, "Greske") and response.Greske is not None:
            error_log = "\n".join(
                [" - ".join(
                    [item.SifraGreske,item.PorukaGreske.replace("\t", "").replace("\n", "")]
                    ) for item in response.Greske.Greska]
            )
        if msg_type == "racuni"and origin.l10n_hr_late_delivery:
            msg_type = "rac_pon"

        values = {
            "user_id": self.env.user.id,
            "name": msg_type != "echo" and
                    response.Zaglavlje.IdPoruke or "ECHO",
            "type": msg_type,
            "time_stamp": msg_type != "echo" and
                          response.Zaglavlje.DatumVrijeme or
                          time_stop["datum_vrijeme"],
            "time_obr": time_obr,
            "sadrzaj": etree.tostring(msg_obj.history.last_sent["envelope"]).decode("utf-8"),
            "odgovor": etree.tostring(msg_obj.history.last_sent["envelope"]).decode("utf-8"),
            "greska": error_log != "" and error_log  or "OK",
            "fiskal_prostor_id": origin._name == "account.move"
                     and origin.l10n_hr_fiskal_uredjaj_id.prostor_id.id or False,
            "fiskal_uredjaj_id": origin._name == "account.move"
                     and origin.l10n_hr_fiskal_uredjaj_id.id or False,
            "invoice_id": origin._name == "account.move" and origin.id or False,
            "company_id": self.id
        }
        return values

    def create_fiskal_log(self, msg_type, msg_obj, response, time_start, origin):
        """
        borrow and SMOP rewrite from decodio
        """
        log_vals = self._get_log_vals(msg_type, msg_obj, response, time_start, origin)
        self.env["l10n.hr.fiskal.log"].create(log_vals)

    def button_test_echo(self):
        fd = self.get_fiskal_data()
        fisk = fiskal.Fiskalizacija(fiskal_data=fd)
        time_start = self.get_l10n_hr_time_formatted()
        msg = "TEST message"
        echo = fisk.test_service(msg)
        self.create_fiskal_log("echo", fisk, echo, time_start)

    def get_fiskal_data(self):
        fina_cert = self.l10n_hr_fiskal_cert_id
        if not fina_cert:
            raise MissingError(_("Fiskal Cerificate not found! Check company setup!"))
        fina_pem, key_file, cert_file, production = fina_cert.get_fiskal_ssl_data()

        fiskal_path = self._get_fiskal_path()
        schema = "file://" + fiskal_path + "schema/" + self.l10n_hr_fiskal_schema
        wsdl_file = schema + "/wsdl/FiskalizacijaService.wsdl"

        ca_path, cis_ca_list = None, []
        cert_path = fiskal_path + "/fina_cert/" + self.l10n_hr_fiskal_cert_id.cert_type
        for fcert in os.listdir(cert_path):
            fpath = os.path.join(cert_path, fcert)
            cis_ca_list.append(fpath)
        res = {
            "company_oib": self.vat,
            "cert_oib": self.l10n_hr_fiskal_cert_id.cert_oib,
            "wsdl": wsdl_file,
            "key": key_file,
            "cert": cert_file,
            "fina": fina_pem,
            "ca_list": cis_ca_list,
            "ca_path": ca_path,
            "url": "fiskalcis" if production else "fiskalcistest",
            "demo": not production,
        }
        return res


class FiskalProstor(models.Model):
    _inherit = "l10n.hr.fiskal.prostor"

    fiskal_log_ids = fields.One2many(
        comodel_name="l10n.hr.fiskal.log",
        inverse_name="fiskal_prostor_id",
        string="Logovi poruka",
        help="Logovi poslanih poruka prema poreznoj upravi",
    )




