# -*- coding: utf-8 -*-
#############################################################################
#
#    Irvas International d.0.0
#
#    Copyright (C) 2021-TODAY Irvas(<https://www.irvas.rs>).
#    Author: Cybrosys Technogies @cybrosys(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import api, fields, models, tools


class StockGeoLocation(models.Model):
    _inherit = "stock.location"

    location_latitude = fields.Float(string="Location Latitude")
    location_longitude = fields.Float(string="Location Longitude")
    parking_location = fields.Boolean(string = "is Parking Location")
    keybox_location = fields.Boolean(string = "is KeyBox Location")
   # key_position = fields.Char(string = "Key Position")

    #street_name = fields.Char('Street Name')
    #street_number = fields.Char('Street Number')
    # street_name = fields.Char(
    #     'Street Name', compute='_compute_street_data', inverse='_inverse_street_data', store=True)
    # street_number = fields.Char(
    #     'House', compute='_compute_street_data', inverse='_inverse_street_data', store=True)
    # street_number2 = fields.Char(
    #     'Door', compute='_compute_street_data', inverse='_inverse_street_data', store=True)

    city_id = fields.Many2one(comodel_name='res.city', string='City ID')
   # country_enforce_cities = fields.Boolean(related='country_id.enforce_cities')

   # def _inverse_street_data(self):
   #     """ update self.street based on street_name, street_number and street_number2 """
   #     for partner in self:
   #         street = ((partner.street_name or '') + " " + (partner.street_number or '')).strip()
   #         if partner.street_number2:
   #             street = street + " - " + partner.street_number2
   #         partner.street = street

    @api.depends('street')
    def _compute_street_data(self):
        """Splits street value into sub-fields.
        Recomputes the fields of STREET_FIELDS when `street` of a partner is updated"""
        for partner in self:
            partner.update(tools.street_split(partner.street))

    def _get_street_split(self):
        self.ensure_one()
        return {
            'street_name': self.street_name,
            'street_number': self.street_number,
            'street_number2': self.street_number2
        }

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            self.city = self.city_id.name
            self.zip = self.city_id.zipcode
            self.state_id = self.city_id.state_id
        elif self._origin:
            self.city = False
            self.zip = False
            self.state_id = False