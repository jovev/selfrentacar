# See LICENSE file for full copyright and licensing details.
"""Fleet Rent Model."""

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF, ustr
import logging
try:
  import qrcode
except ImportError:
  qrcode = None
try:
  import base64
except ImportError:
  base64 = None
from io import BytesIO
_logger = logging.getLogger(__name__)
READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel'}
}
class FleetRent(models.Model):
    """Fleet Rent Model."""

    _name = "fleet.rent"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']  # ovo je kljucno za portal pristup
    _description = "Fleet Rent"
#    _order = 'date_order desc, id desc'
    _check_company_auto = True

    @api.onchange("vehicle_id")
    def _compute_change_vehicle_owner(self):
        """Method to display owner name."""
        for rent in self:
            rent.vehicle_owner = False
            if rent.vehicle_id:
                # we added sudo in below code to fix the access issue with rent user.
                rent.vehicle_owner = rent.vehicle_id.sudo().vehicle_owner.name
 
    @api.onchange("vehicle_id")
    def change_odometer(self):
        _logger.info("--------------------------------USAO u change odometer    self == %s" , self)
        """Method to display odometer value."""
        for rent in self:
            if rent.vehicle_id:
                rent.odometer = rent.vehicle_id.odometer

    @api.depends("account_move_line_ids")
    def _compute_total_deb_cre_amt_calc(self):
        """Method to calculate Total income amount."""
        for rent in self:
            rent.total_deb_cre_amt = rent.total_debit_amt - rent.total_credit_amt

    def _compute_total_credit_amt_calc(self):
        """Method to calculate Total credit amount."""
        for rent in self:
            rent.total_credit_amt = sum(
                acc_mov_line.credit or 0.0
                for acc_mov_line in rent.account_move_line_ids
            )

    def _compute_total_debit_amt_calc(self):
        """Method to calculate Total debit amount."""
        for rent in self:
            rent.total_debit_amt = sum(
                acc_mov_line.debit or 0.0 for acc_mov_line in rent.account_move_line_ids
            )

    @api.model
    def default_get(self, fields):
        """Overridden method to update odometer in fleet rent."""
        context = self._context or {}
        vehical_obj = self.env["fleet.vehicle"]
        res = super(FleetRent, self).default_get(fields)
        if res.get("vehicle_id", False):
            vehicle = vehical_obj.browse(res["vehicle_id"])
            if (
                context.get("from_rent_smartbutton", False)
                and vehicle.state == "write-off"
            ):
                msg = _("Rent can not create when vehicle " "in write-off state !!")
                raise UserError(msg)
            if vehicle.state == "write-off":
                res.update({"vehicle_id": False, "odometer": vehicle.odometer or 0.0})
            else:
                res.update({"odometer": vehicle.odometer or 0.0})
        return res

    def _compute_get_odometer(self):
        _logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!! USAO computer_get_odometer   self == %s", self)
        odometer_obj = self.env["fleet.vehicle.odometer"]
        for rent in self:
            if rent.vehicle_id:
                odometer = odometer_obj.search(
                    [("vehicle_id", "=", rent.vehicle_id.id)],
                    limit=1,
                    order="value desc",
                )
                if odometer:
                    rent.odometer = odometer.value

    def _inverse_set_odometer(self):
        _logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$ USAO incverse_set_odometer   self == %s", self)
        odometer_obj = self.env["fleet.vehicle.odometer"]
        for rent in self:
            if rent.vehicle_id:
                odometer = odometer_obj.search(
                    [("vehicle_id", "=", rent.vehicle_id.id)],
                    limit=1,
                    order="value desc",
                )
                if rent.odometer < odometer.value:
                    msg = _(
                        "User Error!\nYou can't add odometer less "
                        "than previous odometer value %s !"
                    ).format(odometer.value)
                    raise UserError(msg)

                if rent.odometer:
                    date = fields.Date.context_today(rent)
                    odometer_obj.create(
                        {
                            "value": rent.odometer,
                            "date": date,
                            "vehicle_id": rent.vehicle_id.id,
                        }
                    )

    @api.depends("deposit_amt")
    def _compute_get_deposit(self):
        """Method to set deposit return and deposit received."""
        for rent in self:
            deposit_inv_ids = self.env["account.move"].search(
                [
                    ("fleet_rent_id", "=", rent.id),
                    ("move_type", "=", "out_invoice"),
                    ("state", "in", ["posted"]),
                    ("is_deposit_inv", "=", True),
                ]
            )
            residual_amt = 0.0
            rent.deposit_received = False
            if deposit_inv_ids:
                residual_amt = sum(
                    [
                        dp_inv.amount_residual
                        for dp_inv in deposit_inv_ids
                        if dp_inv.amount_residual > 0.0
                    ]
                )
                if residual_amt > 0.0:
                    rent.deposit_received = False
                else:
                    rent.deposit_received = True

    @api.depends("amount_return")
    def _compute_amount_return(self):
        """Method to set the deposit return value."""
        for rent in self:
            credit_inv_ids = self.env["account.move"].search(
                [
                    ("fleet_rent_id", "=", rent.id),
                    ("move_type", "=", "out_refund"),
                    ("state", "in", ["posted"]),
                    ("is_deposit_return_inv", "=", True),
                ]
            )
            residual_amt = 0.0
            rent.is_deposit_return = False
            if credit_inv_ids:
                residual_amt = sum(
                    [
                        credit_inv.amount_residual
                        for credit_inv in credit_inv_ids
                        if credit_inv.amount_residual > 0.0
                    ]
                )
                if residual_amt > 0.0:
                    rent.is_deposit_return = False
                else:
                    rent.is_deposit_return = True

    @api.depends("rent_type_id", "date_start")
    def _compute_create_date(self):
        for rent in self:
            if rent.rent_type_id and rent.date_start:
                if rent.rent_type_id.renttype == "Months":
                    rent.date_end = rent.date_start + relativedelta(
                        months=int(rent.rent_type_id.duration)
                    )
                if rent.rent_type_id.renttype == "Years":
                    rent.date_end = rent.date_start + relativedelta(
                        years=int(rent.rent_type_id.duration)
                    )
                if rent.rent_type_id.renttype == "Weeks":
                    rent.date_end = rent.date_start + relativedelta(
                        weeks=int(rent.rent_type_id.duration)
                    )
                if rent.rent_type_id.renttype == "Days":
                    rent.date_end = rent.date_start + relativedelta(
                        days=int(rent.rent_type_id.duration)
                    )
                if rent.rent_type_id.renttype == "Hours":
                    rent.date_end = rent.date_start + relativedelta(
                        hours=int(rent.rent_type_id.duration)
                    )

    @api.depends("maintanance_ids", "maintanance_ids.cost")
    def _compute_total_maintenance_cost(self):
        """Method to calculate total maintenance."""
        for rent in self:
            rent.maintenance_cost = sum(
                cost_line.cost or 0.0 for cost_line in rent.maintanance_ids
            )

    @api.depends("rent_schedule_ids", "rent_schedule_ids.amount")
    def _compute_total_amount_rent(self):
        """Method to calculate Total Rent of current Tenancy."""
        for rent in self:
            rent.total_rent = sum(
                rent_line.amount or 0.0 for rent_line in rent.rent_schedule_ids
            )

    name = fields.Char(translate=True, copy=False, default="New")
    state = fields.Selection(
        [
            ("draft", "New"),
            ("open", "Reserved"),
            ("pending", "To Renew"),
            ("close", "Closed"),
            ("running", "Checked Out"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        "Status",
        default="draft",
        copy=False,
    )
    vehicle_id = fields.Many2one("fleet.vehicle", "Vehicle", help="Name of Vehicle.")
    vehicle_owner = fields.Char(
        "vehicle_owner", compute="_compute_change_vehicle_owner"
    )

    # user_id = fields.Many2one(
    #     comodel_name='res.users',
    #     string="Salesperson",
    #     compute='_compute_user_id',
    #     store=True, readonly=False, precompute=True, index=True,
    #     tracking=2,
    #     domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
    #         self.env.ref("sales_team.group_sale_salesman").id
    #     ))

    tenant_id = fields.Many2one(
        "res.users", "Tenant", help="Tenant Name of Rental Vehicle."
    )
    driver_licence_id = fields.Char(
        related="tenant_id.d_id", required=False, store=True, translate=True, readonly=False, string = "Licence No"
    )
    driver_passport_id = fields.Char(
        related="tenant_id.ref", required=False, store=True, translate=True, readonly=False, string = "Passport No"
    )
    driver_id1 = fields.Char(string="Driver 1")
    driver1_driver_licence_no = fields.Char(string="Licence No")
    driver1_passport_no = fields.Char(string="Passport No")



   # tenant_id = fields.Many2one(
   #     "res.partner", "Tenant", help="Tenant Name of Rental Vehicle."
   # )

    fleet_tenant_id = fields.Many2one(
        related="tenant_id.partner_id",
        store=True,
        help="Tenant Name of Rental Vehicle.",
    )
    user_id = fields.Many2one(
        "res.users", "Account Manager", help="Manager of Rental Vehicle."
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env["res.company"]._default_currency_id(),
        help="The optional other currency \
                                  if it is a multi-currency entry.",
    )
    odometer = fields.Float(
        compute="_compute_get_odometer",
        inverse="_inverse_set_odometer",
        help="Odometer measure of the vehicle at \
                            the moment of this log",
    )
    odometer_unit = fields.Selection(
        [("kilometers", "Kilometers"), ("miles", "Miles")],
        related="vehicle_id.odometer_unit",
        help="Unit of the vehicle odometer.",
        default="kilometers",
        store=True,
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, help="Name of Company."
    )
    rent_amt = fields.Monetary(
        "Rental Vehicle Rent",
        currency_field="currency_id",
        help="Rental vehicle rent for selected \
                                vehicle per rent type.",
        copy=False,
    )
    deposit_amt = fields.Monetary(
        "Deposit Amount",
        copy=False,
        currency_field="currency_id",
        help="Deposit amount for Rental Vehicle.",
    )
    deposit_received = fields.Boolean(
        compute="_compute_get_deposit",
        copy=False,
        help="True if deposit amount received for " "current Rental Vehicle.",
    )
    is_payment_received = fields.Boolean(
        copy=False,
        help="True if rent amount received for " "current Rental Vehicle.",
    )
    is_deposid_received = fields.Boolean(
        copy=False,
        help="True if deposid received for " "current Rental Vehicle.",
    )
    contact_id = fields.Many2one("res.partner", "Contact", help="Contact person name.")
    contract_dt = fields.Datetime(
        "Contract Creation",
        default=lambda *a: datetime.now(),
        help="Rental Vehicle contract creation date.",
    )
    amount_return = fields.Monetary(
        "Deposit Returned",
        copy=False,
        currency_field="currency_id",
        help="Deposit Returned amount for Rental Vehicle.",
    )
    is_deposit_return = fields.Boolean(
        compute="_compute_amount_return",
        copy=False,
        help="True if deposit amount returned for current Rental Vehicle.",
    )
    maintenance_cost = fields.Float(
        compute="_compute_total_maintenance_cost",
        store=True,
        help="Add Maintenance Cost.",
    )
    date_start = fields.Datetime(
        "Start Date",
        default=lambda *a: datetime.now(),
        help="Rental Vehicle contract start date.",
    )
    date_end = fields.Datetime(
        compute="_compute_create_date",
        store=True,
        help="Rental Vehicle contract end date.",
    )
    rent_type_id = fields.Many2one("rent.type", "Rent Type")
    total_rent = fields.Monetary(
         compute="_compute_total_amount_rent",
         currency_field="currency_id",
         store=True,
         help="Total rent of this Rental Vehicle.",
    )
    duration = fields.Char("Duration")
    rent_close_by = fields.Many2one("res.users", copy=False)
    date_close = fields.Datetime("Rent Close Date", copy=False)

    rent_schedule_ids = fields.One2many(
        "tenancy.rent.schedule", "fleet_rent_id", "Rent Schedule"
    )

    maintanance_ids = fields.One2many(
        "maintenance.cost", "fleet_rent_id", "Maintenance Costs"
    )
    description = fields.Text()
    account_move_line_ids = fields.One2many(
        "account.move.line", "fleet_rent_id", "Account Move"
    )
    account_payment_ids = fields.One2many("account.payment", "fleet_rent_id", "Entries")
    total_debit_amt = fields.Monetary(
        compute="_compute_total_debit_amt_calc",
        string="Total Debit Amount",
        currency_field="currency_id",
    )
    total_credit_amt = fields.Monetary(
        compute="_compute_total_credit_amt_calc",
        string="Total Credit Amount",
        currency_field="currency_id",
    )
    total_deb_cre_amt = fields.Monetary(
        compute="_compute_total_deb_cre_amt_calc",
        string="Total Expenditure",
        currency_field="currency_id",
    )
    invoice_id = fields.Many2one("account.move", "Invoice")
    cr_rent_btn = fields.Boolean("Hide Rent Button", copy=False)

    close_reson = fields.Text("Rent Close Reason", help="Rent Close Reason.")
    invoice_count = fields.Integer(
        compute="_compute_count_invoice",
    )
    refund_inv_count = fields.Integer(
        compute="_compute_count_refund_invoice", string="Refund"
    )
    # Dodao lubi - prosirenje modela
    #
    require_signature = fields.Boolean(
        string="Online Signature",
        compute='_compute_require_signature',
        store=True, readonly=False, precompute=True,
        states=READONLY_FIELD_STATES,
        help="Request a online signature and/or payment to the customer in order to confirm orders automatically.")
    require_payment = fields.Boolean(
        string="Online Payment",
        compute='_compute_require_payment',
        store=True, readonly=False, precompute=True,
        states=READONLY_FIELD_STATES)

    signature = fields.Image(
        string="Signature",
        copy=False, attachment=True, max_width=1024, max_height=1024)
    signed_by = fields.Char(
        string="Signed By", copy=False)
    signed_on = fields.Datetime(
        string="Signed On", copy=False)
    qr_code = fields.Binary("QR Code", compute='generate_qr_code')


    option_ids = fields.One2many(
        "fleet.rent.options", "fleet_rent_id", "Option Costs"
    )
    attachment_ids = fields.Many2many('ir.attachment', 'car_fleet_rent_checklist_ir_attachments_rel',
                                     'rental_id', 'attachment_id', string="Attachments",
                                     help="Images of the vehicle before contract/any attachments")
    checklist_line = fields.One2many('car.fleet.rent.checklist', 'fleet_rent_id', string="Checklist",
                                     help="Facilities/Accessories, That should verify when closing the contract.",
                                     states={'invoice': [('readonly', True)],
                                             'done': [('readonly', True)],
                                             'cancel': [('readonly', True)]})
    total = fields.Float(string="Total (Accessories/Tools)", readonly=True, copy=False)
    tools_missing_cost = fields.Float(string="Missing Cost", readonly=True, copy=False,
                                      help='This is the total amount of missing tools/accessories')
    damage_cost = fields.Float(string="Damage Cost", copy=False)
    damage_cost_sub = fields.Float(string="Damage Cost", readonly=True, copy=False)
    total_cost = fields.Float(string="Total", readonly=True, copy=False)
#############
    web_car_request = fields.Char(string="Required car model, class, ..")
    plate = fields.Char(string="Vehicle Plate", related='vehicle_id.license_plate')
    rent_from = fields.Many2one('stock.location', string='Start location')
    rent_from_longitude = fields.Float(string="GPS X", related='rent_from.location_longitude')
    rent_from_longitude = fields.Float(string="GPS Y", related='rent_from.location_latitude')
    return_location = fields.Many2one('stock.location', string='Return location')
    reservation_code = fields.Char(string="Reservation Code", copy=False)
    allow_crossborder = fields.Boolean(string="Cross Border")
    amount_pay_deposit = fields.Float(string="Amount pay deposit", copy=False)
    pickup_fuel = fields.Selection([('e', 'Empty'), ('14', '1/4'), ('12', '1/2'), ('34', '3/d'),
                                    ('f', 'Full')], string="Pickup fuel",
                                   help='Feel level at pickup', required=False)
    dropoff_fuel = fields.Selection([('e', 'Empty'), ('14', '1/4'), ('12', '1/2'), ('34', '3/d'),
                                     ('f', 'Full')], string="Dropoff fuel",
                                    help='Feel level at dropoff', required=False)
    x_bazna_lokacija = fields.Many2one(related='vehicle_id.x_bazna_lokacija', string = 'Base Location')
    x_trenutna_lokacija = fields.Many2one(related='vehicle_id.x_trenutna_lokacija', string='Current Location')
    x_key_position = fields.Char(related='vehicle_id.x_key_position', string = 'Key position in KeyBox')
    x_key_rfid = fields.Char(related='vehicle_id.x_key_rfid', string='Key RFID number')
    x_total_rent =fields.Monetary(
         currency_field="currency_id",
         string="Total Rent",
         help="Total rent of this Rental Vehicle.",
    )
    notes = fields.Char(string = "Additional notes")


# Info o placanjima
    # Payment fields
    transaction_ids = fields.Many2many(
        comodel_name='payment.transaction',
        relation='fleet_rent_transaction_rel',
        string="Transactions",
        copy=False, readonly=True)
    authorized_transaction_ids = fields.Many2many(
        comodel_name='payment.transaction',
        string="Authorized Transactions",
        compute='_compute_authorized_transaction_ids',
        copy=False)

#    Info o vozacima:
#

  #  driver_id2 = fields.Many2one('res.partner', string="Driver 2", )
  #  driver2_passport_no = fields.Char(string="Passport No", related='driver_id2.ref')
  #  driver2_driver_licence_no = fields.Char(string="Licence No", related='driver_id2.d_id')
    def generate_qr_code(self):
       for rec in self:
           if qrcode and base64:
               qr = qrcode.QRCode(
                   version=1,
                 error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=3,
                   border=4,
               )
               base_url = rec.env['ir.config_parameter'].get_param('web.base.url')
               access_url = rec.get_portal_url()
               qr.add_data(base_url)
               qr.add_data(access_url)
               qr.make(fit=True)
               img = qr.make_image()
               temp = BytesIO()
               img.save(temp, format="PNG")
               qr_image = base64.b64encode(temp.getvalue())
               rec.update({'qr_code': qr_image})
    @api.depends('transaction_ids')
    def _compute_authorized_transaction_ids(self):
        for trans in self:
            trans.authorized_transaction_ids = trans.transaction_ids.filtered(lambda t: t.state == 'authorized')
    @api.depends('company_id')
    def _compute_require_payment(self):
        for order in self:
            order.require_payment = order.company_id.portal_confirmation_pay
    @api.depends('company_id')
    def _compute_require_signature(self):
        for order in self:
            order.require_signature = order.company_id.portal_confirmation_sign

    def _has_to_be_signed(self, include_draft=False):
        return (self.state == 'open' or (self.state == 'draft' and include_draft)) and self.require_signature and not self.signature

    def action_preview_rent_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }



    @api.depends('checklist_line.checklist_active')
    def check_action_verify(self):
        flag = 0
        for each in self:
            for i in each.checklist_line:
                if i.checklist_active:
                    continue
                else:
                    flag = 1
            if flag == 1:
                each.check_verify = False
            else:
                each.check_verify = True
    def action_verify(self):
        self.state = "invoice"
        self.reserved_fleet_id.unlink()
        self.rent_end_date = fields.Date.today()
        if self.total_cost != 0:
            inv_obj = self.env['account.move']
            inv_line_obj = self.env['account.move.line']
            supplier = self.customer_id
            inv_data = {
                'ref': supplier.name,
                'partner_id': supplier.id,
                'currency_id': self.account_type.company_id.currency_id.id,
                'journal_id': self.journal_type.id,
                'invoice_origin': self.name,
                'company_id': self.account_type.company_id.id,
                'invoice_date_due': self.rent_end_date,
            }
            inv_id = inv_obj.create(inv_data)
            product_id = self.env['product.product'].search([("name", "=", "Fleet Rental Service")])
            if product_id.property_account_income_id.id:
                income_account = product_id.property_account_income_id
            elif product_id.categ_id.property_account_income_categ_id.id:
                income_account = product_id.categ_id.property_account_income_categ_id
            else:
                raise UserError(
                    _('Please define income account for this product: "%s" (id:%d).') % (product_id.name,
                                                                                         product_id.id))
            inv_line_data = {
                'name': "Damage/Tools missing cost",
                'account_id': income_account.id,
                'price_unit': self.total_cost,
                'quantity': 1,
                'product_id': product_id.id,
                'move_id': inv_id.id,
            }
            inv_line_obj.create(inv_line_data)
            imd = self.env['ir.model.data']
            action = self.env.ref('account.view_move_tree')
            list_view_id = self.env.ref('account.view_move_form', False)
            form_view_id = self.env.ref('account.view_move_tree', False)
            result = {
                'name': 'Fleet Rental Invoices',
                'view_mode': 'form',
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'views': [(list_view_id.id, 'tree'), (form_view_id.id, 'form')],
            }

            if len(inv_id) > 1:
                result['domain'] = "[('id','in',%s)]" % inv_id.ids
            else:
                result = {'type': 'ir.actions.act_window_close'}
            return result

    @api.constrains("deposit_amt", "rent_amt", "maintenance_cost")
    def check_amt(self):
        for amount in self:
            if amount.rent_amt < 0.0:
                msg = _(
                    "Rental Vehicle Rent amount should be greater than zero."
                    " Please add 'Rental Vehicle Rent' amount !!"
                )
                raise ValidationError(msg)
            if amount.deposit_amt < 0.0:
                msg = _(
                    "Deposit amount should be greater than zero."
                    " Please add 'Amount Deposit'!"
                )
                raise ValidationError(msg)
            if amount.maintenance_cost < 0.0:
                msg = _("Maintenance cost should be greater than zero.")
                raise ValidationError(msg)

    @api.constrains("vehicle_id")
    def _check_vehicle_id(self):
        for rec in self:
            duplicate_rent = self.env["fleet.rent"].search(
                [
                    ("state", "in", ["open", "pending", "close"]),
                    ("id", "!=", rec.id),
                    ("vehicle_id", "=", rec.vehicle_id.id),
                ]
            )
            if duplicate_rent:
                msg = _(
                    "Vehicle Rent Order is already "
                    "available for this vehicle !! \n Choose other"
                    " vehicle and Prepare new rent order !!"
                )
                raise ValidationError(msg)

    @api.depends('partner_id')
    def _compute_user_id(self):
        for order in self:
            if not order.user_id:
                order.user_id = order.partner_id.user_id or order.partner_id.commercial_partner_id.user_id or \
                                (self.user_has_groups('sales_team.group_sale_salesman') and self.env.user)
    def _compute_count_invoice(self):
        """Method to count Out Invoice."""
        obj = self.env["account.move"]
        for rent in self:
            rent.invoice_count = obj.search_count(
                [
                    ("move_type", "=", "out_invoice"),
                    ("fleet_rent_id", "=", rent.id),
                    ("is_deposit_inv", "=", True),
                ]
            )

    def _compute_count_refund_invoice(self):
        """Method to count Refund Invoice."""
        obj = self.env["account.move"]
        for rent in self:
            rent.refund_inv_count = obj.search_count(
                [
                    ("move_type", "=", "out_refund"),
                    ("fleet_rent_id", "=", rent.id),
                    ("is_deposit_return_inv", "=", True),
                ]
            )

    # ovo je preuzeto iz Sales Order
    def action_rentconfirmation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        _logger.info("***USAO u action_rentconfirmation_send    self == %s", self)
        self.ensure_one()
       # self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'fleet.rent',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        #    'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        
    def _find_mail_template(self):
        """ Get the appropriate mail template for the current sales order based on its state.

        If the SO is confirmed, we return the mail template for the sale confirmation.
        Otherwise, we return the quotation email template.

        :return: The correct mail template based on the current status
        :rtype: record of `mail.template` or `None` if not found
        """
        self.ensure_one()
        if self.env.context.get('proforma') or self.state not in ('new', 'open'):
            return self.env.ref('fleet_rent.mail_template_33_d7dff2da', raise_if_not_found=False)
        else:
            return self._get_confirmation_template()
            
    def _get_confirmation_template(self):
        """ Get the mail template sent on SO confirmation (or for confirmed SO's).

        :return: `mail.template` record or None if default template wasn't found
        """
        return self.env.ref('fleet_rent.mail_template_34_29ec1fd4', raise_if_not_found=False)

    def action_rent_confirm(self):
        """Method to confirm rent status."""
        for rent in self:
            rent_vals = {"state": "open"}
            if not rent.name or rent.name == "New":
                seq = self.env["ir.sequence"].next_by_code("fleet.rent")
                rent_vals.update({"name": seq})
            rent.write(rent_vals)
        self.ensure_one()
       # self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'fleet.rent',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        #    'model_description': self.with_context(lang=lang).type_name,
        }
        _logger.info("***IZABRAO MAIL TEMPLATE    self = %s   dragan = %s  ", self, self._context)
        self.action_send_email()
        

    def action_send_email(self):
        mail_template = self.env.ref('fleet_rent.fleet_email_template')
        mail_template.send_mail(self.id, force_send=True)

    def action_rent_close(self):
        """Method to Change rent state to close."""
        return {
            "name": _("Rent Close Form"),
            "res_model": "rent.close.reason",
            "type": "ir.actions.act_window",
            "view_id": False,
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
        }

    def action_rent_done(self):
        """Method to Change rent state to done."""
        rent_sched_obj = self.env["tenancy.rent.schedule"]
        for rent in self:
            if not rent.rent_schedule_ids:
                msg = _(
                    "Without Rent schedule you can not done the rent."
                    "\nplease first create the rent schedule."
                )
                raise ValidationError(msg)
            if rent.rent_schedule_ids:
                rent_schedule = rent_sched_obj.search(
                    [("paid", "=", False), ("id", "in", rent.rent_schedule_ids.ids)]
                )
                if rent_schedule:
                    msg = _(
                        "Scheduled Rents is remaining."
                        "\nplease first pay scheduled rents.!!"
                    )
                    raise ValidationError(msg)
                rent.state = "done"

    def action_set_to_draft(self):
        """Method to Change rent state to close."""
        for rent in self:
            if rent.state == "open" and rent.rent_schedule_ids:
                msg = _(
                    "You can not move rent to draft "
                    "stage because rent schedule is already created !!"
                )
                raise UserError(msg)
            rent.state = "draft"

    def action_set_to_renew(self):
        """Method to open rent renew wizard."""
        context = self.env.context
        context = dict(context)
        if context is None:
            context = {}
        for rent in self:
            rent.cr_rent_btn = False
            if rent.vehicle_id and rent.vehicle_id.state == "write-off":
                msg = _(
                    "You can not renew rent for %s because this"
                    " vehicle is in write-off."
                ).format(rent.vehicle_id.name)
                raise UserError(msg)
            tenancy_rent_ids = self.env["tenancy.rent.schedule"].search(
                [("fleet_rent_id", "=", rent.id), ("state", "in", ["draft", "open"])]
            )
            if tenancy_rent_ids:
                msg = _(
                    "In order to Renew a Tenancy,"
                    "Please make all related Rent Schedule entries posted !!"
                )
                raise UserError(msg)
            if rent.date_close:
                date = rent.date_close + timedelta(days=1)
            else:
                date = rent.date_end + timedelta(days=1)
            context.update({"default_start_date": date})
            return {
                "name": _("Tenancy Renew Wizard"),
                "res_model": "renew.tenancy",
                "type": "ir.actions.act_window",
                "view_id": False,
                "view_mode": "form",
                "view_type": "form",
                "target": "new",
                "context": context,
            }

    def action_deposite_return(self):
        """Method to return deposite."""
        for rent in self:
            deposit_inv_ids = self.env["account.move"].search(
                [
                    ("fleet_rent_id", "=", rent.id),
                    ("move_type", "=", "out_refund"),
                    ("state", "in", ["draft", "open", "in_payment"]),
                    ("is_deposit_return_inv", "=", True),
                ]
            )
            if deposit_inv_ids:
                msg = _(
                    "Deposit Return invoice is already Pending\n"
                    "Please proceed that Return invoice first"
                )
                raise UserError(msg)

            self.ensure_one()
            vehicle = rent.vehicle_id or False
            purch_journal = rent.env["account.journal"].search(
                [("type", "=", "sale")], limit=1
            )
            if vehicle and not vehicle.expence_acc_id:
                msg = _(
                    "Please Configure Expense Account in "
                    "Vehicle Registration form !!"
                )
                raise UserError(msg)

            inv_line_values = {
                "name": "Deposit Return" or "",
                "quantity": 1,
                "account_id": vehicle
                and vehicle.expence_acc_id
                and vehicle.expence_acc_id.id
                or False,
                "price_unit": rent.deposit_amt or 0.00,
                "fleet_rent_id": rent.id,
            }
            invoice_id = rent.env["account.move"].create(
                {
                    "invoice_origin": "Deposit Return For " + rent.name or "",
                    "move_type": "out_refund",
                    "partner_id": rent.tenant_id
                    and rent.tenant_id.partner_id.id
                    or False,
                    "invoice_line_ids": [(0, 0, inv_line_values)],
                    "invoice_date": fields.Date.today() or False,
                    "fleet_rent_id": rent.id,
                    "is_deposit_return_inv": True,
                    "journal_id": purch_journal and purch_journal.id or False,
                }
            )

            rent.write({"invoice_id": invoice_id.id})
        return True

    def action_deposite_receive(self):
        """Method to open the related payment form view."""
        for rent in self:
            deposit_inv_ids = self.env["account.move"].search(
                [
                    ("fleet_rent_id", "=", rent.id),
                    ("move_type", "=", "out_invoice"),
                    ("state", "in", ["draft", "open", "in_payment"]),
                    ("is_deposit_inv", "=", True),
                ]
            )
            if deposit_inv_ids:
                msg = _(
                    "Deposit invoice is already Pending\n"
                    "Please proceed that deposit invoice first"
                )
                raise UserError(msg)

            inv_line_values = {
                "name": "Deposit Receive" or "",
                "quantity": 1,
                "price_unit": rent.deposit_amt or 0.00,
                "fleet_rent_id": rent.id,
            }
            invoice_id = rent.env["account.move"].create(
                {
                    "move_type": "out_invoice",
                    "partner_id": rent.tenant_id
                    and rent.tenant_id.partner_id.id
                    or False,
                    "invoice_line_ids": [(0, 0, inv_line_values)],
                    "invoice_date": fields.Date.today() or False,
                    "fleet_rent_id": rent.id,
                    "is_deposit_inv": True,
                }
            )
            rent.write({"invoice_id": invoice_id.id})
            return True

    def create_rent_schedule(self):
        """Method to create rent schedule Lines."""
        for rent in self:
            for rent_line in rent.rent_schedule_ids:
                if not rent_line.paid and not rent_line.move_check:
                    msg = _(
                        "You can't create new rent "
                        "schedule Please make all related Rent Schedule "
                        "entries paid."
                    )
                    raise UserError(msg)
            rent_obj = self.env["tenancy.rent.schedule"]
            currency = rent.currency_id or False
            tenent = rent.tenant_id or False
            vehicle = rent.vehicle_id or False
            if rent.date_start and rent.rent_type_id and rent.rent_type_id.renttype:
                interval = int(rent.rent_type_id.duration)
                date_st = rent.date_start
                if rent.rent_type_id.renttype == "Months":
                    for _i in range(0, interval):
                        date_st = date_st + relativedelta(months=int(1))
                        rent_obj.create(
                            {
                                "start_date": date_st.strftime(DTF),
                                "amount": rent.rent_amt,
                                # at create time aslo set pan_amt (Pending Amount)
                                "pen_amt": rent.rent_amt,
                                "vehicle_id": vehicle and vehicle.id or False,
                                "fleet_rent_id": rent.id,
                                "currency_id": currency and currency.id or False,
                                "rel_tenant_id": tenent and tenent.id or False,
                            }
                        )
                if rent.rent_type_id.renttype == "Years":
                    for _i in range(0, interval):
                        date_st = date_st + relativedelta(years=int(1))
                        rent_obj.create(
                            {
                                "start_date": date_st.strftime(DTF),
                                "amount": rent.rent_amt,
                                # at create time aslo set pan_amt (Pending Amount)
                                "pen_amt": rent.rent_amt,
                                "vehicle_id": vehicle and vehicle.id or False,
                                "fleet_rent_id": rent.id,
                                "currency_id": currency and currency.id or False,
                                "rel_tenant_id": tenent and tenent.id or False,
                            }
                        )
                if rent.rent_type_id.renttype == "Weeks":
                    for _i in range(0, interval):
                        date_st = date_st + relativedelta(weeks=int(1))
                        rent_obj.create(
                            {
                                "start_date": date_st.strftime(DTF),
                                "amount": rent.rent_amt,
                                # at create time aslo set pan_amt (Pending Amount)
                                "pen_amt": rent.rent_amt,
                                "vehicle_id": vehicle and vehicle.id or False,
                                "fleet_rent_id": rent.id,
                                "currency_id": currency and currency.id or False,
                                "rel_tenant_id": tenent and tenent.id or False,
                            }
                        )
                if rent.rent_type_id.renttype == "Days":
                    rent_obj.create(
                        {
                            "start_date": date_st.strftime(DTF),
                            "amount": rent.rent_amt * interval,
                            # at create time aslo set pan_amt (Pending Amount)
                            "pen_amt": rent.rent_amt * interval,
                            "vehicle_id": vehicle and vehicle.id or False,
                            "fleet_rent_id": rent.id,
                            "currency_id": currency and currency.id or False,
                            "rel_tenant_id": tenent and tenent.id or False,
                        }
                    )
                if rent.rent_type_id.renttype == "Hours":
                    rent_obj.create(
                        {
                            "start_date": date_st.strftime(DTF),
                            "amount": rent.rent_amt * interval,
                            # at create time aslo set pan_amt (Pending Amount)
                            "pen_amt": rent.rent_amt * interval,
                            "vehicle_id": vehicle and vehicle.id or False,
                            "fleet_rent_id": rent.id,
                            "currency_id": currency and currency.id or False,
                            "rel_tenant_id": tenent and tenent.id or False,
                        }
                    )
                # cr_rent_btn is used to hide rent schedule button.
                rent.cr_rent_btn = True
        return True

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        create_context = dict(self.env.context or {})
        create_context['default_user_ids'] = False
        if custom_values is None:
            custom_values = {}
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
            'user_id': "WEB BOOKING",
            'contact_id': msg.get('author_id'),
        }
        defaults.update(custom_values)

        rent = super(Rent, self.with_context(create_context)).message_new(msg, custom_values=defaults)
        email_list = rent.email_split(msg)
        partner_ids = [p.id for p in self.env['mail.thread']._mail_find_partner_from_emails(email_list, records=rent,
                                                                                            force_create=False) if p]
        rent.message_subscribe(partner_ids)
        return rent
    def _get_portal_return_action(self):
        """ Return the action used to display orders when returning from customer portal. """
        self.ensure_one()
        return self.env.ref('ii_carrental_portal.action_quotations_with_onboarding')
    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        """
            Get a portal url for this model, including access_token.
            The associated route must handle the flags for them to have any effect.
            - suffix: string to append to the url, before the query string
            - report_type: report_type query string, often one of: html, pdf, text
            - download: set the download query string to true
            - query_string: additional query string
            - anchor: string to append after the anchor #
        """
        _logger.info("***USAO u GET PORTAL URL    self == %s", self)
        self.ensure_one()
        token = self._portal_ensure_token()
        _logger.info("*****************     URL == %s", token)
        url = self.access_url + '%s?access_token=%s%s%s%s%s' % (
            suffix if suffix else '',
            self._portal_ensure_token(),
            '&report_type=%s' % report_type if report_type else '',
            '&download=true' if download else '',
            query_string if query_string else '',
            '#%s' % anchor if anchor else ''
        )
        _logger.info("*****************     URL == %s", url)
        return url

    def _compute_access_url(self):
        super()._compute_access_url()
        for order in self:
            order.access_url = f'/my/carrental_contract/{order.id}'

    def _has_to_be_paid(self, include_draft=False):
        return True
    #    transaction = self.get_portal_last_transaction()
    #    return (self.state == 'sent' or (
    #                self.state == 'draft' and include_draft)) and not self.is_expired and self.require_payment and transaction.state != 'done' and self.amount_total


