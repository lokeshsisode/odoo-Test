{
    'name': 'Hospital management',
    'version': '1.0',
    'sequence': -100,
    'category': 'Productivity',
    'summary': 'Hospital management System',
    'description': 'Hospital management System',
    'licenes': 'LGPL-3',
    'depends': ['sale','mail','report_xlsx'],
    'data': [
            'security/ir.model.access.csv',
            'security/hospital_security.xml',
            'security/crm_security.xml',
            'wizard/create_appointment.xml',
            'wizard/sale_print_excel.xml',
            'views/patient.xml',
            'views/doctor.xml',
            'views/appointment.xml',
            'views/diseases.xml',
            'views/kids.xml',
            'views/sale.xml',
            'views/crm.xml',
            'reports/reports_template.xml',
            'reports/reports.xml',


    ],
    'installable': True,
    'application': True,

}
