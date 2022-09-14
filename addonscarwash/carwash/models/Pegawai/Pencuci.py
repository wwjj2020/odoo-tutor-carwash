from odoo import models, api, fields


class Pencuci(models.Model):
    _name = 'carwash.pencuci'
    _description = 'New Description'
    _inherit = 'carwash.pegawai'

    id_pencuci = fields.Char(string='ID Pencuci')
    
    cucimobil_ids = fields.One2many(
        string='cucimobil',
        comodel_name='carwash.cucimobil',
        inverse_name='pencuci_id',
    )
    
    total_mobil = fields.Char(compute='_compute_total_mobil', string='Total Mobil')
    
    @api.depends('cucimobil_ids')
    def _compute_total_mobil(self):
        for rec in self:
            ids = self.env['carwash.cucimobil'].search([('pencuci_id', '=', rec.id)]).mapped('name')
            rec.total_mobil = len(ids)