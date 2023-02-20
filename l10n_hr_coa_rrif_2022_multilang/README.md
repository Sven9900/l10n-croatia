# RRIF 2021 Chart of accounts - Multilang

Odoo has recently updated Croatian localisation module l10n_hr, and added a new one:
l10n_hr_eur, both depending on l10n_multilang Main CoA module _l10n_hr_coa_rrif_2022_ is
reverted not to depend on l10n_multilang module because of odoo16 issue with multi lang
: https://github.com/odoo/odoo/issues/107599

So this module provides a bridge for those who needs multilang CoA, depending on bot:
CoA module and l10n_multilang, and containing translations terms for original CoA
module, to be loaded and updated.

Be aware of possible problems with disaapearing translations after upgrades of account
module. Most dangerous affect is to possibly modified account names from template CoA

Adding translations for xx_template model from main CoA mnodule is simple But adding
translation to applied models: account_account, is a bit more difficult, as referencing
them trought po file may be inaccurate in multi company situation!
