{
    "name": """Croatia - JOPPD report""",
    "summary": """JOPPD report base""",
    "category": "Croatia",
    "images": [],
    "version": "16.0.0.1.0",
    "application": False,
    "author": "Dajmi5",
    "website": "",
    "support": "",
    "licence": "LGPL-3",
    "depends": [
        "hr",
        "l10n_hr_base",
        # "base_address_extended",  # Zbog kucnog broja i slova u adresama!
    ],
    "data": [
        "security/joppd_security.xml",
        "security/ir.model.access.csv",
        "data/l10n.hr.joppd.codebook.csv",
        "views/joppd_views.xml",
        "views/joppd_codebook_views.xml",
        "views/hr_employee_views.xml",
        "views/joppd_menuitems.xml",
    ],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": True,
}
