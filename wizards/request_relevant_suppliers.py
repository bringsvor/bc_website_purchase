__author__ = 'tbri'
from openerp import fields, models, api, _
import logging

_logger = logging.getLogger(__name__)

class request_relevant_suppliers(models.TransientModel):
    _name = "requisition_suppliers"
    _description = "Purchase Requisition Suppliers"

    def _get_active_id(self):
        return self.env.context.get('active_id', False)

    name = fields.Char('What?')
    tender = fields.Many2one('purchase.requisition', 'CallForBitds',  default=lambda self: self._get_active_id())
    numsupp = fields.Integer('Number of suppliers', compute='_get_numsupp')
    product_suppliers = fields.One2many('relevant_supplierinfo', 'relevant_suppliers',
        string='Suppliers')

    """
    @api.depends('tender')
    def onchange_tender(self):
        print "ONCHANGE_TENDER"
        if self.tender:
            sellers = [{'supplier': 1290, 'leadtime': 12}, {'supplier': 579, 'leadtime': 27}]
            self.product_suppliers = [(0, 0, v) for v in sellers]
            _logger.info('product_suppliers onchange %s', self.product_suppliers)
    """

    @api.one
    def _get_numsupp(self):
        self.numsupp = len(self.product_suppliers)

    @api.one
    def _comp_product_suppliers(self):
        sellers = [{'supplier': 1290, 'leadtime': 12}, {'supplier': 579, 'leadtime': 27}]
        self.product_suppliers = [(0, 0, v) for v in sellers]
        return sellers


    @api.v7
    def Xdefault_get(self, cr, uid, fields_list=None, context=None):
        dg = self.xxdefault_get(cr, uid)
        print "DEFAULT GET V7", dg
        return dg[0]

    @api.one
    def xxdefault_get(self):
        vals = {}
        _logger.info(' CONTEXT %s', self.env.context)
        active_id = self.env.context['active_id']
        tender = self.env['purchase.requisition'].browse(active_id)
        products = [line.product_id for line in tender.line_ids]

        sellers = []
        for product in products:
            for seller in product.seller_ids:
                _logger.info('CREATING SELLER %s',seller.name.name)

                #supp = self.env['bc_website_purchase.relevant.supplierinfo'].create(
                #    {'supplier' : seller.name.id,
                #                                 'leadtime' : seller.delay,
                #                                 'relevant_suppliers' : self.id
                #    }
                #)
                info = {'supplier' : seller.name.id,
                        'leadtime' : seller.delay,
                        #'relevant_suppliers' : self.id
                         }
                _logger.info('About to create %s', info)
                #self.product_suppliers = [(0,0, info)]
                sellers.append(info)
                _logger.info('SUPP %s', sellers)

        #self.product_suppliers = [(0, 0, v) for v in sellers]

        vals['product_suppliers'] = [(0, 0, v) for v in sellers]
        return vals


    def default_get(self, cr, uid, fields_list=None, context=None):
        val = {}
        active_id = context['active_id']
        tender = self.pool('purchase.requisition').browse(cr, uid, [active_id])
        products = [line.product_id for line in tender.line_ids]
        sellers = []
        for product in products:
            for seller in product.seller_ids:
                info = {'name' : seller.name.id,
                        'leadtime' : seller.delay,
                        #'relevant_suppliers' : self.id
                         }
                _logger.info('About to create %s', info)
                # do not add existing sellers
                if info not in sellers:
                    sellers.append(info)


        #sellers = [{'supplier': 1290, 'leadtime': 12}, {'supplier': 579, 'leadtime': 27}]
        val['product_suppliers'] = [(0, 0, v) for v in sellers]
        return val


    def Xview_init(self, cr, uid, fields, context=None):
        res = super(request_relevant_suppliers, self).view_init(cr, uid, fields, context)
        _logger.info(' %s VIEW INIT CONTEXT %s', res, context)
        active_id = context['active_id']
        tender = self.pool('purchase.requisition').browse(cr, uid, [active_id])
        products = [line.product_id for line in tender.line_ids]

        for product in products:
            for seller in product.seller_ids:
                _logger.info('%s CREATING SELLER %s',fields, seller.name.name)

                #supp = self.env['bc_website_purchase.relevant.supplierinfo'].create(
                #    {'supplier' : seller.name.id,
                #                                 'leadtime' : seller.delay,
                #                                 'relevant_suppliers' : self.id
                #    }
                #)
                info = {'name' : seller.name.id,
                        'leadtime' : seller.delay,
                        'relevant_suppliers' : self.id
                         }
                _logger.info('About to create %s', info)
                self.product_suppliers = [(0,0, info)]
                _logger.info('SUPP %s', self.product_suppliers)

        if not tender.line_ids:
            raise Warning(_('Error'), _('Define product(s) you want to include in the call for bids.'))

        return res

    @api.one
    def create_order(self):
        _logger.info('create_order in request_relevant_suppliers')
        active_id = self.env.context['active_id']
        _logger.info('create_order active_id %s' % active_id)
        tender = self.env['purchase.requisition'].browse(active_id)
	sso = self.env['super.sales.order'].browse([tender.sso_id.id])
        prods = self.env['relevant_supplierinfo'].search([('relevant_suppliers','=',self.id)])
        _logger.info('create_order %s %s', self.id, prods)

        for si in prods:
            supplierinfo = si.read(['name', 'leadtime'])[0]

            _logger.info('create_order %s %s', tender, supplierinfo['name'])
            si_leadtime = supplierinfo['leadtime']
            rfq_id = tender.make_purchase_order(supplierinfo['name'][0])
            _logger.info('create_order rfq %s', rfq_id)
	    dict_products_leadtimes = {}
	    for order_line in sso.order_line:
		dict_products_leadtimes[order_line.product_id.id] = order_line.delay
            for rfq in rfq_id.values():
                # not great but
                po = self.env['purchase.order'].search([('id', '=', rfq)])
                po.write({'template_id': tender.template_id.id})
                lines = self.env['purchase.order.line'].search([('order_id','=',rfq)])
		for po_line in lines:
			if po_line.product_id.id in dict_products_leadtimes.keys():
				leadtime = dict_products_leadtimes[po_line.product_id.id]
			else:
				leadtime = si_leadtime
			if po_line.product_id.default_code == 'SETUP':
                		po_line.write({'leadtime' : leadtime,'product_qty': 0})
			else:
	                	po_line.write({'leadtime' : leadtime})

        return {'type': 'ir.actions.act_window_close'}

    """
    def view_init(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        res = super(purchase_requisition_partner, self).view_init(cr, uid, fields_list, context=context)
        record_id = context and context.get('active_id', False) or False
        tender = self.pool.get('purchase.requisition').browse(cr, uid, record_id, context=context)
        if not tender.line_ids:
            raise osv.except_osv(_('Error!'), _('Define product(s) you want to include in the call for bids.'))
        return res

    def create_order(self, cr, uid, ids, context=None):
        active_ids = context and context.get('active_ids', [])
        data =  self.browse(cr, uid, ids, context=context)[0]
        self.pool.get('purchase.requisition').make_purchase_order(cr, uid, active_ids, data.partner_id.id, context=context)
        return {'type': 'ir.actions.act_window_close'}
    """

class relevant_supplierinfo(models.TransientModel):
    _name = 'relevant_supplierinfo'

    # Basically a transient version of product.supplierinfo

    relevant_suppliers = fields.Many2one('requisition_suppliers')
    name = fields.Many2one('res.partner', 'Supplier')
    leadtime = fields.Integer('Leadtime', help='Time from confirmed order to receipt of goods.')
