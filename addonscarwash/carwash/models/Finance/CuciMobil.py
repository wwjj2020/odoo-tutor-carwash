from email.policy import default
from re import S
from odoo import api, fields, models


class CuciMobil(models.Model):
    _name = 'carwash.cucimobil'
    _description = 'New Description'

    name = fields.Char(string='Nomor Transaksi')
    tgl = fields.Date(string="Tanggal Transaksi", default=fields.Datetime.now())
    plat = fields.Char(string='Plat Mobil')
    merek = fields.Char(string='Tipe Mobil')
    
    ukuran = fields.Selection(
        string='Ukuran Mobil',
        selection=[('small', 'Kecil'), 
                   ('med', 'Sedang'),
                   ('big', 'Besar')
                   ]
    )

    harga = fields.Integer('Harga Cuci')
    
    pencuci_id = fields.Many2one(
        string='Pencuci Mobil',
        comodel_name='carwash.pencuci',
        ondelete='cascade',
    )

    pengelap_ids = fields.Many2many(
        string='Pengelap Mobil',
        comodel_name='carwash.pengelap'
    )    

    @api.onchange('ukuran')
    def _onchange_ukuran(self):
        if self.ukuran == 'small':
            self.harga = 40000
        elif self.ukuran == 'med':
            self.harga = 45000
        elif self.ukuran == 'big':
            self.harga = 50000

    

    
