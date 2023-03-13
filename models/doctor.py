from odoo import  api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctors"
    _inherit = ['mail.thread',
                'mail.activity.mixin'
               ]
    _rec_name = 'doctor_id'

    doctor_id = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", required=True, default=0, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other') ], required=True, default='male', tracking=True)
    specealization = fields.Many2one('hospital.diseases',string='Specialization' , required=True)
    image = fields.Binary(string='Doctor Image')


    def copy(self, default=None):
        if default is None:
            default={}
        if 'doctor_id' not in default:
            default['doctor_id'] = _("%s (copy)") % (self.doctor_id)
        return super(HospitalDoctor, self).copy(default=default)





