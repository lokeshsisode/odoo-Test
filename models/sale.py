from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    sale_description = fields.Char(string="Sale Description")


class add_no_of_employee(models.Model):
    _inherit = "hr.department"
    no_of_employee = fields.Many2one('hr.employee', string='No of Employee')
