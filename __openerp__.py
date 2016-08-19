{
    'name': "Stock valuation improved",
    'version': '9.0.1.0',
    'depends': ['stock'],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Stock',
    'description': 
    """
    This modules adds the product prices value in the inventory adjustments.

    It takes the supplier purchase price for each product or the simple purchase price and computes the value for each lines of the inventoty ajustment.
    """,
    'data': [
        'view/view_inventory_form.xml',
        'report/stock_inventory.xml'
    ],
}
