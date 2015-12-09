from openerp import models, api, fields
from datetime import date

#class product_template(models.Model):
#    _inherit = "product.template"
#
#    ntty_url = fields.Char('NTTY URL', size=128, help='NTTY Hiperlink')

class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"
    """
    @api.one
    def _compute_default_lot_year(self):
	year = date.today().year
	return year
    """
    """
    @api.one
    def _compute_assemble_date_code(self):
	year = str(self.lot_year or 1)
	if len(year) > 2:
		year = year[-2:]
	else:
		year = year.zfill(2)
	if self.batch_number:
		batch_number = self.batch_number
	else:
		batch_number = 'N/A'
	self.assemble_date_code = str(self.lot_week or 1).zfill(2) + year + batch_number
    """ # utils

    #leadtime = fields.Integer('Leadtime', default=10, help='Requested leadtime in days.')
    # UTILS units_shipped = fields.Integer('Units Shipped', help='Units Shipped',default=0)
    # UTILS :weight = fields.Float('Weight', help='Weight',default=0)
    #collies = fields.Integer('# Collies', help='# Collies',default=0)
    #units_in_stock = fields.Integer('Units in Stock', help='Units in Stock',default=0)
    # UTILS batch_number = fields.Char('Lot Number', help='Batch Number',size=24,default='N/A')
    #tracking_number = fields.Char('Tracking Number', help='Batch Number',size=12,default='N/A')
    #date_code = fields.Char('Shipping Date', help='Date Code',default='1980/01/01')
    #expiry_date = fields.Char('Expiry Date', help='Expiry Date',default='1980/01/01')
    #UTILS lot_week = fields.Integer('Lot Week', help='Lot Week',default=1)
    #lot_year = fields.Integer('Lot Year', help='Lot Year',default=_compute_default_lot_year)
    # assemble_date_code = fields.Char('Assemble Date Code', help='Assemble Date Code',readonly=True,compute=_compute_assemble_date_code)


class purchase_requisition(models.Model):
    _inherit = 'purchase.requisition'

    template_id = fields.Many2one('purchase.quote.template', 'Quote template')

    @api.one
    def action_purchase_requisition_suppliers(self):
        vals = {}
        sellers = [{'supplier': 1290, 'leadtime': 12}, {'supplier': 579, 'leadtime': 27}]
        vals['product_suppliers'] = [(0, 0, v) for v in sellers]

        wizard = self.env['requisition_suppliers'].create(vals=vals)
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
