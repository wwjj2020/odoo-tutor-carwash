from odoo import models, fields

class DaftarCuciMobil(models.AbstractModel):
    _name = 'report.carwash.report_cucimobil_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, cucimobil):
        # One sheet by partner
        sheet = workbook.add_worksheet('Laporan Cuci Mobil')
        # Menambahkan informasi tanggal laporan
        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(1, 0, 'Nomor Transaksi')
        sheet.write(1, 1, 'Tanggal Transaksi')
        sheet.write(1, 2, 'Plat Mobil')
        sheet.write(1, 3, 'Tipe Mobil')
        sheet.write(1, 4, 'Ukuran Mobil')
        sheet.write(1, 5, 'Harga Cuci')
        sheet.write(1, 6, 'Pencuci Mobil')
        sheet.write(1, 7, 'Pengelap Mobil')
        sheet.write(1, 8, 'Biaya Tambahan')
        sheet.write(1, 9, 'Biaya Total')

        row = 2
        col = 0
        for obj in cucimobil:
            col = 0

            sheet.write(row, col, obj.name)
            sheet.write(row, col + 1, obj.tgl)
            sheet.write(row, col + 2, obj.plat)
            sheet.write(row, col + 3, obj.merek)
            sheet.write(row, col + 4, obj.ukuran)
            sheet.write(row, col + 5, obj.harga)
            sheet.write(row, col + 6, obj.pencuci_id.name)

            for i in obj.pengelap_ids:
                sheet.write(row, col + 7, ', '.join(obj.pengelap_ids.mapped('name')))

            for i in obj.biayatambahan_ids:
                sheet.write(row, col + 8, ', '.join(obj.biayatambahan_ids.aksesoris_id.mapped('name')))

            sheet.write(row, col + 9, obj.total_harga)
                
            row += 1