class RentType(models.Model):
    """Rent Type Model."""

    _name = "rent.type"
    _description = "Vehicle Rent Type"

    # @api.model
    # def create(self, vals):
    #     """Overridden Method."""
    #     if vals.get('duration') < 1:
    #         raise ValidationError("You Can't Enter Duration Less "
    #                               "Than One(1).")
    #     return super(RentType, self).create(vals)

    @api.constrains("duration")
    def _check_vehicle_id(self):
        if self.duration < 1:
            msg = _("You Can't Enter Duration Less " "Than One(1).")
            raise ValidationError(msg)

    @api.depends("duration", "renttype")
    def name_get(self):
        """Name get Method."""
        res = []
        for rec in self:
            rec_str = ""
            if rec.duration:
                rec_str += ustr(rec.duration)
            if rec.renttype:
                rec_str += " " + rec.renttype
            res.append((rec.id, rec_str))
        return res

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """Name Search Method."""
        args += ["|", ("duration", operator, name), ("renttype", operator, name)]
        cuur_ids = self.search(args, limit=limit)
        return cuur_ids.name_get()

    @api.onchange("duration", "renttype")
    def onchange_renttype_name(self):
        """Onchange Rent Type Name."""
        full_name = ""
        for rec in self:
            if rec.duration:
                full_name += ustr(rec.duration)
            if rec.renttype:
                full_name += " " + ustr(rec.renttype)
            rec.name = full_name

    name = fields.Char()
    duration = fields.Integer(default=1)
    renttype = fields.Selection(
        [
            ("Hours", "Hours"),
            ("Days", "Days"),
            ("Weeks", "Weeks"),
            ("Months", "Months"),
            ("Years", "Years"),
        ],
        default="Months",
    )


