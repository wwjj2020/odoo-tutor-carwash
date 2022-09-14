from odoo import api, fields, models


class Aksesoris(models.Model):
    _name = 'carwash.aksesoris'
    _description = 'New Description'

    name = fields.Char(string='Nama Barang')
    buy = fields.Integer(string='Harga Modal')
    sell = fields.Integer(string='Harga Jual')
    qty = fields.Integer(string='Stock Barang')