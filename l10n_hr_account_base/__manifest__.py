
{
    "name": "Croatia - Accounting base",
    "summary": "Croatia accounting localisation",
    "category": "Accounting/Localizations/Croatia",
    "images": [],
    "version": "16.0.0.0.1",
    "application": False,

    'author': "Daj Mi 5",
    'website': "",
    "support": "",
    "license": "LGPL-3",
    "depends": [
        "account",
        "base_vat",
        "base_iban",
        "l10n_hr",
        "l10n_hr_base",
    ],
    "excludes": [],
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    "data": [
        "security/ir.model.access.csv",
        "views/res_company_view.xml",
        "views/account_move_view.xml",
        "views/account_journal_view.xml",
        "views/menuitems.xml",
    ],
    "qweb": [],
    "demo": [],

    "auto_install": False,
    "installable": True,
}
