from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Purchase(models.Model):
    _name = 'carwash.purchase'
    _description = 'New Description'

    name = fields.Char(string='Nomor Transaksi')
    tgl = fields.Date(string="Tanggal Transaksi", default=fields.Datetime.now())
    aksesoris_id = fields.Many2one(
        string='Aksesoris',
        comodel_name='carwash.aksesoris'
    )

    qty = fields.Integer(string='Jumlah')

    biaya = fields.Integer(compute='_compute_biaya', string='biaya')

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
    
    @api.depends('aksesoris_id', 'qty')
    def _compute_biaya(self):
        for i in self:
            i.biaya = i.aksesoris_id.buy * i.qty

    @api.model
    def create(self,vals):
        record = super(Purchase,self).create(vals)
        if record.qty:
            self.env['carwash.aksesoris'].search([('id','=',record.aksesoris_id.id)]).write({'qty' : record.aksesoris_id.qty + record.qty})
        return record

    @api.constrains('qty')
    def check_quantity(self):
        for line in self:
            if line.qty < 1:
                raise ValidationError('Jumlah pembelian harus minimal 1, silahkan input dengan benar!')

    def unlink(self):
        if self.aksesoris_id:
            self.env['carwash.aksesoris'].search([('id','=',self.aksesoris_id.id)]).write({'qty' : self.aksesoris_id.qty - self.qty})

        line = super(Purchase, self).unlink()
    
    _sql_constraints = [
        ('no_nota_unik', 'unique (name)', 'Nomor Nota tidak boleh sama!')
    ]