class MaintenanceType(models.Model):
    """Maintenance Type Model."""

    _name = "maintenance.type"
    _description = "Vehicle Maintenance Type"

    name = fields.Char("Maintenance Type", required=True)
    main_cost = fields.Boolean(
        "Recurring cost", help="Check if the recurring cost involve"
    )
    cost = fields.Float("Maintenance Cost", help="insert the cost")


class MaintenanceCost(models.Model):
    """Maintenance Cost Model."""

    _name = "maintenance.cost"
    _description = "Vehicle Maintenance Cost"

    maint_type = fields.Many2one("maintenance.type", "Maintenance Type")
    cost = fields.Float("Maintenance Cost", help="insert the cost")
    fleet_rent_id = fields.Many2one("fleet.rent", "Rental Vehicle")
    tenant_id = fields.Many2one(
        related="fleet_rent_id.tenant_id",
        string="Tenant User",
        store=True,
        help="Tenant Name of Rental Vehicle.",
    )
    fleet_tenant_id = fields.Many2one(
        "res.partner", "Fleet Tenant", help="Tenant Name of Rental Vehicle."
    )

    @api.onchange("maint_type")
    def onchange_maint_type(self):
        """Method is used to set maintenance type related.

        Fields value on change of property.
        """
        if self.maint_type:
            self.cost = self.maint_type.cost or 0.00


