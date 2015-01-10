# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from datetime import datetime
from tools.translate import _

class gap_analysis(osv.osv):
    _inherit = 'gap_analysis'

    def gap_to_quotation(self, cr, uid, ids, context=None):
        sale_order_obj = self.pool.get('sale.order')
        sale_order_line_obj = self.pool.get('sale.order.line')

        gap_quot_conf_obj = self.pool.get('gap_analysis.quotation.conf')
        gap_quot_product = gap_quot_conf_obj.get_quotation_product(cr, uid, context=context)

        gap = self.browse(cr, uid, ids, context=context)[0]

        if not gap.partner_id:
            raise osv.except_osv(_('Error'), _('Must be add a Partner to Generate Quotation'))
        elif not gap.gap_lines:
            raise osv.except_osv(_('Error'), _("Must be add Functionalities to Generate Quotation"))

        order_name = "%s %s" % (gap.reference, gap.name)

        vals = {
            'name': order_name,
            'partner_id': gap.partner_id.id,
            'partner_invoice_id': gap.partner_id.id,
            'partner_shipping_id': gap.partner_id.id,
            'date_order': datetime.now(),
            'client_order_ref': gap.reference,
            'user_id': context.get('uid'),
            'pricelist_id': 1,
        }

        so_defaults = sale_order_obj.default_get(
                                         cr,
                                         uid,
                                         [
                                          'picking_policy',
                                          'order_policy'
                                         ],
                                         context=context
                                     )

        vals.update(so_defaults)

        order_id = sale_order_obj.search(cr, uid, [('name', '=', order_name)], context=context)

        if order_id:
            order_id = order_id[0]
            sale_order_obj.write(cr, uid, order_id, vals, context=context)
            order_lines = sale_order_line_obj.search(cr, uid, [('order_id', '=', order_id)], context=context)
            sale_order_line_obj.unlink(cr, uid, order_lines, context=context)
        else:
            order_id = sale_order_obj.create(cr, uid, vals, context=context)

        for gap_line in gap.gap_lines:
            line_vals = {
                'product_id': gap_quot_product,
                'name': gap_line.functionality.name,
                'price_unit': gap_line.total_cost, 
                'order_id': order_id,
            }

            sol_defaults = sale_order_line_obj.default_get(
                                             cr,
                                             uid,
                                             [
                                                'product_uom_qty',
                                             ],
                                             context=context
                                         )

            line_vals.update(sol_defaults)

            line_id = sale_order_line_obj.create(cr, uid, line_vals, context=context)

        return True
gap_analysis()

class gap_analysis_quotation_conf(osv.osv):
    _name = 'gap_analysis.quotation.conf'

    def get_quotation_product(self, cr, uid, context=None):
        record = self.search(cr, uid, [], context=context)

        if not record:
            raise osv.except_osv(_('Error'), _('Product template not defined on Gap Analysis Configuration'))

        return self.browse(cr, uid, record[0], context=context).product_id.id

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', select=1, required=False),
    }
gap_analysis_quotation_conf()
