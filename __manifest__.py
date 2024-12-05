{
    'name': 'Sale Order Delivery Alert',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add possibility to insert lines everywhere on sale order lines',
    'description': """
        Add possibility to insert lines everywhere on sale order lines
    """,
    'author': 'Lapinski Sebastian',
    'depends': [
        'sale_management',
    ],
    'data': [
        "views/sale_order.xml",
        "wizard/insert_line_wizard_view.xml",
        "security/ir.model.access.csv",
    ],
    'license': 'LGPL-3'
}
