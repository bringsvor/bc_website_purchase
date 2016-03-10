{
    'name': 'Purchase Quotation Online Proposals',
    'category': 'Website',
    'version': '1.1',
    'description': """
GURBA
=========================

        """,
    #'depends': ['website', 'mail', 'purchase', 'purchase_requisition','product','bc_supplier_certification','elmatica_utils'],
    'depends': ['website', 'mail', 'purchase', 'purchase_requisition','product','bc_supplier_certification'],
    'data': [
        'wizards/request_relevant_suppliers.xml',
        'views/website_quotation.xml',
        'views/website_quotation_backend.xml',
        #'views/report_saleorder.xml',
        'data/website_quotation_data.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        # 'data/website_quotation_demo.xml'
    ],
    'qweb': [
	'static/xml/*.xml',
	'static/src/xml/*.xml'
	],
    'installable': True,
}
