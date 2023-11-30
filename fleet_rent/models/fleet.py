# See LICENSE file for full copyright and licensing details.
"""Fleet Model."""

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class FleetVehicleExtend(models.Model):
    """Fleet Vehicle Extend."""

    _inherit = "fleet.vehicle"

    def _compute_count_rent(self):
        """Count the total number of Rent for the current vehicle."""
        rent_obj = self.env["fleet.rent"]
        for vehicle in self:
            vehicle.rent_count = rent_obj.search_count(
                [("vehicle_id", "=", vehicle.id)]
            )

    rent_count = fields.Integer(compute="_compute_count_rent", string="Rents")
    web_car_id = fields.Integer("Web Car ID")    # Koristi se za uskladjivanje sa ID u WP za dodatne opcije pri rentiranju
    web_price_group_id = fields.Integer("Web Car ID")    # Koristi se za uskladjivanje sa ID u WP za dodatne opcije pri rentiranju

class FleetVehicleCategoryExtend(models.Model):
    """Fleet Category Vehicle Extend."""

    _inherit = "fleet.vehicle.model.category"
    web_site_cat_id = fields.Integer("Web Category ID")