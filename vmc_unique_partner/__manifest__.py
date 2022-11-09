# -*- coding: utf-8 -*-
{
    'name': "Vmc prevent duplicates partners",
    'version': "12.0.1.0.0",
    'summary': """Module to prevent duplicates partners. """,
    'author': "Vemesco",
    'website': "https://vemesco.com/",
    'category': 'Uncategorized',
    'depends': [
        'base',
        'l10n_co_edi_jorels',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/extra_function.xml',
    ],
}
