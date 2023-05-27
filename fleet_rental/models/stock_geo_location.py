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

from odoo import models, fields


class StockGeoLocation(models.Model):
    _inherit = "stock.location"

    location_latitude = fields.Float(string="Location Latitude")
    location_longitude = fields.Float(string="Location Longitude")
    parking_location = fields.Boolean(string = "os Parking Location")