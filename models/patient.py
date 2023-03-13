from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread',
                'mail.activity.mixin'
                ]
    name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", required=True, default=0, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], required=True, tracking=True)
    note = fields.Text(string='Description', required=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'), ('done', 'Done'),
                              ('cancel', 'Cancel')
                              ], default='draft', string='Status', tracking=True)
    patient_refrance_id = fields.Many2one('res.partner', string='Refrance')
    prescription_line_ids = fields.One2many("appointment.prescription.lines", "patient_id", string='prescription lines')
    image = fields.Binary(string='patient Image')
    doctor = fields.Many2one('hospital.doctor', string='Doctor Name', required=True)
    active = fields.Boolean(string="Active", default=False)
    exist_diseases_id = fields.Many2many('hospital.diseases', 'patient_diseases_rel', string='Pre-Exist Diseases')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    def help_redirect_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.odoo.com/documentation/16.0/',
        }


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string='Medicine')
    qty = fields.Integer(string='Quantity')
    patient_id = fields.Many2one('hospital.patient')
    price_unit = fields.Integer(
        string="Unit Price",
        readonly=False, required=True, default=0)
    price_subtotal = fields.Float('Sub Total', readonly=True, compute='_total_price')
    currency_id = fields.Many2one('res.currency', related='patient_id.currency_id')
    total_amount = fields.Monetary(string="Total Amount", store=True, compute='_get_total_amount')

    @api.model
    def _total_price(self):
        for order in self:
            total = 0.0
            total += (order.price_unit * order.qty)
            order.price_subtotal = total

    @api.depends('total_amount', 'price_unit')
    def _get_total_amount(self):
        """Compute the total amounts of the SO."""
