# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rent_signature(models.Model):
    _name = 'fleet.rent.signature'
    _description = 'rent_signature.rent_signature'


    signature = fields.Binary(string='Signature')

    def clear_signature(self):
        self.signature = False
