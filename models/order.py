from openerp import models, api, fields

#class product_template(models.Model):
#    _inherit = "product.template"
#
#    ntty_url = fields.Char('NTTY URL', size=128, help='NTTY Hiperlink')

class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"

    leadtime = fields.Integer('Leadtime', default=10, help='Requested leadtime in days.')


class purchase_requisition(models.Model):
    _inherit = 'purchase.requisition'

    template_id = fields.Many2one('purchase.quote.template', 'Quote template')

    @api.one
    def action_purchase_requisition_suppliers(self):
        vals = {}
        sellers = [{'supplier': 1290, 'leadtime': 12}, {'supplier': 579, 'leadtime': 27}]
        vals['product_suppliers'] = [(0, 0, v) for v in sellers]

	import  pdb;pdb.set_trace()
        wizard = self.env['requisition_suppliers'].create(vals=vals)
        print "WIZARD CREATED", wizard
        return wizard

        ir_ui_view_osv = self.env['ir.ui.view']
        view_id = ir_ui_view_osv.search(
            [('name', '=', 'view_purchase_requisition_suppliers')]
        )


        return {
            'name' : 'Select supplier wizard',
            'view_type' : 'form',
            'view_mode' : 'form',
            'res_model' : 'requisition_suppliers',
            'res_id' : wizard.id,
            'view_id' : view_id,
            'type' : 'ir.actions.act_window',
            'target' : 'new',
            'context' : self.env.context
        }
