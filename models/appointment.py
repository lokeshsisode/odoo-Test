from odoo import api, fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread',
                'mail.activity.mixin'
                ]

    name = fields.Many2one('hospital.patient', string="Name", required=True, tracking=True)
    note = fields.Text(string='Note')
    age = fields.Integer(string='Age', related='name.age')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'), ('done', 'Done'),
                              ('cancel', 'Cancel')
                              ], default='draft', string='Status', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')])
    appointment_datetime = fields.Datetime(string='Date & Time')
    appointment_count = fields.Integer(string='Appointment_count', compute='_compute_appointment_count')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor Name', required=True)
    diseases_ids = fields.One2many("appointment.exist.diseases",'exist_diseases_id', string='Existing diseases')

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env["hospital.appointment"].search_count([('id', '=', rec.id)])
            self.appointment_count = appointment_count

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.onchange( 'name','gender', 'note','doctor_id')
    def onchange_field(self):
        if self.name:
            if self.name.gender:
                self.gender = self.name.gender
            else:
                self.gender=''

            if self.name.note:
                    self.note = self.name.note
            else:
                self.note= ''

            if self.name.doctor:
                    self.doctor_id = self.name.doctor
            else:
                self.doctor_id= ''

    @api.onchange( 'name' )
    def onchange_id(self):
        values = []
        for rec in self:
            for line in rec.name:
                vals={
                    'name': rec.name,
                    'gender': rec.gender,
                    'diseases_id':rec.name.exist_diseases_id
                }
                values.append((0,0,vals))
            rec.diseases_ids = values

    #  Map,filter,lambda function

    def test_recordset(self):
        for rec in self:
            partners= self.env['res.partner'].search([])
            print('maped partners',partners.mapped('create_date'))
            print('sorted partners',partners.sorted(lambda o:o.name))
            print('filterd partners',partners.filtered(lambda o:o.name=='admin'))





    class AppointmentExistDiseases(models.Model):
        _name = "appointment.exist.diseases"
        _description = "Appointment Exist Diseases"

        name = fields.Many2one('hospital.patient',string='Name')
        gender = fields.Selection([
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')], required=True)
        diseases_id = fields.Many2many('hospital.diseases', string='Exist Diseases')
        exist_diseases_id = fields.Many2one("hospital.appointment",string="Diseases")

