 # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager

import logging
_logger = logging.getLogger(__name__)

class CustomerPortal(portal.CustomerPortal):

    # def _prepare_home_portal_values(self, counters):
    #     values = super()._prepare_home_portal_values(counters)
    #     partner = request.env.user.tenant_id
    #
    #     FleetContract = request.env['fleet.rent']
    #     if 'rent_count' in counters:
    #         values['rent_count'] = FleetContract.search_count(self._prepare_carrental_domain(partner)) \
    #             if FleetContract.check_access_rights('read', raise_exception=False) else 0
    #     if 'rent_count' in counters:
    #         values['rent_count'] = FleetContract.search_count(self._prepare_orders_domain(partner)) \
    #             if FleetContract.check_access_rights('read', raise_exception=False) else 0
    #
    #     return values

    def _prepare_home_portal_values(self, counters):
        """Which will set all portal values. And return total events count"""
        values = super()._prepare_home_portal_values(counters)
        if 'rent_count' in counters:
            rent_count = request.env['fleet.rent'].search_count(
                self._get_events_domain()) \
                if request.env['fleet.rent'].check_access_rights('read',
                                                                         raise_exception=False) else 0
            values['rent_count'] = rent_count
        return values

    def _get_events_domain(self):
        """Returns the events that are in stage 'cancel' and 'draft'"""
        return [('state', 'not in', ('open', 'draft'))]


    def _prepare_carrental_domain(self, partner):
        return [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['draft', 'open'])
        ]

    def _prepare_orders_domain(self, partner):
        return [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['open', 'draft'])
        ]

    def _get_sale_searchbar_sortings(self):
        return {
            'date': {'label': _('Order Date'), 'order': 'contract_dt desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

    def _prepare_carrental_portal_rendering_values(
        self, page=1, date_begin=None, date_end=None, sortby=None, quotation_page=False, **kwargs
    ):
        FleetContract = request.env['fleet.rent']
        _logger.info("***************** USAO U _prepare_carrental_portal_rendering_values    Values == %s", FleetContract)

        if not sortby:
            sortby = 'date'

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()

        if quotation_page:
            url = "/my/carrental"
            domain = self._prepare_carrental_domain(partner)
        else:
            url = "/my/carrental_contracts"
            domain = self._prepare_orders_domain(partner)

        searchbar_sortings = self._get_sale_searchbar_sortings()

        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        pager_values = portal_pager(
            url=url,
            total=FleetContract.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
        )
        orders = FleetContract.search(domain, order=sort_order, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            'date': date_begin,
            'carrentals': orders.sudo() if quotation_page else FleetContract,
            'orders': orders.sudo() if not quotation_page else FleetContract,
            'page_name': 'carrent' if quotation_page else 'carrent',
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        _logger.info("*****************     Values == %s", values)
    #    _logger.info("*****************  Generisani URL= %s", values['quotations'][0].get_portal_url())
        return values

    @http.route(['/my/carrental', '/my/carrental/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_carrental(self, **kwargs):
        values = self._prepare_carrental_portal_rendering_values(quotation_page=True, **kwargs)
        request.session['my_carrental_history'] = values['carrentals'].ids[:100]
        _logger.info("Usao u my/carrental     Values == %s", values)
        return request.render("ii_carrental_portal.portal_my_carrental", values)

    @http.route(['/my/carrental_contract', '/my/carrental_contract/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_orders(self, **kwargs):
        values = self._prepare_carrental_portal_rendering_values(quotation_page=False, **kwargs)
        _logger.info("Usao u carrental_contract     Values == %s", values)
        request.session['my_orders_history'] = values['orders'].ids[:100]
        return request.render("ii_carrental_portal.portal_my_carrental", values)

    @http.route(['/my/carrental_contract/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        _logger.info("Usao u carrental_contract    self, orderiid == %s  %s", self, order_id)
        try:
            order_sudo = self._document_check_access('fleet.rent', order_id, access_token=access_token)
            _logger.info("Usao u carrental_contract ORDER SUDO == %s", order_sudo)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='fleet_rent.report_fleet_rent', download=download)
        _logger.info("Usao u carrental_contract NIJE HTML == %s", report_type)
        if request.env.user.share and access_token:
            # If a public/portal user accesses the order with the access token
            # Log a note on the chatter.
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if session_obj_date != today:
                # store the date as a string in the session to allow serialization
                request.session['view_quote_%s' % order_sudo.id] = today
                # The "Quotation viewed by customer" log note is an information
                # dedicated to the salesman and shouldn't be translated in the customer/website lgg
                context = {'lang': order_sudo.user_id.partner_id.lang or order_sudo.company_id.partner_id.lang}
                msg = _('Quotation viewed by customer %s', order_sudo.tenant_id.name)
                del context
                _message_post_helper(
                    "fleet.rent",
                    order_sudo.id,
                    message=msg,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    tenant_ids=order_sudo.tenant_id.sudo().partner_id.ids,
                )

        backend_url = f'/web#model={order_sudo._name}'\
                      f'&id={order_sudo.id}'\
                      f'&action={order_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        values = {
            'sale_order': order_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': order_sudo.company_id,  # Used to display correct company logo
        }
        _logger.info("Usao u carrental_contract backend URL == %s", values)
        _logger.info("Usao u carrental_contract VALUES == %s", values)
        # Payment values
        if order_sudo._has_to_be_paid():
            _logger.info("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB Usao u carrental_contract 0")
            ###################### OVO JE PROBLEM
            ##values.update(self._get_payment_values(order_sudo))
        _logger.info("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB Usao u carrental_contract 1")

        if order_sudo.state in ('draft', 'open', 'cancel'):
            history_session_key = 'my_quotations_history'
        else:
            history_session_key = 'my_orders_history'
        _logger.info("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB Usao u carrental_contract 2")

        values = self._get_page_view_values(
            order_sudo, access_token, values, history_session_key, False)
        _logger.info("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB Usao u carrental_contract 3")

        return request.render('ii_carrental_portal.fleet_rent_portal_template', values)

    def _get_payment_values(self, order_sudo):
        """ Return the payment-specific QWeb context values.

        :param recordset order_sudo: The sales order being paid, as a `fleet.rent` record.
        :return: The payment-specific values.
        :rtype: dict
        """
        logged_in = not request.env.user._is_public()
        providers_sudo = request.env['payment.provider'].sudo()._get_compatible_providers(
            order_sudo.company_id.id,
            order_sudo.tenant_id.id,
            order_sudo.total_rent,
            currency_id=order_sudo.currency_id.id,
            sale_order_id=order_sudo.id,
        )  # In sudo mode to read the fields of providers and partner (if not logged in)
        tokens = request.env['payment.token'].search([
            ('provider_id', 'in', providers_sudo.ids),
            ('tenant_id', '=', order_sudo.tenant_id.id)
        ]) if logged_in else request.env['payment.token']
        # Make sure that the partner's company matches the order's company.
        if not payment_portal.PaymentPortal._can_partner_pay_in_company(
            order_sudo.tenant_id, order_sudo.company_id
        ):
            providers_sudo = request.env['payment.provider'].sudo()
            tokens = request.env['payment.token']
        fees_by_provider = {
            provider: provider._compute_fees(
                order_sudo.total_rent,
                order_sudo.currency_id,
                order_sudo.tenant_id.country_id,
            ) for provider in providers_sudo.filtered('fees_active')
        }
        return {
            'providers': providers_sudo,
            'tokens': tokens,
            'fees_by_provider': fees_by_provider,
            'show_tokenize_input': PaymentPortal._compute_show_tokenize_input_mapping(
                providers_sudo, logged_in=logged_in, sale_order_id=order_sudo.id
            ),
            'amount': order_sudo.total_rent,
            'currency': order_sudo.pricelist_id.currency_id,
            'tenant_id': order_sudo.tenant_id.id,
            'access_token': order_sudo.access_token,
            'transaction_route': order_sudo.get_portal_url(suffix='/transaction'),
            'landing_route': order_sudo.get_portal_url(),
        }

    @http.route(['/my/carrental_contract/<int:order_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            order_sudo = self._document_check_access('fleet.rent', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if not order_sudo._has_to_be_signed():
            return {'error': _('The order is not in a state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            order_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        if not order_sudo._has_to_be_paid():
            order_sudo.action_confirm()
            order_sudo._send_order_confirmation_mail()

        pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('fleet_rent.report_fleet_rent', [order_sudo.id])[0]

        _message_post_helper(
            'fleet.rent',
            order_sudo.id,
            _('Order signed by %s', name),
            attachments=[('%s.pdf' % order_sudo.name, pdf)],
            token=access_token,
        )

        query_string = '&message=sign_ok'
        if order_sudo._has_to_be_paid(True):
            query_string += '#allow_payment=yes'
        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(query_string=query_string),
        }

    @http.route(['/my/carrental_contract/<int:order_id>/decline'], type='http', auth="public", methods=['POST'], website=True)
    def portal_quote_decline(self, order_id, access_token=None, decline_message=None, **kwargs):
        try:
            order_sudo = self._document_check_access('fleet.rent', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if order_sudo._has_to_be_signed() and decline_message:
            order_sudo._action_cancel()
            _message_post_helper(
                'fleet.rent',
                order_sudo.id,
                decline_message,
                token=access_token,
            )
            redirect_url = order_sudo.get_portal_url()
        else:
            redirect_url = order_sudo.get_portal_url(query_string="&message=cant_reject")

        return request.redirect(redirect_url)


class PaymentPortal(payment_portal.PaymentPortal):

    @http.route('/my/carrental_contract/<int:order_id>/transaction', type='json', auth='public')
    def portal_order_transaction(self, order_id, access_token, **kwargs):
        """ Create a draft transaction and return its processing values.

        :param int order_id: The sales order to pay, as a `fleet.rent` id
        :param str access_token: The access token used to authenticate the request
        :param dict kwargs: Locally unused data passed to `_create_transaction`
        :return: The mandatory values for the processing of the transaction
        :rtype: dict
        :raise: ValidationError if the invoice id or the access token is invalid
        """
        # Check the order id and the access token
        try:
            order_sudo = self._document_check_access('fleet.rent', order_id, access_token)
        except MissingError as error:
            raise error
        except AccessError:
            raise ValidationError(_("The access token is invalid."))

        kwargs.update({
            'reference_prefix': None,  # Allow the reference to be computed based on the order
            'tenant_id': order_sudo.tenant_id.id,
            'fleet_rent_id': order_id,  # Include the SO to allow Subscriptions tokenizing the tx
        })
        kwargs.pop('custom_create_values', None)  # Don't allow passing arbitrary create values
        tx_sudo = self._create_transaction(
            custom_create_values={'fleet_rent_ids': [Command.set([order_id])]}, **kwargs,
        )

        return tx_sudo._get_processing_values()

    # Payment overrides

    @http.route()
    def payment_pay(self, *args, amount=None, fleet_rent_id=None, access_token=None, **kwargs):
        """ Override of payment to replace the missing transaction values by that of the sale order.

        This is necessary for the reconciliation as all transaction values, excepted the amount,
        need to match exactly that of the sale order.

        :param str amount: The (possibly partial) amount to pay used to check the access token
        :param str fleet_rent_id: The sale order for which a payment id made, as a `fleet.rent` id
        :param str access_token: The access token used to authenticate the partner
        :return: The result of the parent method
        :rtype: str
        :raise: ValidationError if the order id is invalid
        """
        # Cast numeric parameters as int or float and void them if their str value is malformed
        amount = self._cast_as_float(amount)
        fleet_rent_id = self._cast_as_int(fleet_rent_id)
        if fleet_rent_id:
            order_sudo = request.env['fleet.rent'].sudo().browse(fleet_rent_id).exists()
            if not order_sudo:
                raise ValidationError(_("The provided parameters are invalid."))

            # Check the access token against the order values. Done after fetching the order as we
            # need the order fields to check the access token.
            if not payment_utils.check_access_token(
                access_token, order_sudo.tenant_id.id, amount, order_sudo.currency_id.id
            ):
                raise ValidationError(_("The provided parameters are invalid."))

            kwargs.update({
                'currency_id': order_sudo.currency_id.id,
                'tenant_id': order_sudo.tenant_id.id,
                'company_id': order_sudo.company_id.id,
                'fleet_rent_id': fleet_rent_id,
            })
        return super().payment_pay(*args, amount=amount, access_token=access_token, **kwargs)

    def _get_custom_rendering_context_values(self, fleet_rent_id=None, **kwargs):
        """ Override of payment to add the sale order id in the custom rendering context values.

        :param int fleet_rent_id: The sale order for which a payment id made, as a `fleet.rent` id
        :return: The extended rendering context values
        :rtype: dict
        """
        rendering_context_values = super()._get_custom_rendering_context_values(**kwargs)
        if fleet_rent_id:
            rendering_context_values['fleet_rent_id'] = fleet_rent_id

            # Interrupt the payment flow if the sales order has been canceled.
            order_sudo = request.env['fleet.rent'].sudo().browse(fleet_rent_id)
            if order_sudo.state == 'cancel':
                rendering_context_values['amount'] = 0.0
        return rendering_context_values

    def _create_transaction(self, *args, fleet_rent_id=None, custom_create_values=None, **kwargs):
        """ Override of payment to add the sale order id in the custom create values.

        :param int fleet_rent_id: The sale order for which a payment id made, as a `fleet.rent` id
        :param dict custom_create_values: Additional create values overwriting the default ones
        :return: The result of the parent method
        :rtype: recordset of `payment.transaction`
        """
        if fleet_rent_id:
            if custom_create_values is None:
                custom_create_values = {}
            # As this override is also called if the flow is initiated from sale or website_sale, we
            # need not to override whatever value these modules could have already set
            if 'fleet_rent_ids' not in custom_create_values:  # We are in the payment module's flow
                custom_create_values['fleet_rent_ids'] = [Command.set([int(fleet_rent_id)])]

        return super()._create_transaction(
            *args, fleet_rent_id=fleet_rent_id, custom_create_values=custom_create_values, **kwargs
        )


    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
    #    """
    #         Get a portal url for this model, including access_token.
    #         The associated route must handle the flags for them to have any effect.
    #         - suffix: string to append to the url, before the query string
    #         - report_type: report_type query string, often one of: html, pdf, text
    #         - download: set the download query string to true
    #         - query_string: additional query string
    #         - anchor: string to append after the anchor #
    #     """
         _logger.info("***USAO u GET PORTAL URL    self == %s", self)
         self.ensure_one()
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
    #
    # def _compute_access_url(self):
    #     super()._compute_access_url()
    #     for order in self:
    #         order.access_url = f'/my/carrental/{order.id}'
