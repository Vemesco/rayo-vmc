# -*- coding: utf-8 -*-	
# Part of Odoo. See LICENSE file for full copyright and licensing details.	

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):	
    _inherit = "res.company"	

    extra_function = fields.Boolean(string='Activate extra-function', default = False)
    email_is_required = fields.Boolean(string='Email', default = False)
    regime_type_is_required= fields.Boolean(string='Regime type', default = False)
    municipality_is_required= fields.Boolean(string='Municipality', default = False)
    document_type_is_required= fields.Boolean(string='Document type', default = False)
    liability_is_required= fields.Boolean(string='Liability type', default = False)

class ResConfigSettings(models.TransientModel):	
    _inherit = "res.config.settings"	

    extra_function = fields.Boolean(related="company_id.extra_function", string='Activate extra-function', default = False, readonly = False)
    email_is_required = fields.Boolean(related="company_id.email_is_required", string='Email for Invoicing', default = False, readonly = False)
    regime_type_is_required= fields.Boolean(related="company_id.regime_type_is_required", string='Regime Type', default = False, readonly = False)
    municipality_is_required= fields.Boolean(related="company_id.municipality_is_required", string='Municipality', default = False, readonly = False)
    document_type_is_required= fields.Boolean(related="company_id.document_type_is_required", string='Document Type', default = False, readonly = False)
    liability_is_required= fields.Boolean(related="company_id.liability_is_required", string='Liability', default = False, readonly = False)

    