from odoo import models, fields

class DaftarPencuci(models.AbstractModel):
    _name = 'report.carwash.report_pencuci_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, pencuci):
        # One sheet by partner
        sheet = workbook.add_worksheet('Daftar Pencuci')
        # Menambahkan informasi tanggal laporan
        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(1, 0, 'ID Pencuci')
        sheet.write(1, 1, 'Nama Karyawan')
        sheet.write(1, 2, 'Alamat')
        sheet.write(1, 3, 'Tanggal lahir')
        sheet.write(1, 4, 'Nomor Telepon')
        sheet.write(1, 5, 'Total mobil yang dicuci selama kerja')

        row = 2
        col = 0
        for obj in pencuci:
            col = 0
            sheet.write(row, col, obj.id_pencuci)
            sheet.write(row, col + 1, obj.name)
            sheet.write(row, col + 2, obj.alamat)
            sheet.write(row, col + 3, obj.tgl_lahir)
            sheet.write(row, col + 4, obj.telp)
            sheet.write(row, col + 5, obj.total_mobil)
            row += 1