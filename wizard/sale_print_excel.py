from odoo import api, fields, models, _


class CreateExcel(models.TransientModel):
    _name = "create.excel"
    _description = "Create Excel"

    partner_id = fields.Many2many('res.partner', string="Name")
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def create_create_excel_action(self):

        domain = []
        if self.partner_id:
            print(self.partner_id)
            partner_ids = self.partner_id.mapped('id')
            domain += [('order_id.partner_id', 'in', partner_ids)]

        date_from = self.date_from
        if date_from:
            domain += [('create_date', '>=', self.date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('create_date', '<=', self.date_to)]

        sale_order_line = self.env['sale.order.line'].search_read(domain)

        data = {'sale_order_line': sale_order_line}

        return self.env.ref('esteem_hospital.print_excel_report').report_action(self, data=data)
