from odoo import models, fields

class DaftarAksesoris(models.AbstractModel):
    _name = 'report.carwash.report_aksesoris_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, aksesoris):
        # One sheet by partner
        sheet = workbook.add_worksheet('Daftar aksesoris')
        # Menambahkan informasi tanggal laporan
        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(1, 0, 'Nama Barang')
        sheet.write(1, 1, 'Harga Modal')
        sheet.write(1, 2, 'Harga Jual')
        sheet.write(1, 3, 'Stok Barang')

        row = 2
        col = 0
        for obj in aksesoris:
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col + 1, obj.buy)
            sheet.write(row, col + 2, obj.sell)
            sheet.write(row, col + 3, obj.qty)
            row += 1