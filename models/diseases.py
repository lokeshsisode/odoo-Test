from odoo import  api, fields, models, _

class diseases(models.Model):
    _name = "hospital.diseases"
    _description = "Diseases"
    _rec_name = 'diseases_id'

    diseases_id = fields.Char(string="Diseases Name", required=True)
    color = fields.Integer('Color Index', default=0)