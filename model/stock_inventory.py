from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class stock_inventory(models.Model):
    _inherit = ['stock.inventory']

    total_value = fields.Float(compute='_compute_value', string="Total value")

    @api.one
    @api.onchange('order_line')
    def _compute_value(self):
        value = 0
        for line in self.line_ids:
            value += round(float(line.value), 2)

        self.total_value = round(float(value), 2)

class stock_inventory_line(models.Model):
    _inherit = ['stock.inventory.line']

    # New field
    value = fields.Float(compute='_compute_value_for_line', string="Value")

    @api.one
    def _compute_value_for_line(self):
        if len(self.product_id.seller_ids) < 1: # Product has no sellers
            self.value = round(float(self.product_id.standard_price * self.product_qty), 2)

        else: # has sellers
            suppliers = self.product_id.seller_ids.sorted(key=lambda r:r.sequence)
            right_supplier = suppliers[0]
            self.value = round(float(right_supplier.price * self.product_qty ), 2)

