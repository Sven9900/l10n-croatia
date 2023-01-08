
{
    "name": "Croatia - Fiskalizacija",
    "summary": "Croatia Fiscalizacija računa",
    "category": "Croatia",
    "images": [],
    "version": "16.0.0.0.2",
    "application": False,
    "author": "Daj mi 5, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-croatia",
    "support": "",
    "license": "AGPL-3",
    "depends": [
        "l10n_hr_account_base",
    ],
    "external_dependencies": {
        "python": ["zeep", "xmlsec"],
        "bin": []
    },
    "data": [
        "views/fiskal_certificate_views.xml",
        "views/account_tax.xml",
        "views/account_journal_views.xml",
        "views/res_company.xml",
        "views/account_move_views.xml",
        "security/ir.model.access.csv",
    ],
    "qweb": [],
    "demo": [],
    "auto_install": False,
    "installable": True,
}
