# -*- coding: utf-8 -*-
{
    "name": """Croatia - City data""",
    "summary": """Adds location data for Croatia - Cities, post offices etc.""",
    "category": "Croatia",
    "images": [],
    "version": "16.0.1.0.0",
    "application": False,

    'author': "Odoo Community Association (OCA)"
              ", Decodio Applications d.o.o."
              ", Davor Bojkić (DAJ MI 5)",
    'website': "",
    "support": "",
    "licence": "LGPL-3",
    #"price" : 20.00,   #-> only if module if sold!
    #"currency": "EUR",

    "depends": [
        "base_address_extended",
    ],
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    "data": [
        "data/res_country_state_data.xml",
        "data/res.city.csv",
    ],
    "qweb": [],
    "demo": [],

    "auto_install": False,
    "installable": True,
}

