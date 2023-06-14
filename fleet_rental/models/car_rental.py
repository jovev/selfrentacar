# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.irvas.rs>).
#    Author: Lubi @IRVAS (odoo@irvas.rs)
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

from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo import Command
from odoo.exceptions import UserError, Warning, ValidationError
import logging
import re
from bs4 import BeautifulSoup
regex = re.compile(r'<[^>]+>')
_logger = logging.getLogger(__name__)


def remove_html(string):
    return regex.sub('', string)
def pars_html_table(data):
    soup = BeautifulSoup(data, 'html.parser')

 #####   Obrada prve tabele   ############################3
    table = soup.find_all('table')[0]  # Grab the first table
    _logger.info('****PARS HTML-TABLE ********** selektovana = %s', table)
    my_dic = {}
    my_dic_opt = {}
    option_lines = []
    t1_col_name = ['Customer Details','Reservation code', 'Customer', 'Date of Birth', 'Street Address', 'City', 'Flight number','Country', 'Phone', 'Email', 'Additional Comments' ]
    t2_col_name = ['Customer Details', 'Reservation code', 'Customer', 'Date of Birth', 'Street Address', 'City',
                   'Flight number', 'Country', 'Phone', 'Email', 'Additional Comments']

    # Collecting Ddata
    row_no = 0
    for row in table.find_all('tr'):
        # Find all data for each column
        columns = row.find_all('td')
        #    print (columns)
        if (columns != []):
            kolona1 = columns[0].text.strip()
            _logger.info('****PARS HTML-TABLE ********** kolona1 = %s', kolona1)
    #        print(kolona1)
            if kolona1 == "Customer Details" or kolona1 == "Detalji o korisniku":
                kolona2 = "BLANK"
            else:
                kolona2 = columns[1].text.strip()
    #        print(kolona2)
            _logger.info('****PARS HTML-TABLE ********** kolona2 = %s', kolona2)
        #    my_dic[kolona1] = kolona2
            my_dic[t1_col_name[row_no]] = kolona2
    #        df = pd.concat([df, pd.DataFrame([kolona1, kolona2])], ignore_index=True)
            row_no = row_no + 1
 #    Kraj obrade prve tabele   ###################
    table = soup.find_all('table')[1]  # Grab the second table
    _logger.info('****PARS HTML-TABLE ********** selektovana = %s', table)
    my_dic_t2 = {}
    t2_col_name = ['Rental Details', 'Detalji najma', 'Rent from', 'Lokacija preuzimanja','Return Location', 'Lokacija vracaanja', 'Pick-up Date & Time', 'Datum i vrijeme preuzimanja',
                   'Return Date & Time','Datum i vrijeme vraćanja', 'Period', 'Selected Cars', 'Price','Cijena', 'Total', 'Rental Options','Opcije najma']
    # Collecting Ddata
    row_no = 0
    last_col_name = "0"
    for row in table.find_all('tr'):
        # Find all data for each column
        columns = row.find_all('td')
        #    print (columns)
        last_col_name = kolona1
        if (columns != []):
            kolona1 = columns[0].text.strip()
            _logger.info('****PARS HTML-TABLE ********** kolona1 = %s', kolona1)
            #        print(kolona1)
            if kolona1 == "Rental Details" or kolona1 == "Detalji najma":
                kolona2 = "BLANK"
                kolona3 = "BLANK"
                continue
            if kolona1 == "Rent from" or kolona1 == "Lokacija preuzimanja":
                kolona2 = columns[0].text.strip()
                kolona3 = columns[1].text.strip()
            #    my_dic_t2['Rent from'] = kolona2
            #    my_dic_t2['Return location'] = kolona3
                continue
            if kolona1 == "Pick-up Date & Time" or kolona1 == "Datum i vrijeme preuzimanja":
                kolona1 = columns[0].text.strip()
            #    kolona2 = columns[1].text.strip()
            #    kolona3 = columns[2].text.strip()
            #    my_dic_t2['Pick-up Date & Time'] = kolona2
            #    my_dic_t2['Return Date & Time'] = kolona3
            #    my_dic_t2['Period'] = kolona2
                continue
            if kolona1 == "Selected Cars" or kolona1 == "Izaberi vozila":
                kolona1 = columns[0].text.strip()
                kolona2 = columns[1].text.strip()
                kolona3 = columns[2].text.strip()
            #    my_dic_t2['Selected Cars'] = kolona1
            #    my_dic_t2['Price'] = kolona2
            #    my_dic_t2['Total'] = kolona3
                continue
            if kolona1 == "Rental Options" or kolona1 == "Opcije najma":
                kolona1 = columns[0].text.strip()
                kolona2 = "BLANK"
                kolona3 = "BLANK"
                redni_broj_opcije = 1    # pocinemo da brojimo opcije
                continue
            if kolona1 == "Total":
                kolona1 = columns[0].text.strip()
                kolona2 = "BLANK"
                kolona3 = "BLANK"
                continue

            if last_col_name == "Rent from" or last_col_name == "Lokacija preuzimanja":
                kolona1 = columns[0].text.strip()
                kolona2 = columns[1].text.strip()
                my_dic['Rent from'] = kolona1
                my_dic['Return location'] = kolona2

            if last_col_name == "Pick-up Date & Time" or last_col_name == "Datum i vrijeme preuzimanja":
                kolona1 = columns[0].text.strip()
                kolona2 = columns[1].text.strip()
                kolona3 = columns[2].text.strip()
                my_dic['Pick-up Date & Time'] = kolona1
                my_dic['Return Date & Time'] = kolona2

            if last_col_name == "Selected Cars" or last_col_name == "Izaberi vozila":
                kolona1 = columns[0].text.strip()
                kolona2 = columns[1].text.strip()
                kolona3 = columns[2].text.strip()
                my_dic['Selected Cars'] = kolona1
                my_dic['Rent Price'] = kolona2

            if last_col_name == "Rental Options" or last_col_name == "Opcije najma":
                kolona1 = columns[0].text.strip()
                kolona2 = columns[1].text.strip()
                kolona3 = columns[2].text.strip()
                option = "option" + str(redni_broj_opcije)
                price = "price" + str(redni_broj_opcije)
                tprice = "tprice" + str(redni_broj_opcije)
                option_content = "{'option':" + kolona1 + ",'price':" + kolona2 + ",'total_price':" + kolona3 +"}"
                option_lines.append(Command.create(option_content))
                my_dic_opt[option] = option_content
               # my_dic_opt[price] = kolona2
               # my_dic_opt['tprice'] = kolona3
                kolona1 = last_col_name
                redni_broj_opcije = redni_broj_opcije + 1


            #else:
            #    kolona2 = columns[1].text.strip()
            #        print(kolona2)
            _logger.info('****PARS HTML-TABLE ********** kolona2 = %s', kolona2)
            #    my_dic[kolona1] = kolona2
            # my_dic_t2[t1_col_name[row_no]] = kolona2
            #        df = pd.concat([df, pd.DataFrame([kolona1, kolona2])], ignore_index=True)
            row_no = row_no + 1
    #    Kraj obrade druge tabele   ###################
    _logger.info('***************  Dictionart TABELE 2 = %s', my_dic)
    return my_dic, my_dic_opt


