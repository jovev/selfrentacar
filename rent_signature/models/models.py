# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rent_signature(models.Model):
#     _name = 'rent_signature.rent_signature'
#     _description = 'rent_signature.rent_signature'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
