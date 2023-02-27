from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"


    def write(self,vals):
        user = self.env.user
        if user.has_group('esteem_hospital.group_hospital_manager'):
            super(CrmLead, self).write(vals)
        else:
            raise UserError(_("You don't have permission to modify orders!"))













