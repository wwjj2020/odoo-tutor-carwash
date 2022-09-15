from odoo import api, fields, models


class Pegawai(models.Model):
    _name = 'carwash.pegawai'
    _description = 'New Description'

    name = fields.Char(string='Nama Pegawai', required=True)
    alamat = fields.Char(string='Alamat Pegawai', required=True)
    tgl_lahir = fields.Date(string='Tanggal Lahir', required=True)
    telp = fields.Char(string='Nomor Telepon', required=True)

