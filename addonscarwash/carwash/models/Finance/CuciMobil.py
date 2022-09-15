from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CuciMobil(models.Model):
    _name = 'carwash.cucimobil'
    _description = 'New Description'

    name = fields.Char(string='Nomor Transaksi', required=True)
    tgl = fields.Date(string="Tanggal Transaksi", default=fields.Datetime.now())
    plat = fields.Char(string='Plat Mobil', required=True)
    merek = fields.Char(string='Tipe Mobil')

    _sql_constraints = [
        ('no_nota_unik', 'unique (name)', 'Nomor Nota tidak boleh sama!')
    ]
    
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

    biayatambahan_ids = fields.One2many(
        comodel_name='carwash.biayatambahan', 
        inverse_name='cucimobil_id', 
        string='Biaya Tambahan')

    total_harga = fields.Integer(compute='_compute_total_harga', string='total_harga')

    state = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('confirm', 'Confirm'),
                   ('done', 'Done'),
                   ('cancelled', 'Cancelled'),
                   ],
        required=True, readonly=True, default='draft')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})
    
    @api.depends('biayatambahan_ids', 'harga')
    def _compute_total_harga(self):
        for i in self:
            i.total_harga = sum(i.biayatambahan_ids.mapped('total')) + i.harga
            

    @api.onchange('ukuran')
    def _onchange_ukuran(self):
        if self.ukuran == 'small':
            self.harga = 40000
        elif self.ukuran == 'med':
            self.harga = 45000
        elif self.ukuran == 'big':
            self.harga = 50000
    
    def unlink(self):
        if self.biayatambahan_ids:
            penjualan = []
            for line in self:
                penjualan = self.env['carwash.biayatambahan'].search([('cucimobil_id', '=', line.id)])

            for ob in penjualan:
                ob.aksesoris_id.qty += ob.qty

        line = super(CuciMobil, self).unlink()
    
    def write(self, vals):
      for line in self:
          real_data = self.env['carwash.biayatambahan'].search([('cucimobil_id', '=', line.id)])

          for data in real_data:
              data.aksesoris_id.qty += data.qty
      
      line = super(CuciMobil, self).write(vals)
      
      for line in self:
          edited_data = self.env['carwash.biayatambahan'].search([('cucimobil_id', '=', line.id)])

          for new_data in edited_data:
              if new_data in real_data:
                  new_data.aksesoris_id.qty -= new_data.qty
              else:
                  pass

      return line
            
class BiayaTambahan(models.Model):
    _name = 'carwash.biayatambahan'
    _description = 'New Description'

    name = fields.Char(string='Name')

    cucimobil_id = fields.Many2one(
        string='detail',
        comodel_name='carwash.cucimobil',
    )

    aksesoris_id = fields.Many2one(
        string='Aksesoris',
        comodel_name='carwash.aksesoris'
    )

    harga_satuan = fields.Integer(
        string='Harga Satuan',
        onchange='_onchange_aksesoris_id')

    qty = fields.Integer(string="Jumlah")

    total = fields.Integer(compute='_compute_total', string='total')
    
    @api.depends('harga_satuan', 'qty')
    def _compute_total(self):
        for i in self:
            i.total = i.qty * i.harga_satuan
    
    @api.onchange('aksesoris_id')
    def _onchange_aksesoris_id(self):
        if self.aksesoris_id.sell:
            self.harga_satuan = self.aksesoris_id.sell

    @api.model
    def create(self,vals):
        record = super(BiayaTambahan,self).create(vals)
        if record.qty:
            self.env['carwash.aksesoris'].search([('id','=',record.aksesoris_id.id)]).write({'qty' : record.aksesoris_id.qty - record.qty})
        return record

    @api.constrains('qty')
    def check_quantity(self):
        for line in self:
            if line.qty < 1:
                raise ValidationError('Jumlah pembelian harus minimal 1, silahkan input dengan benar!')
            elif line.aksesoris_id.qty < line.qty:
                raise ValidationError('Stok yang tersedia tidak mencukupi.')
    

    
