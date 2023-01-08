import os
import base64
from datetime import datetime
from OpenSSL import crypto as SSLCrypto
from odoo import api, fields, models, _
from odoo.tools import config as odoo_config
from odoo.exceptions import UserError, ValidationError


PROD = {
    'root': 'fina_cert/prod/FinaRootCA.pem',
    'FISKAL 2': 'fina_cert/prod/FinaRDCCA2020.pem',
    'FISKAL 1': 'fina_cert/prod/FinaRDCCA2015.pem',
}
DEMO = {
    'root': 'fina_cert/demo/demo2014_root_ca.pem',
    'FISKAL 2': 'fina_cert/demo/demo2020_sub_ca.pem',
    'FISKAL 1': 'fina_cert/demo/demo2014_sub_ca.pem',
}

class FiskalCertificate(models.Model):
    _name = "l10n.hr.fiskal.certificate"
    _description = "Fiskal certificate store"

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda s: s.env.user.company_id
    )
    # 1. load cert file fields
    cert_file = fields.Binary(string="Received cert file")
    cert_file_name = fields.Char()
    cert_password = fields.Char(string='Password for certificate')
    # the rest of fields filled on conversion
    name = fields.Char(readonly=True)
    cert_type = fields.Selection(
        selection=[
            ('prod', 'Fiskal Prod'),
            ('demo', 'Fiskal Demo'),
            ('other', 'Other/Unknown')
        ], readonly=True
    )
    cert_issuer = fields.Char(readonly=True,)
    cert_subject = fields.Char(readonly=True,)
    cert_oib = fields.Char(readonly=True,)
    pem_key = fields.Text(
        string='Private key', readonly=True,
        help='Private key from user P12/PFX cert file',
    )
    pem_crt = fields.Text(
        string='Certificate', readonly=True,
        help='Fiskal certificate from user P12/PFX cert file',
    )
    fina_certs_data = fields.Text(readonly=True,)
    fina_cert_bundle = fields.Text(
        string="Fina certificates", readonly=True,
        help="Certificate bundle from FINA matching certificate",
    )
    not_before = fields.Datetime(readonly=True)
    not_after = fields.Datetime(readonly=True)

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('convert', 'Converted'),
            ('active', 'Active'),
            ('expired', 'Expired'),
            ('cancel', 'Cancelled'),
        ], readonly=True, default="draft", tracking=1,
    )

    def button_convert_p12(self):
        self.ensure_one()
        if not self.cert_file:
            return False
        _password = self.cert_password or ''
        try:
            p12 = SSLCrypto.load_pkcs12(base64.decodestring(self.cert_file), _password)
        except:
            raise UserError(_('Certificate access error, check password or uploaded file type!'))

        cert = p12.get_certificate()
        issuer = dict(cert.get_issuer().get_components())
        subject = dict(cert.get_subject().get_components())
        name = p12.get_friendlyname().decode('utf-8')
        cert_not_before = cert.get_notBefore().decode('utf-8')
        cert_not_after = cert.get_notAfter().decode('utf-8')
        self.not_before = datetime.strptime(cert_not_before, "%Y%m%d%H%M%SZ")
        self.not_after = datetime.strptime(cert_not_after, "%Y%m%d%H%M%SZ")
        self.cert_issuer = ' | '.join([
            issuer[b'O'].decode('utf-8'),
            issuer.get(b'CN', issuer.get(b'OU', b'')).decode('utf-8')]
        )
        self.cert_subject = ' | '.join([
            subject[b'O'].decode('utf-8'),
            subject[b'CN'].decode('utf-8')]
        )
        self.name = ' | '.join([
            subject[b'CN'].decode('utf-8'),
            issuer.get(b'CN', issuer.get(b'OU', b'')).decode('utf-8'),
            subject[b'O'].decode('utf-8'),
            ]
        )
        self.cert_oib = subject[b'O'].decode('utf-8').split(" ")[-1]
        self.pem_key = SSLCrypto.dump_privatekey(SSLCrypto.FILETYPE_PEM, p12.get_privatekey())
        self.pem_crt = SSLCrypto.dump_certificate(SSLCrypto.FILETYPE_PEM, p12.get_certificate())

        self.state = 'convert'
        self.cert_type = 'demo' if "demo" in self.cert_issuer.lower() else 'prod'
        fiskal_path = self.company_id._get_fiskal_path()
        cert_paths = self.cert_type == 'demo' and DEMO or PROD
        sub_cert = subject.get(b'CN', False)
        sub_cert = sub_cert == b'FISKAL 2' and 'FISKAL 2' or 'FISKAL 1'
        self.fina_certs_data = '\n'.join((cert_paths[sub_cert], cert_paths['root']))
        fina_bundle = ""
        for file in (cert_paths['root'], cert_paths[sub_cert]):
            path = fiskal_path + file
            with open(path, 'r') as rf:
                pem = rf.read()
                fina_bundle += pem
        self.fina_cert_bundle = fina_bundle

    def action_validate(self):
        for cert in self:
            if cert.not_after < fields.Datetime.now():
                cert.state = 'expired'
            else:
                cert.state = 'active'

    def action_cancel(self):
        for cert in self:
            cert.state = 'cancel'


    def unlink(self):
        for cert in self:
            if cert.state == 'active':
                raise UserError(_('Deleting active certificate is not allowed!'))
        return super().unlink()

    def _get_datastore_path(self):
        return odoo_config.filestore(self._cr.dbname)

    def _get_fiskal_cert_path(self):
        fisk_cert_path = os.path.join(
            self._get_datastore_path(), 'l10n_hr')
        if not os.path.exists(fisk_cert_path):
            os.mkdir(fisk_cert_path, 4600)  # setuid,rw, minimal rights applied
        return fisk_cert_path

    def _get_key_cert_file_name(self):
        key = "{0}-{1}-{2}_key.pem".format(
            self.cert_type, self.id, self._cr.dbname)
        crt = "{0}-{1}-{2}_crt.pem".format(
            self.cert_type, self.id, self._cr.dbname)
        fina = "{0}-{1}-{2}_fina.pem".format(
            self.cert_type, self.id, self._cr.dbname)
        return key, crt, fina

    def _disk_check_exist(self, file):
        return os.path.exists(file)

    def _disk_same_content(self, file, content):
        try:
            with open(file, mode="r") as f:
                on_disk = f.read()
                f.close
        except Exception as E:
            on_disk = False
        return not on_disk == content

    def _disk_write_content(self, file, content):
        with open(file, mode="w") as f:
            f.write(content)
            f.flush()

    def get_fiskal_ssl_data(self):
        """
        key and cert are stored on disk because
        ssl and crypto libraries expect them readable on disk or some url.
        so we store both of them in odoo datastore
        :return:
        """
        production = self.cert_type == 'prod'
        f_path = self._get_fiskal_cert_path()
        key, cert, fina = self._get_key_cert_file_name()
        for pem in (key, cert, fina):
            file = os.path.join(f_path, pem)
            if pem.endswith('_fina.pem'):
                content = self.fina_cert_bundle
                fina = file
            elif pem.endswith('_key.pem'):
                content = self.pem_key
                key = file
            else:
                content = self.pem_crt
                cert = file

            if self._disk_check_exist(file) or \
                    self._disk_same_content(file, content):
                self._disk_write_content(file, content)
        return fina, key, cert, production
