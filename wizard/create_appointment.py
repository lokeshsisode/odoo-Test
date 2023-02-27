from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models, _


class CreateAppointment(models.TransientModel):
    _name = "create.appointment"
    _description = "Create Appointment"

    name = fields.Many2one('hospital.patient', string="Name", required=True)
    appointment_datetime = fields.Datetime(string='Date & Time')

    def view_create_appointment_action(self):
        val = {
            'name': self.name.id,
            'appointment_datetime': self.appointment_datetime,
            'gender': self.name.gender,
            'note': self.name.note,
            'doctor_id': self.name.doctor.id,
            # 'diseases_ids': rec.name.exist_diseases_id
        }

        appointment_rec = self.env['hospital.appointment'].create(val)
        return {
            'name': ('Appointment'),
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': appointment_rec.id,
        }








    def view_appointment(self):
        action = self.env.ref('esteem_hospital.appointment_action').read()[0]
        action['domain'] = [('name', '=' , self.name.id)]
        return action
