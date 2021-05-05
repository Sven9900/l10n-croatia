# -*- coding: utf-8 -*-
{
    "name": "Croatia COA - RRIF 2015",
    "summary": "Croatia COA template - RRIF2015",
    "category": "Accounting/Localizations/Account Charts",
    "images": [],
    "version": "14.0.1.0.0",
    "application": False,

    "author": "DAJ MI 5,"
              "Odoo Croatian Community",
    # "support": "support@odoo-hrvatska.org",
    # "website": "http://odoo-hrvatska.org",
    "licence": "LGPL-3",
    "depends": [
        "account",
        "base_vat",
        "base_iban",
        # TESTNO
        #"account_invoice_tax_note", # from OCA! - oslobodjenja!

    ],
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    "data": [
        "data/l10n_hr_chart_data.xml",         # DB: template id = l10n_hr_coa_rrif_2015_template
        "data/res_county_group.xml",           # Dodajem EU države bez HR

        "data/account.account.type.csv",       # Tipovi konta, reducirano za dodane u standardnom odoo
        "data/account.account.template.csv",   # konta
        "data/account_chart_tag_data.xml",     # posatvlja defaulte na kontni plan
        "data/account.group.template.csv",     # 16.1.2020: koristim account grupe za sintetiku!

        "data/account.tax.group.csv",
        "data/account_tax_report_data.xml",   # dodan group_id
        "data/account_tax_template_data.xml",

        "data/account.fiscal.position.template.csv",
        "data/account.fiscal.position.tax.template.csv", # TODO: PPO, Neoporezivi, bez sjedista
        "data/account.fiscal.position.account.template.csv",

        'data/account_chart_template_load.xml'
    ],
    "qweb": [],
    "demo": [],

    "auto_install": False,
    "installable": True,
    #"post_init_hook": '_install_l10n_hr_modules',
}