class TenancyRentSchedule(models.Model):
    """Tenancy Rent Schedule."""

    _name = "tenancy.rent.schedule"
    _description = "Tenancy Rent Schedule"
    _rec_name = "fleet_rent_id"
    _order = "start_date"

    @api.depends("move_id")
    def _compute_get_move_check(self):
        for rent_sched in self:
            rent_sched.move_check = bool(rent_sched.move_id)

    note = fields.Text("Notes", help="Additional Notes.")
    currency_id = fields.Many2one("res.currency", "Currency")
    amount = fields.Monetary(
        default=0.0, currency_field="currency_id", help="Rent Amount."
    )
    start_date = fields.Datetime("Date", help="Start Date.")
    end_date = fields.Date(help="End Date.")
    cheque_detail = fields.Char()
    move_check = fields.Boolean(compute="_compute_get_move_check", store=True)
    rel_tenant_id = fields.Many2one("res.users", "Tenant")
    move_id = fields.Many2one("account.move", "Depreciation Entry")
    vehicle_id = fields.Many2one("fleet.vehicle", "Vehicle", help="Vehicle Name.")
    fleet_rent_id = fields.Many2one(
        "fleet.rent", "Rental Vehicle", help="Rental Vehicle Name."
    )
    paid = fields.Boolean(help="True if this rent is paid by tenant")
    state = fields.Selection(
        [("draft", "Draft"), ("open", "Open"), ("paid", "Paid"), ("cancel", "Cancel")],
        default="draft",
    )
    invc_id = fields.Many2one("account.move", "Invoice")
    inv = fields.Boolean("Is Invoice?")
    pen_amt = fields.Float("Pending Amount", help="Pending Amount.")

    def create_invoice(self):
        """Create invoice for Rent Schedule."""
        self.ensure_one()
        journal_id = self.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        rent = self.fleet_rent_id or False
        vehicle = rent and rent.vehicle_id or False
        if vehicle and not vehicle.income_acc_id:
            msg = _("Please Configure Income Account from Vehicle !!")
            raise UserError(msg)
        inv_line_main = {
            # 'invoice_origin': 'tenancy.rent.schedule',
            "name": "Maintenance cost",
            "price_unit": rent and rent.maintenance_cost or 0.00,
            "quantity": 1,
            "fleet_rent_id": rent.id or False,
        }
        inv_line_values = {
            "name": "Tenancy(Rent) Cost",
            "price_unit": self.amount or 0.00,
            "quantity": 1,
            "fleet_rent_id": rent.id or False,
        }
        inv_values = {
            "partner_id": rent
            and rent.tenant_id
            and rent.tenant_id.partner_id
            and rent.tenant_id.partner_id.id
            or False,
            "move_type": "out_invoice",
            "vehicle_id": vehicle and vehicle.id or False,
            "invoice_date": fields.Date.today() or False,
            "journal_id": journal_id and journal_id.id or False,
            "fleet_rent_id": rent and rent.id or False,
        }
        if self.fleet_rent_id and self.fleet_rent_id.maintenance_cost:
            inv_values.update(
                {"invoice_line_ids": [(0, 0, inv_line_values), (0, 0, inv_line_main)]}
            )
        else:
            inv_values.update({"invoice_line_ids": [(0, 0, inv_line_values)]})
        acc_id = self.env["account.move"].create(inv_values)
        self.write({"invc_id": acc_id.id, "inv": True})
        context = dict(self._context or {})
        wiz_form_id = self.env.ref("account.view_move_form").id

        return {
            "view_type": "form",
            "view_id": wiz_form_id,
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": self.invc_id.id,
            "type": "ir.actions.act_window",
            "target": "current",
            "context": context,
        }

    def open_invoice(self):
        """Method Open Invoice."""
        context = dict(self._context or {})
        wiz_form_id = self.env.ref("account.view_move_form").id
        return {
            "view_type": "form",
            "view_id": wiz_form_id,
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": self.invc_id.id,
            "type": "ir.actions.act_window",
            "target": "current",
            "context": context,
        }

    def create_move(self):
        """
        Button Method is used to create account move.

        @param self: The object pointer.
        """
        move_line_obj = self.env["account.move.line"]
        created_move_ids = []
        journal_ids = self.env["account.journal"].search([("type", "=", "sale")])
        for line in self:
            depreciation_date = fields.Datetime.now()
            company_currency = line.tenancy_id.company_id.currency_id.id
            current_currency = line.tenancy_id.currency_id.id
            sign = -1
            move_vals = {
                "name": line.tenancy_id.ref or False,
                "date": depreciation_date,
                "schedule_date": line.start_date,
                "journal_id": journal_ids and journal_ids.ids[0],
                "asset_id": line.tenancy_id.property_id.id or False,
                "source": line.tenancy_id.name or False,
            }
            move_id = self.env["account.move"].create(move_vals)
            if not line.tenancy_id.property_id.income_acc_id.id:
                msg = _("Please Configure Income Account from Property.")
                raise UserError(msg)
            cond1 = company_currency is not current_currency
            cond2 = -sign * line.tenancy_id.rent
            move_line_obj.create(
                {
                    "name": line.tenancy_id.name,
                    "ref": line.tenancy_id.ref,
                    "move_id": move_id.id,
                    "debit": 0.0,
                    "credit": line.tenancy_id.rent,
                    "journal_id": journal_ids and journal_ids.ids[0],
                    "partner_id": line.tenancy_id.tenant_id.id or False,
                    "currency_id": company_currency != current_currency
                    and current_currency
                    or False,
                    "amount_currency": cond1 and cond2 or 0.0,
                    "date": depreciation_date,
                }
            )
            move_line_obj.create(
                {
                    "name": line.tenancy_id.name,
                    "ref": "Tenancy Rent",
                    "move_id": move_id.id,
                    "credit": 0.0,
                    "debit": line.tenancy_id.rent,
                    "journal_id": journal_ids and journal_ids.ids[0],
                    "partner_id": line.tenancy_id.tenant_id.id or False,
                    "currency_id": company_currency != current_currency
                    and current_currency,
                    "amount_currency": company_currency != current_currency
                    and sign * line.tenancy_id.rent
                    or 0.0,
                    "analytic_account_id": line.tenancy_id.id,
                    "date": depreciation_date,
                    "asset_id": line.tenancy_id.property_id.id or False,
                }
            )
            line.write({"move_id": move_id.id})
            created_move_ids.append(move_id.id)
            move_id.write({"ref": "Tenancy Rent", "state": "posted"})
        return created_move_ids

    @api.model
    def rent_remainder_cron(self):
        """Method to remainder rent."""
        mail_temp_rec = self.env.ref("fleet_rent.email_rent_remainder_template")
        tenancy_rent_recs = self.search(
            [("state", "!=", "paid"), ("start_date", "<=", fields.Datetime.now())]
        )
        if tenancy_rent_recs and mail_temp_rec:
            for pending_rent in tenancy_rent_recs:
                mail_temp_rec.send_mail(pending_rent.id, force_send=True)
##  Prosirenja - lubi

class CarRentalReservationOptions(models.Model):
    _name = 'fleet.rent.options'
    _description = 'Fleet Rental Reservation options'

    @api.onchange("price", "quantity")
    def _compute_option_total_price(self):
        """Method to compute total price."""
        for rent in self:
            rent.total_price = rent.quantity * rent.price
    option = fields.Many2one('product.product', string='Rental options')
  #  option = fields.Char(string="Optional service or equipment")
    price = fields.Float(string="Price for option")
    quantity = fields.Float(string='Qty')
    total_price = fields.Float(string="Total Price")
    fleet_rent_id = fields.Many2one('fleet.rent', string='Rental options')
class CarRentalChecklist(models.Model):
    _name = 'car.fleet.rent.checklist'

    name = fields.Many2one('car.tools', string="Name")
    checklist_active = fields.Boolean(string="Available", default=True)
    fleet_rent_id = fields.Many2one("fleet.rent", "Rental Vehicle")
    price = fields.Float(string="Price")
