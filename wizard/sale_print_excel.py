from odoo import  api, fields, models, _

class CreateExcel(models.TransientModel):
    _name = "create.excel"
    _description = "Create Excel"


    fields_id = fields.Many2many('sale.order', string="Name")
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')


    def create_create_excel_action(self):

        domain= []
        if self.fields_id:
            print(self.fields_id)
            order_ids=self.fields_id.mapped('id')
            domain+=[('order_id','in',order_ids)]

        date_from = self.date_from
        if date_from:
            domain += [('create_date', '>=', self.date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('create_date', '<=', self.date_to)]

        # sale_order = self.env['sale.order'].search_read()
        sale_order_line = self.env['sale.order.line'].search_read(domain)


        data = {'sale_order_line':sale_order_line}

        return self.env.ref('esteem_hospital.print_excel_report').report_action(self, data=data)