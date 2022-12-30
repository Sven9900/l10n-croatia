
{
    "name": "Croatia - Fiscalisation",
    "summary": "Croatia Fiscalisation",
    "category": "Croatia",
    "images": [],
    "version": "16.0.0.0.1",
    "application": False,
    "description": """Core placeholder for future module - far away from usability test""",
    'author': "Daj mi 5",
    'website': "",
    "support": "",
    "license": "LGPL-3",
    "depends": [
        "crypto_store",
        "l10n_hr_account_base",
    ],
    "external_dependencies": {
        "python": ['zeep'],
        "bin": []
    },
    "data": [
        'views/account_tax.xml',
        'views/account_journal_views.xml',
        'views/res_company.xml',
        'views/account_move_views.xml',
        'security/ir.model.access.csv',


    ],
    "qweb": [],
    "demo": [],

    "auto_install": False,
    "installable": True,
}