class CarRentalReservation(models.Model):
    _name = 'car.rental.reservation'
    _description = 'Fleet Rental Management Reservation'
    _inherit = 'mail.thread'
    # customer details
    name = fields.Char(string="Name", default="Draft Reservation", readonly=True, copy=False)
    customer_name = fields.Char(required=True, string='Customer', help="Customer")
    reservation_code = fields.Char(string="Reservation Code", copy=False)
    date_of_birth = fields.Char(string="Date of Birth")
    street_address = fields.Char(string="Street Address")
    city = fields.Char(string="City")
    flight_number = fields.Char(string="Flight number")
    country = fields.Char(string="Country")
    phone = fields.Char(string="Phone")
    cemail = fields.Char(string="Email")   #customer email
    additional_comments = fields.Text(string="Additional Comments")
  # Polja vezana za neposredno rentiranje
    rent_from = fields.Char(string="Rent From")
    return_location = fields.Char(string="Return_location")
    rent_start_date = fields.Datetime(string="Rent Start Date", required=True, help="Start date of rent", track_visibility='onchange')
    rent_end_date = fields.Datetime(string="Rent End Date", required=True, help="End date of contract", track_visibility='onchange')
    selected_cars = fields.Char(string="Selected Cars")     # Ovo je u stvari spisak vozila u odredjenoj
    rent_price = fields.Char(string="Rent price for car")
    grand_price = fields.Char(string="Total price for car rent and options")

    state = fields.Selection(
        [('draft', 'Draft'), ('reserved', 'Reserved'), ('running', 'Running'), ('cancel', 'Cancel'),
         ('checking', 'Checking'), ('invoice', 'Invoice'), ('done', 'Done')], string="State",
        default="draft", copy=False, track_visibility='onchange')
    option_lines = fields.One2many('car.rental.reservation.options', 'rental_options', readonly=True, help="Selected Rental options",
                                   copy=False)


    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        # _logger.INFO("msg %s, custom_values= %s", msg, custom_values)
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        #_logger.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! self= %s, msg %s, custom_values= %s', self, msg, custom_values)
        email_body = msg['body']
        # skidamo HTM tagove
        #clear_tekst = remove_html(email_body)[98:]
        #_logger.info('***************  Goli tekst = %s', clear_tekst)
        # Parsiramo body emaila
        #reserv_parameters = pars_reservation_body(clear_tekst)
        reserv_parameters, my_dic_opt = pars_html_table(email_body)



        _logger.info('***************  Parametri Posle Parsiranja = %s', reserv_parameters)
        _logger.info('***************  Opcije Posle Parsiranja = %s', my_dic_opt)
        # string = option_lines[0] + "," + option_lines[1]

        # stomer = reserv_parameters['Customer'] or erv_parameters['Customer']

        # Ova polja treba napuniti iz sadrzaja emaila.
        create_context = dict(self.env.context or {})
        create_context['default_user_ids'] = False


        if custom_values is None:
            custom_values = {'name': msg.get('subject') or _("No Subject"),
                             'customer_name': reserv_parameters['Customer'],
                             'reservation_code':reserv_parameters['Reservation code'],
                             'date_of_birth': reserv_parameters['Date of Birth'],
                             'street_address': reserv_parameters['Street Address'],
                             'city': reserv_parameters['City'],
                             'flight_number': reserv_parameters['Flight number'],
                             'country': reserv_parameters['Country'],
                             'phone': reserv_parameters['Phone'],
                             'cemail': reserv_parameters['Email'],
                             'additional_comments': reserv_parameters['Additional Comments'],
                             'rent_from': reserv_parameters['Rent from'],
                             'return_location': reserv_parameters['Return location'],
                         #    'rent_start_date': reserv_parameters['Pick-up Date & Time'],
                         #    'rent_end_date': reserv_parameters['Return Date & Time'],
                             'selected_cars': reserv_parameters['Selected Cars'],
                             'rent_price': reserv_parameters['Rent Price'],

                             #    'grand_price': reserv_parameters['Grand Price'],
                             'option_lines': [Command.create(my_dic_opt['option1']),Command.create(my_dic_opt['option2']), Command.create(my_dic_opt['option3']) ],


                             }
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
                             'customer_name': "Ime i przime kupca",
                             'reservation_code': "R000000000",
                             'date_of_birth': "1900-01-01",
                             'city': "Belgrade",
                             'flight_number': "Enter FN",
                             'country': "Serbia",
                             'phone': "063461420",
                             'cemail': "info@example.com",
                             'additional_comments': "No additional comments",
                             'rent_from': "Belgrade",
                             'return_location': "Belgrade",
                             'rent_start_date': "2023-01-01",
                             'rent_end_date': "2023-01-02",
                             'selected_cars': "VW Golf 7-Automatic, Wagon-New Car, Station Wagon, New Renault Megan - Automatic- Vagon",
                              'rent_price': "1.0",
                             'grand_price': "1.0",

                            'option_lines': [Command.create(my_dic_opt['option1']),Command.create(my_dic_opt['option2']), Command.create(my_dic_opt['option3']) ],

        }
        defaults.update(custom_values)
        _logger.info('!!!!!!! DEFAULTS Pre upisa ubazu= %s   Custom value =%s', defaults, custom_values)

        rent = super(CarRentalReservation, self.with_context(create_context)).message_new(msg, custom_values=defaults)
        #     email_list = rent.email_split(msg)
        #     partner_ids = [p.id for p in self.env['mail.thread']._mail_find_partner_from_emails(email_list, records=rent,
        #                                                                                        force_create=False) if p]
        #    rent.message_subscribe(partner_ids)
        # sada pripremamo detalje opcije
        #defaults["option_lines"] = []
        #defaults_line_vals = self._prepare_option_line(l, lines[l])

        #invoice_vals["invoice_line_ids"].append(Command.create(invoice_line_vals))
        return rent

    def action_confirm(self):
        if self.rent_end_date < self.rent_start_date:
            raise ValidationError("Please select the valid end date.")

        customers = self.env['res.partner'].search([('email', '=', self.cemail)])
        countries = self.env['res.country'].search([('name', '=', self.country)])
        country_id=""
        for country in countries:
          country_id = country.id
        if customers:
            for customer in customers:
                customer_name = customer.name
                customer_id = customer
        else:   # Znaci, korisnik ne postoji , idemo u proces kreiranja novog korisnika u respartner
            values = {
                'name': self.customer_name,
                'email': self.cemail,
                'phone': self.phone,
                'is_company': '0',
                'street': self.street_address,
                'city': self.city,
                'country_id': country_id,
            }
            customer_id = self.env['res.partner'].create(values)

        start_locations = self.env['stock.location'].search([('name','=',self.rent_from)])
        if start_locations:
            for start_location in start_locations:
                location_start_id = start_location.id
        else:
            location_start_id = '18'

        end_locations = self.env['stock.location'].search([('name', '=', self.return_location)])
        if end_locations:
            for end_location in end_locations:
                location_end_id = end_location.id
        else:
            location_end_id = '18'
        self.state = "checking"

        car_categories = self.env['fleet.vehicle.model.category'].search([('name', '=', self.selected_cars)])
        if car_categories:
            for car_category in car_categories:
                car_category_id = car_category.id
        else:
            car_category_id = '1'

        values = {
                         'customer_id': customer_id.id,
                         'rent_start_date': self.rent_start_date,
                         'rent_end_date': self.rent_end_date,
                         'reservation_code': self.reservation_code,
                         'notes': self.additional_comments,
                         'rent_from': location_start_id,
                         'return_location': location_end_id ,
                         'web_car_request': self.selected_cars,
                         'total': self.grand_price,
                        'state':'draft',
                        'cost':self.rent_price,
                        'first_payment':'0.0',
                         }
        self.env['car.rental.contract'].create(values)


    #    raise ValidationError("Kreiranje nije jos zavrseno . Ovo je samo test akcije")

    def action_cancel(self):
        self.state = "cancel"


