from odoo import api, fields, models


class Purchase(models.Model):
    _name = 'carwash.purchase'
    _description = 'New Description'

    name = fields.Char(string='Nomor Transaksi')
    tgl = fields.Date(string="Tanggal Transaksi", default=fields.Datetime.now())
    aksesoris_id = fields.Many2one(
        string='Aksesoris',
        comodel_name='carwash.aksesoris'
    )

    harga_satuan = fields.Integer(
        string='Harga Satuan',
        onchange='_onchange_aksesoris_id')

    qty = fields.Integer(string='Jumlah')

    biaya = fields.Integer(compute='_compute_biaya', string='biaya')
    
    @api.depends('harga_satuan', 'qty')
    def _compute_biaya(self):
        for i in self:
            i.biaya = i.harga_satuan * i.qty

    @api.onchange('aksesoris_id')
    def _onchange_aksesoris_id(self):
        self.harga_satuan = self.aksesoris_id.sell
