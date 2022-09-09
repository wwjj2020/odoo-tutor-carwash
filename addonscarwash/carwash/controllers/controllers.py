# -*- coding: utf-8 -*-
# from odoo import http


# class Carwash(http.Controller):
#     @http.route('/carwash/carwash', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/carwash/carwash/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('carwash.listing', {
#             'root': '/carwash/carwash',
#             'objects': http.request.env['carwash.carwash'].search([]),
#         })

#     @http.route('/carwash/carwash/objects/<model("carwash.carwash"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('carwash.object', {
#             'object': obj
#         })
