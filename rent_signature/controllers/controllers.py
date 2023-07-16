# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class MyModuleController(http.Controller):

    @http.route('/rent_signature/save_signature', type='json', auth='user')
    def save_signature(self, id, signature):
        record = request.env['fleet.rent.signature'].browse(id)
        record.write({'signature': signature})
        return True


# from odoo import http


# class RentSignature(http.Controller):
#     @http.route('/rent_signature/rent_signature', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rent_signature/rent_signature/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rent_signature.listing', {
#             'root': '/rent_signature/rent_signature',
#             'objects': http.request.env['rent_signature.rent_signature'].search([]),
#         })

#     @http.route('/rent_signature/rent_signature/objects/<model("rent_signature.rent_signature"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rent_signature.object', {
#             'object': obj
#         })
