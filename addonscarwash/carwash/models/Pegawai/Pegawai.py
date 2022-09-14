from odoo import api, fields, models


class Pegawai(models.Model):
    _name = 'carwash.pegawai'
    _description = 'New Description'

    name = fields.Char(string='Nama Pegawai')
    alamat = fields.Char(string='Alamat Pegawai')
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    telp = fields.Char(string='Nomor Telepon')

