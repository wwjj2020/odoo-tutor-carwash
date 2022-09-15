from odoo import models, api, fields


class Pengelap(models.Model):
    _name = 'carwash.pengelap'
    _description = 'New Description'
    _inherit = 'carwash.pegawai'

    id_pengelap = fields.Char(string='ID Pengelap',required=True)

    cucimobil_ids = fields.Many2many(
        string='Daftar Cuci Mobil',
        comodel_name='carwash.cucimobil'
    )

    total_mobil = fields.Char(compute='_compute_total_mobil', string='Total Mobil')
    
    @api.depends('cucimobil_ids')
    def _compute_total_mobil(self):
        for rec in self:
            ids = self.env['carwash.cucimobil'].search([('pengelap_ids', '=', rec.id)]).mapped('name')
            rec.total_mobil = len(ids)