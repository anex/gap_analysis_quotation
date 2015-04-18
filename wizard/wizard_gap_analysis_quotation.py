from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_gap_analysis_quotation(osv.osv_memory):
    _name = 'wizard.gap_analysis.quotation'

    _columns = {
      'product_id': fields.many2one('product.product', 'Product', help='Product', required=True),
      'product_uom': fields.many2one('product.uom', 'Product Uom', help='Product Uom', required=True),
      'include_workloads': fields.boolean('Include Workloads?', help='Include Workloads as Order Lines?'),
    }

    _defaults = {
      'product_id': lambda obj, cr, uid, context: obj.pool.get('gap_analysis.quotation.conf').get_quotation_product(cr, uid, context=context),
    }

    def action_apply(self, cr, uid, ids, context=None):
        """
        Convert gap_analysis to Sale Order Quotation
        """
        if context is None:
            context = {}

        gap_obj = self.pool.get('gap_analysis')

        data = self.browse(cr, uid, ids, context=context)[0]

        return gap_obj.gap_to_quotation(
                                        cr,
                                        uid,
                                        context.get('active_id'),
                                        data.product_id.id,
                                        data.product_uom.id,
                                        data.include_workloads,
                                        context=context
                                       )

wizard_gap_analysis_quotation()
