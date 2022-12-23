# -*- coding: utf-8 -*-
from odoo import api,fields,models,_
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)



class ResPartner(models.Model):
    _inherit="res.partner"

    l10n_latam_identification_type_id = fields.Many2one()
    vat = fields.Char(copy=False,string="VAT")
    email_edi = fields.Char(copy=False)
    vat_is_required = fields.Boolean(string="vat_is_required")
    def get_partner_list(self,partner_objs):
        partner_list = ''
        for partner in partner_objs:
            if partner.name == False:
                partner.name = ''
            partner_list = partner_list + ' || ' + partner.name
        return partner_list

# define vat and email_edi with unique fields
    @api.constrains('vat','email_edi')
    def _check_vat_unique(self):
        is_extra_funcion = self.env.user.company_id.extra_function
        email_is_required = self.env.user.company_id.email_is_required
        regime_type_is_required = self.env.user.company_id.regime_type_is_required
        municipality_is_required = self.env.user.company_id.municipality_is_required
        document_type_is_required = self.env.user.company_id.document_type_is_required
        liability_is_required = self.env.user.company_id.liability_is_required
        vat_is_required = self.env.user.company_id.vat_is_required

        for record in self:
            if record.vat:
                #ADD validations to VAT
                letters = list(map(chr, range(65, 91)))
                vat_only_nums = (record.vat).replace('-','')
                if is_extra_funcion:
                    if (((record.vat).count('-') < 2) and (vat_only_nums.isnumeric()) and (record.vat)[len((record.vat))-1].isnumeric() and len((record.vat))==11 and (record.vat)[9]=='-' and record.l10n_co_document_type == 'rut') or ((record.vat).isnumeric() and record.l10n_co_document_type != 'rut' ):
                        _logger.info("Correct VAT format")
                    
                    elif record.l10n_co_document_type == 'external_id' and (record.vat[0] in letters and record.vat[1] in letters):
                        _logger.info("Correct VAT format")
                    else:
                        raise ValidationError(_('The "'+ record.vat +'" VAT does not comply with the correct format.\n' + 'Correct Nit format: xxxxxxxxx-x  where x represents an integer digit.\n' +'If your document type is other, the correct format are only numbers.'))
            if is_extra_funcion:

                if record.vat:
                    partner_objs = record.env['res.partner'].search([('vat','=',record.vat),('id','!=',record.id)])
                    if record.get_partner_list(partner_objs) and record.vat:
                        raise ValidationError(_('The vat ' +record.vat+' is already exist in the following records:' + '\n' + record.get_partner_list(partner_objs)))

                if record.email_edi:
                    partner_objs = record.env['res.partner'].search([('email_edi','=',record.email_edi),('id','!=',record.id)])
                    if record.get_partner_list(partner_objs):
                        raise ValidationError(_('The Email for invoicing ' +record.email_edi+' is already exist in the following records:' + '\n' + record.get_partner_list(partner_objs)))

                #validations for import data 
                required_fields = {
                    'vat' : [record.vat,vat_is_required,'vat'],
                    'l10n_co_document_type' : [record.l10n_co_document_type,document_type_is_required,'Document type'],
                    'type_regime_id' : [record.type_regime_id,regime_type_is_required,'Regime type'],
                    'type_liability_id' : [record.type_liability_id,liability_is_required,'Liability type'],
                    'municipality_id' : [record.municipality_id,municipality_is_required,'Municipality id'],
                    'email_edi' : [record.email_edi,email_is_required,'email for invoicing']
                }
                for rec in required_fields:
                    if not required_fields[rec][0] and required_fields[rec][1]:    
                            partner_objs = record.env['res.partner'].search([(rec,'=',False),('id','!=',record.id)])
                            if record.get_partner_list(partner_objs):
                                raise ValidationError(_('Please Add '+required_fields[rec][2]))
    
    #If extra_functions is active, the user don't have permissions to duplicate contacts
    @api.multi
    def copy(self):
        res = super(ResPartner, self).copy()
        is_extra_funcion = self.env.user.company_id.extra_function
        vat_is_required = self.env.user.company_id.vat_is_required
        if is_extra_funcion:
            raise ValidationError(_('You do not have permissions to duplicate a contact'))
        return res

    #Define obligatories fields to Electronic Invoicing
    @api.multi
    def write(self,values):
        res = super(ResPartner, self).write(values)
        is_extra_funcion = self.env.user.company_id.extra_function
        email_is_required = self.env.user.company_id.email_is_required
        regime_type_is_required = self.env.user.company_id.regime_type_is_required
        municipality_is_required = self.env.user.company_id.municipality_is_required
        document_type_is_required = self.env.user.company_id.document_type_is_required
        liability_is_required = self.env.user.company_id.liability_is_required
        vat_is_required = self.env.user.company_id.vat_is_required

        for record in self:
            if is_extra_funcion:
                if not record.vat and vat_is_required:
                    raise ValidationError(_('Please add vat'))
                elif (not record.l10n_co_document_type and document_type_is_required):
                    raise ValidationError(_('Please Add document type'))
                elif (not record.type_regime_id and regime_type_is_required):
                    raise ValidationError(_('Please Add regime type -----> (Electronic Invoicing Field)'))
                elif (not record.type_liability_id and liability_is_required):
                    raise ValidationError(_('Please Add liability type -----> (Electronic Invoicing Field)'))
                elif (not record.municipality_id and municipality_is_required):
                    raise ValidationError(_('Please Add municipality -----> (Electronic Invoicing Field)'))
                elif (not record.email_edi and email_is_required):
                    raise ValidationError(_('Please Add email for invoicing -----> (Electronic Invoicing Field)'))
        return res

