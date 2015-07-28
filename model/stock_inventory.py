from openerp import models, fields, api

class stock_inventory(models.Model):
    _inherit = ['stock.inventory']

    total_value = fields.Float(compute='_compute_value', string="Total value")

    @api.one
    @api.onchange('order_line')
    def _compute_value(self):
        cr = self.env.cr
        uid = self.env.user.id

        value = 0

        inventory_line_obj = self.pool.get('stock.inventory.line')
        inventory_lines = inventory_line_obj.search(cr, uid, [('inventory_id', '=', self.id)])
        if inventory_lines:
            for inventory_line in inventory_line_obj.browse(cr, uid, inventory_lines):
                value += inventory_line.value

        self.total_value = value

class stock_inventory_line(models.Model):
    _inherit = ['stock.inventory.line']

    # New field
    value = fields.Float(compute='_compute_value_for_line', string="Value")

    @api.one
    def _compute_value_for_line(self):
        cr = self.env.cr
        uid = self.env.user.id

        if self.product_id.seller_id.id: # Product has sellers
            # get supplier info
            obj = self.pool.get('product.supplierinfo')
            supplier_info = obj.search(cr, uid, [('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)])
            if supplier_info and supplier_info[0]:
                right_supplier = obj.browse(cr, uid, supplier_info[0])
                for val in obj.browse(cr, uid, supplier_info):
                    if val.sequence < right_supplier.sequence:
                        right_supplier = val
                pricelist_partnerinfo_obj = self.pool.get('pricelist.partnerinfo')
                pricelist_partnerinfos = pricelist_partnerinfo_obj.search(cr, uid, [('suppinfo_id', '=', right_supplier.id)])
                if pricelist_partnerinfos:
                    computed_cost_price = 0
                    if pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).min_quantity == 0:
                        computed_cost_price = pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).price
                    else:
                        computed_cost_price = pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).price / pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).min_quantity
                    self.value = computed_cost_price * self.product_qty
                else:
                    self.value = self.product_id.standard_price * self.product_qty     #error
            else:
                self.value = self.product_id.standard_price * self.product_qty     #error
        else:
            self.value = self.product_id.standard_price * self.product_qty    
