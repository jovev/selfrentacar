# -*- coding: utf-8 -*-

from odoo import _, models, fields, api


class rentomat_configurator(models.Model):
    _name = 'rentomat.configurator'
    _description = 'Rentomat configurator containing key RFID positions'

    name = fields.Char()
    rentomat_id = fields.Char(string = "Rentomat ID")
    location_id = fields.Many2one("stock.location", string = "Rentomat location")
    max_rentomat_capacity = fields.Integer("Rentomat capacity")
    position_1 = fields.Char("RFID for position 1")
    position_2 = fields.Char("RFID for position 2")
    position_3 = fields.Char("RFID for position 3")
    position_4 = fields.Char("RFID for position 4")
    position_5 = fields.Char("RFID for position 5")
    position_6 = fields.Char("RFID for position 6")
    position_7 = fields.Char("RFID for position 7")
    position_8 = fields.Char("RFID for position 8")
    position_9 = fields.Char("RFID for position 9")
    position_10 = fields.Char("RFID for position 10")
    position_11 = fields.Char("RFID for position 11")
    position_12 = fields.Char("RFID for position 12")
    


    description = fields.Text("Description")

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
