# -*- coding: utf-8 -*-
{
    "name": """D5 Base usability""",
    "summary": """
    Base usability features by Daj Mi 5
    - menuitems for account chart temlate models
    - add admin user to full accounting features group

    """,
    "category": "Croatia",
    "images": [],
    "version": "16.0.1.0.0",
    "application": False,

    'author': "Davor Bojkić (DAJ MI 5)",
    'website': "",
    "support": "",
    "licence": "LGPL-3",
    #"price" : 20.00,   #-> only if module if sold!
    #"currency": "EUR",

    "depends": [
        "account",
    ],
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    "data": [
        'views/account_views.xml',
        'security/d5_security_mods.xml',
    ],
    "qweb": [],
    "demo": [],

    "auto_install": False,
    "installable": True,
}

