# -*- coding: utf-8 -*-
# from odoo import http


# class RentomatConfigurator(http.Controller):
#     @http.route('/rentomat_configurator/rentomat_configurator', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rentomat_configurator/rentomat_configurator/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rentomat_configurator.listing', {
#             'root': '/rentomat_configurator/rentomat_configurator',
#             'objects': http.request.env['rentomat_configurator.rentomat_configurator'].search([]),
#         })

#     @http.route('/rentomat_configurator/rentomat_configurator/objects/<model("rentomat_configurator.rentomat_configurator"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rentomat_configurator.object', {
#             'object': obj
#         })
