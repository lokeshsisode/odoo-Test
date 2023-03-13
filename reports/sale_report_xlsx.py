from odoo import  api, fields, models, _


class PartnerXlsx(models.AbstractModel):
    _name = 'report.esteem_hospital.print_excel_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):

        sheet = workbook.add_worksheet('sale order')
        bold = workbook.add_format({'bold': True})
        sheet.set_column('C:G',20)
        sheet.set_column('D:D',40)
        sheet.set_column('F:F',35)
        sheet.set_column('L:L',20)

        row=0
        col=0
        sheet.write(row,col,'Order No',bold)
        sheet.write(row,col+1,'customer Name',bold)
        sheet.write(row,col+2,'Date',bold)
        sheet.write(row,col+3,'client',bold)
        sheet.write(row,col+4,'Sale Description',bold)
        sheet.write(row,col+5,'Product',bold)
        sheet.write(row,col+6,'Qty',bold)
        sheet.write(row,col+7,'Price',bold)
        sheet.write(row,col+8,'Subtotal',bold)
        sheet.write(row,col+9,'Tax',bold)
        sheet.write(row,col+10,'Total',bold)
        sheet.write(row,col+11,'Date of updated',bold)

        for data in data['sale_order_line'] :
            row +=1

            # if line['price_unit']== '':
            #     line['price_unit']=0
            #
            # elif data['amount_total'] ==0:
            #     data['amount_total']= line['price_subtotal
            sheet.write(row, col, data['order_id'][0])
            sheet.write(row, col + 1, data['order_id'][1])
            sheet.write(row, col + 2, data['create_date'])
            sheet.write(row, col + 3, data['product_template_id'][1])
            sheet.write(row, col + 4, data['product_template_id'][1])
            sheet.write(row, col + 5, data['product_id'][1])
            sheet.write(row, col + 6, data['product_uom_qty'])
            sheet.write(row, col + 7, data['price_unit'])
            sheet.write(row, col + 8, data['price_subtotal'])
            sheet.write(row, col + 9, data['price_tax'])
            sheet.write(row, col + 10, data['price_total'])
            sheet.write(row, col + 11, data['__last_update'])



