class CarRentalReservationOptions(models.Model):
    _name = 'car.rental.reservation.options'
    _description = 'Fleet Rental Management Reservation options'
    option = fields.Char(string="Service option")
    price = fields.Char(string="Price for option")
    total_price = fields.Char(string="Total Price for option")
    rental_options = fields.Many2one('car.rental.reservation', string='Rental options')


class CarRentalContract(models.Model):
    _name = 'car.rental.contract'
    _description = 'Fleet Rental Management'
    _inherit = 'mail.thread'

    @api.onchange('rent_start_date', 'rent_end_date')
    def check_availability(self):
        self.vehicle_id = ''
        fleet_obj = self.env['fleet.vehicle'].search([])
        for i in fleet_obj:
            for each in i.rental_reserved_time:

                if str(each.date_from) <= str(self.rent_start_date) <= str(each.date_to):
                    i.write({'rental_check_availability': False})
                elif str(self.rent_start_date) < str(each.date_from):
                    if str(each.date_from) <= str(self.rent_end_date) <= str(each.date_to):
                        i.write({'rental_check_availability': False})
                    elif str(self.rent_end_date) > str(each.date_to):
                        i.write({'rental_check_availability': False})
                    else:
                        i.write({'rental_check_availability': True})
                else:
                    i.write({'rental_check_availability': True})

    image = fields.Binary(related='vehicle_id.image_128', string="Image of Vehicle")
    reserved_fleet_id = fields.Many2one('rental.fleet.reserved', invisible=True, copy=False)
    name = fields.Char(string="Name", default="Draft Contract", readonly=True, copy=False)
    customer_id = fields.Many2one('res.partner', required=True, string='Customer', help="Customer")
    web_car_request = fields.Char(string="Required car model, class, ..")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=False, help="Vehicle",
                                 readonly=True,
                                 states={'draft': [('readonly', False)]}
                                 )

    driver_id1 = fields.Many2one('res.partner', string="Driver 1")
    driver1_passport_no = fields.Char(string="Passport No", related='driver_id1.ref')
    driver1_driver_licence_no = fields.Char(string="Licence No", related='driver_id1.d_id')
    driver_id2 = fields.Many2one('res.partner', string="Driver 2", )
    driver2_passport_no = fields.Char(string="Passport No", related='driver_id2.ref')
    driver2_driver_licence_no = fields.Char(string="Licence No", related='driver_id2.d_id')
    plate = fields.Char(string="Vehicle Plate", related='vehicle_id.license_plate')
    car_brand = fields.Many2one('fleet.vehicle.model.brand', string="Fleet Brand", size=50,
                                related='vehicle_id.model_id.brand_id', store=True, readonly=True)

    car_color = fields.Char(string="Fleet Color", size=50, related='vehicle_id.color', store=True, copy=False,
                            default='#FFFFFF', readonly=True)
    cost = fields.Float(string="Rent Cost", help="This fields is to determine the cost of rent", required=False)
    rent_start_date = fields.Datetime(string="Rent Start Date", required=True, default=str(date.today()),
                                  help="Start date of contract", track_visibility='onchange')
    rent_end_date = fields.Datetime(string="Rent End Date", required=True, help="End date of contract",
                                track_visibility='onchange')
    state = fields.Selection(
        [('draft', 'Draft'), ('reserved', 'Reserved'), ('running', 'Running'), ('cancel', 'Cancel'),
         ('checking', 'Checking'), ('invoice', 'Invoice'), ('done', 'Done')], string="State",
        default="draft", copy=False, track_visibility='onchange')
    notes = fields.Text(string="Details & Notes")
    cost_generated = fields.Float(string='Recurring Cost',
                                  help="Costs paid at regular intervals, depending on the cost frequency")
    cost_frequency = fields.Selection([('no', 'No'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'),
                                       ('yearly', 'Yearly')], string="Recurring Cost Frequency",
                                      help='Frequency of the recurring cost', required=False)
    journal_type = fields.Many2one('account.journal', 'Journal',
                                   default=lambda self: self.env['account.journal'].search([('id', '=', 1)]))
    account_type = fields.Many2one('account.account', 'Account',
                                   default=lambda self: self.env['account.account'].search([('id', '=', 17)]))
    recurring_line = fields.One2many('fleet.rental.line', 'rental_number', readonly=True, help="Recurring Invoices",
                                     copy=False)
    first_payment = fields.Float(string='First Payment',
                                 help="Transaction/Office/Contract charge amount, must paid by customer side other "
                                      "than recurrent payments",
                                 track_visibility='onchange',
                                 required=True)
    first_payment_inv = fields.Many2one('account.move', copy=False)
    first_invoice_created = fields.Boolean(string="First Invoice Created", invisible=True, copy=False)
    attachment_ids = fields.Many2many('ir.attachment', 'car_rent_checklist_ir_attachments_rel',
                                      'rental_id', 'attachment_id', string="Attachments",
                                      help="Images of the vehicle before contract/any attachments")
    checklist_line = fields.One2many('car.rental.checklist', 'checklist_number', string="Checklist",
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
    invoice_count = fields.Integer(compute='_invoice_count', string='# Invoice', copy=False)
    check_verify = fields.Boolean(compute='check_action_verify', copy=False)
    sales_person = fields.Many2one('res.users', string='Sales Person', default=lambda self: self.env.uid,
                                   track_visibility='always')
    selected_cars_class = fields.Many2one('fleet.vehicle.model.category', string='Car Category')

    rent_from = fields.Many2one('stock.location', string='Start location')
    rent_from_longitude = fields.Float(string="GPS X", related='rent_from.location_longitude')
    rent_from_longitude = fields.Float(string="GPS Y", related='rent_from.location_latitude')
   # rent_from_key_position = fields.Char(string="Key Position", related='stock.location.location_position')

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

    def action_run(self):
        self.state = 'running'

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

    @api.constrains('rent_start_date', 'rent_end_date')
    def validate_dates(self):
        if self.rent_end_date < self.rent_start_date:
            raise ValidationError("Please select the valid end date.")

    def set_to_done(self):
        invoice_ids = self.env['account.move'].search([('invoice_origin', '=', self.name)])
        f = 0
        for each in invoice_ids:
            if each.payment_state != 'paid':
                f = 1
                break
        if f == 0:
            self.state = 'done'
        else:
            raise UserError("Some Invoices are pending")

    def _invoice_count(self):
        invoice_ids = self.env['account.move'].search([('invoice_origin', '=', self.name)])
        self.invoice_count = len(invoice_ids)

    @api.constrains('state')
    def state_changer(self):
        if self.state == "running":
            state_id = self.env.ref('fleet_rental.vehicle_state_rent').id
            self.vehicle_id.write({'state_id': state_id})
        elif self.state == "cancel":
            state_id = self.env.ref('fleet_rental.vehicle_state_active').id
            self.vehicle_id.write({'state_id': state_id})
        elif self.state == "invoice":
            self.rent_end_date = fields.Date.today()
            state_id = self.env.ref('fleet_rental.vehicle_state_active').id
            self.vehicle_id.write({'state_id': state_id})

    @api.constrains('checklist_line', 'damage_cost')
    def total_updater(self):
        total = 0.0
        tools_missing_cost = 0.0
        for records in self.checklist_line:
            total += records.price
            if not records.checklist_active:
                tools_missing_cost += records.price
        self.total = total
        self.tools_missing_cost = tools_missing_cost
        self.damage_cost_sub = self.damage_cost
        self.total_cost = tools_missing_cost + self.damage_cost

    def fleet_scheduler1(self, rent_date):
        inv_obj = self.env['account.move']
        inv_line_obj = self.env['account.move.line']
        recurring_obj = self.env['fleet.rental.line']
        start_date = datetime.strptime(str(self.rent_start_date), '%Y-%m-%d').date()
        end_date = datetime.strptime(str(self.rent_end_date), '%Y-%m-%d').date()
        supplier = self.customer_id
        inv_data = {
            'ref': supplier.name,
            'partner_id': supplier.id,
            'invoice_origin': self.name,
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
        recurring_data = {
            'name': self.vehicle_id.name,
            'date_today': rent_date,
            'account_info': income_account.name,
            'rental_number': self.id,
            'recurring_amount': self.cost_generated,
            'invoice_number': inv_id.id,
            'invoice_ref': inv_id.id,
        }
        recurring_obj.create(recurring_data)
        inv_line_data = {
            'name': self.vehicle_id.name,
            'account_id': income_account.id,
            'price_unit': self.cost_generated,
            'quantity': 1,
            'product_id': product_id.id,
            'move_id': inv_id.id,
        }
        inv_line_obj.update(inv_line_data)
        mail_content = _(
            '<h3>Reminder Recurrent Payment!</h3><br/>Hi %s, <br/> This is to remind you that the '
            'recurrent payment for the '
            'rental contract has to be done.'
            'Please make the payment at the earliest.'
            '<br/><br/>'
            'Please find the details below:<br/><br/>'
            '<table><tr><td>Contract Ref<td/><td> %s<td/><tr/>'
            '<tr/><tr><td>Amount <td/><td> %s<td/><tr/>'
            '<tr/><tr><td>Due Date <td/><td> %s<td/><tr/>'
            '<tr/><tr><td>Responsible Person <td/><td> %s, %s<td/><tr/><table/>') % \
                       (self.customer_id.name, self.name, inv_id.amount_total, inv_id.invoice_date_due,
                        inv_id.user_id.name,
                        inv_id.user_id.mobile)
        main_content = {
            'subject': "Reminder Recurrent Payment!",
            'author_id': self.env.user.partner_id.id,
            'body_html': mail_content,
            'email_to': self.customer_id.email,
        }
        self.env['mail.mail'].create(main_content).send()

    @api.model
    def fleet_scheduler(self):
        inv_obj = self.env['account.move']
        inv_line_obj = self.env['account.move.line']
        recurring_obj = self.env['fleet.rental.line']
        today = date.today()
        for records in self.search([]):
            start_date = datetime.strptime(str(records.rent_start_date), '%Y-%m-%d').date()
            end_date = datetime.strptime(str(records.rent_end_date), '%Y-%m-%d').date()
            if end_date >= date.today():
                temp = 0
                if records.cost_frequency == 'daily':
                    temp = 1
                elif records.cost_frequency == 'weekly':
                    week_days = (date.today() - start_date).days
                    if week_days % 7 == 0 and week_days != 0:
                        temp = 1
                elif records.cost_frequency == 'monthly':
                    if start_date.day == date.today().day and start_date != date.today():
                        temp = 1
                elif records.cost_frequency == 'yearly':
                    if start_date.day == date.today().day and start_date.month == date.today().month and \
                            start_date != date.today():
                        temp = 1
                if temp == 1 and records.cost_frequency != "no" and records.state == "running":
                    supplier = records.customer_id
                    inv_data = {
                        'ref': supplier.name,
                        'partner_id': supplier.id,
                        'currency_id': records.account_type.company_id.currency_id.id,
                        'journal_id': records.journal_type.id,
                        'invoice_origin': records.name,
                        'company_id': records.account_type.company_id.id,
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
                    recurring_data = {
                        'name': records.vehicle_id.name,
                        'date_today': today,
                        'account_info': income_account.name,
                        'rental_number': records.id,
                        'recurring_amount': records.cost_generated,
                        'invoice_number': inv_id.id,
                        'invoice_ref': inv_id.id,
                    }
                    recurring_obj.create(recurring_data)
                    inv_line_data = {
                        'name': records.vehicle_id.name,
                        'account_id': income_account.id,
                        'price_unit': records.cost_generated,
                        'quantity': 1,
                        'product_id': product_id.id,
                        'move_id': inv_id.id,

                    }
                    inv_line_obj.update(inv_line_data)
                    mail_content = _(
                        '<h3>Reminder Recurrent Payment!</h3><br/>Hi %s, <br/> This is to remind you that the '
                        'recurrent payment for the '
                        'rental contract has to be done.'
                        'Please make the payment at the earliest.'
                        '<br/><br/>'
                        'Please find the details below:<br/><br/>'
                        '<table><tr><td>Contract Ref<td/><td> %s<td/><tr/>'
                        '<tr/><tr><td>Amount <td/><td> %s<td/><tr/>'
                        '<tr/><tr><td>Due Date <td/><td> %s<td/><tr/>'
                        '<tr/><tr><td>Responsible Person <td/><td> %s, %s<td/><tr/><table/>') % \
                                   (self.customer_id.name, self.name, inv_id.amount_total, inv_id.invoice_date_due,
                                    inv_id.user_id.name,
                                    inv_id.user_id.mobile)
                    main_content = {
                        'subject': "Reminder Recurrent Payment!",
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': self.customer_id.email,
                    }
                    self.env['mail.mail'].create(main_content).send()
            else:
                if self.state == 'running':
                    records.state = "checking"

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

    def action_confirm(self):
        if self.rent_end_date < self.rent_start_date:
            raise ValidationError("Please select the valid end date.")
        check_availability = 0
        for each in self.vehicle_id.rental_reserved_time:
            if each.date_from <= self.rent_start_date <= each.date_to:
                check_availability = 1
            elif self.rent_start_date < each.date_from:
                if each.date_from <= self.rent_end_date <= each.date_to:
                    check_availability = 1
                elif self.rent_end_date > each.date_to:
                    check_availability = 1
                else:
                    check_availability = 0
            else:
                check_availability = 0
        if check_availability == 0:
            reserved_id = self.vehicle_id.rental_reserved_time.create({'customer_id': self.customer_id.id,
                                                                       'date_from': self.rent_start_date,
                                                                       'date_to': self.rent_end_date,
                                                                       'reserved_obj': self.vehicle_id.id
                                                                       })
            self.write({'reserved_fleet_id': reserved_id.id})
        else:
            raise Warning('Sorry This vehicle is already booked by another customer')
        self.state = "reserved"
        sequence_code = 'car.rental.sequence'
        order_date = self.create_date
        order_date = str(order_date)[0:10]
        self.name = self.env['ir.sequence'] \
            .with_context(ir_sequence_date=order_date).next_by_code(sequence_code)
        mail_content = _('<h3>Order Confirmed!</h3><br/>Hi %s, <br/> This is to notify that your rental contract has '
                         'been confirmed. <br/><br/>'
                         'Please find the details below:<br/><br/>'
                         '<table><tr><td>Reference Number<td/><td> %s<td/><tr/>'
                         '<tr><td>Time Range <td/><td> %s to %s <td/><tr/><tr><td>Vehicle <td/><td> %s<td/><tr/>'
                         '<tr><td>Point Of Contact<td/><td> %s , %s<td/><tr/><table/>') % \
                       (self.customer_id.name, self.name, self.rent_start_date, self.rent_end_date,
                        self.vehicle_id.name, self.sales_person.name, self.sales_person.mobile)
        main_content = {
            'subject': _('Confirmed: %s - %s') %
                       (self.name, self.vehicle_id.name),
            'author_id': self.env.user.partner_id.id,
            'body_html': mail_content,
            'email_to': self.customer_id.email,
        }
        self.env['mail.mail'].create(main_content).send()

    def action_cancel(self):
        self.state = "cancel"
        if self.reserved_fleet_id:
            self.reserved_fleet_id.unlink()

    def force_checking(self):
        self.state = "checking"

    def action_view_invoice(self):
        inv_obj = self.env['account.move'].search([('invoice_origin', '=', self.name)])
        inv_ids = []
        for each in inv_obj:
            inv_ids.append(each.id)
        view_id = self.env.ref('account.view_move_form').id
        if inv_ids:
            if len(inv_ids) <= 1:
                value = {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'account.move',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': _('Invoice'),
                    'res_id': inv_ids and inv_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', inv_ids)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'account.move',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name': _('Invoice'),
                }

            return value

    def action_invoice_create(self):
        for each in self:
            rent_date = self.rent_start_date
            if each.cost_frequency != 'no' and rent_date < date.today():
                rental_days = (date.today() - rent_date).days
                if each.cost_frequency == 'weekly':
                    rental_days = int(rental_days / 7)
                if each.cost_frequency == 'monthly':
                    rental_days = int(rental_days / 30)
                for each1 in range(0, rental_days + 1):
                    if rent_date > datetime.strptime(str(each.rent_end_date), "%Y-%m-%d").date():
                        break
                    each.fleet_scheduler1(rent_date)
                    if each.cost_frequency == 'daily':
                        rent_date = rent_date + timedelta(days=1)
                    if each.cost_frequency == 'weekly':
                        rent_date = rent_date + timedelta(days=7)
                    if each.cost_frequency == 'monthly':
                        rent_date = rent_date + timedelta(days=30)

        if self.first_payment != 0:
            self.first_invoice_created = True
            inv_obj = self.env['account.move']
            inv_line_obj = self.env['account.move.line']
            supplier = self.customer_id
            inv_data = {
                'ref': supplier.name,
                'move_type': 'out_invoice',
                'partner_id': supplier.id,
                'currency_id': self.account_type.company_id.currency_id.id,
                'journal_id': self.journal_type.id,
                'invoice_origin': self.name,
                'company_id': self.account_type.company_id.id,
                'invoice_date_due': self.rent_end_date,
            }
            inv_id = inv_obj.create(inv_data)
            self.first_payment_inv = inv_id.id
            product_id = self.env['product.product'].search([("name", "=", "Fleet Rental Service")])
            if product_id.property_account_income_id.id:
                income_account = product_id.property_account_income_id.id
            elif product_id.categ_id.property_account_income_categ_id.id:
                income_account = product_id.categ_id.property_account_income_categ_id.id
            else:
                raise UserError(
                    _('Please define income account for this product: "%s" (id:%d).') % (product_id.name,
                                                                                         product_id.id))

            if inv_id:
                list_value = [(0, 0, {
                    'name': self.vehicle_id.name,
                    'price_unit': self.first_payment,
                    'quantity': 1.0,
                    'account_id': income_account,
                    'product_id': product_id.id,
                    'move_id': inv_id.id,
                })]
                inv_id.write({'invoice_line_ids': list_value})
            mail_content = _(
                '<h3>First Payment Received!</h3><br/>Hi %s, <br/> This is to notify that your first payment has '
                'been received. <br/><br/>'
                'Please find the details below:<br/><br/>'
                '<table><tr><td>Invoice Number<td/><td> %s<td/><tr/>'
                '<tr><td>Date<td/><td> %s <td/><tr/><tr><td>Amount <td/><td> %s<td/><tr/><table/>') % (
                           self.customer_id.name, inv_id.payment_reference, inv_id.invoice_date, inv_id.amount_total)
            main_content = {
                'subject': _('Payment Received: %s') % inv_id.payment_reference,
                'author_id': self.env.user.partner_id.id,
                'body_html': mail_content,
                'email_to': self.customer_id.email,
            }
            self.env['mail.mail'].create(main_content).send()
            imd = self.env['ir.model.data']
            action = self.env.ref('account.action_move_out_invoice_type')
            result = {
                'name': action.name,
                'type': 'ir.actions.act_window',
                'views': [[False, 'form']],
                'target': 'current',
                'res_id': inv_id.id,
                'res_model': 'account.move',
            }
            return result

        else:
            raise ValidationError("Please enter advance amount to make first payment")

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        #_logger.INFO("msg %s, custom_values= %s", msg, custom_values)
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        _logger.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! self= %s, msg %s, custom_values= %s', self, msg, custom_values)
        create_context = dict(self.env.context or {})
        create_context['default_user_ids'] = False
        if custom_values is None:
            custom_values = {'name': msg.get('subject') or _("No Subject"),
            'cost': 1.0,
            'customer_id': 7,
            'first_payment': 1.0,
            'rent_end_date': "2023-03-10",
            'rent_start_date': "2023-03-09",
            'vehicle_id': 1,
           }
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
             'cost': 1.0,
            'customer_id': 7,
            'first_payment': 1.0,
            'rent_end_date': "2023-03-10",
            'rent_start_date': "2023-03-09",
            'vehicle_id': 1,

        }
        defaults.update(custom_values)

        rent = super(CarRentalContract, self.with_context(create_context)).message_new(msg, custom_values=defaults)
        #     email_list = rent.email_split(msg)
        #     partner_ids = [p.id for p in self.env['mail.thread']._mail_find_partner_from_emails(email_list, records=rent,
        #                                                                                        force_create=False) if p]
        #    rent.message_subscribe(partner_ids)
        return rent


class FleetRentalLine(models.Model):
    _name = 'fleet.rental.line'

    name = fields.Char('Description')
    date_today = fields.Date('Date')
    account_info = fields.Char('Account')
    recurring_amount = fields.Float('Amount')
    rental_number = fields.Many2one('car.rental.contract', string='Rental Number')
    payment_info = fields.Char(compute='paid_info', string='Payment Stage', default='draft')
    invoice_number = fields.Integer(string='Invoice ID')
    invoice_ref = fields.Many2one('account.move', string='Invoice Ref')
    date_due = fields.Date(string='Due Date', related='invoice_ref.invoice_date_due')

    def paid_info(self):
        for each in self:
            if self.env['account.move'].browse(each.invoice_number):
                each.payment_info = self.env['account.move'].browse(each.invoice_number).state
            else:
                each.payment_info = 'Record Deleted'


class CarRentalChecklist(models.Model):
    _name = 'car.rental.checklist'

    name = fields.Many2one('car.tools', string="Name")
    checklist_active = fields.Boolean(string="Available", default=True)
    checklist_number = fields.Many2one('car.rental.contract', string="Checklist Number")
    price = fields.Float(string="Price")

    @api.onchange('name')
    def onchange_name(self):
        self.price = self.name.price


class CarTools(models.Model):
    _name = 'car.tools'

    name = fields.Char(string="Name")
    price = fields.Float(string="Price")
