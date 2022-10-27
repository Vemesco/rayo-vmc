# -*- coding: utf-8 -*-	
# Part of Odoo. See LICENSE file for full copyright and licensing details.	

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):	
    _inherit = "res.company"	
    extra_function = fields.Boolean(string='Activate extra-function', default = False )

class ResConfigSettings(models.TransientModel):	
    _inherit = "res.config.settings"	

    extra_function = fields.Boolean(related="company_id.extra_function", string='Activate extra-function', default = False, readonly = False)
    

    