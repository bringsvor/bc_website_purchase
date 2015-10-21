# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today OpenERP SA (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request
import werkzeug
import datetime
import time
import logging
import base64

from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class purchase_quote(http.Controller):
    @http.route([
        "/purchase/<int:order_id>",
        "/purchase/<int:order_id>/<token>"
    ], type='http', auth="public", website=True)
    def view(self, order_id, token=None, message=False, **post):
        # use SUPERUSER_ID allow to access/view order for public user
        # only if he knows the private token
        user_obj = request.registry.get('res.users')
	user = user_obj.browse(request.cr,token and SUPERUSER_ID or request.uid, request.uid)
	
        order_obj = request.registry.get('purchase.order')
        order = order_obj.browse(request.cr, token and SUPERUSER_ID or request.uid, order_id)
        now = time.strftime('%Y-%m-%d')
	"""
        if token:
            if token != order.access_token:
                return request.website.render('website.404')
            if request.session.get('view_quote',False)!=now:
                request.session['view_quote'] = now
                body=_('Quotation viewed by supplier ')
                self.__message_post(body, order_id, type='comment')
	"""
	
        # if token is None and ( request.uid==user.id and user.active==False ):
        if ( request.uid==user.id and user.active==False ):
        	if request.env.ref('web.login', False):
	               values = request.params.copy() or {}
        	       values["redirect"] = "/purchase/%i" % (order_id);
	               return request.render('web.login', values)

	partner_id = user.partner_id.parent_id.id or user.partner_id.id
	if partner_id and request.uid != SUPERUSER_ID:
		if partner_id != order.partner_id.id:
			return request.website.render('website.404')
	else:
		if request.uid != SUPERUSER_ID:
			return request.website.render('website.404')
	
	
        if request.session.get('view_quote',False)!=now:
        	request.session['view_quote'] = now
       		body=_('Quotation viewed by supplier')
       		self.__message_post(body, order_id, type='comment')

        # If the supplier is viewing this, he has received it. If he has received it it must be sent
        order_obj.signal_workflow(request.cr, SUPERUSER_ID, [order_id], 'send_rfq', context=request.context)

        days = 0
        if order.validity_date:
            days = (datetime.datetime.strptime(order.validity_date, '%Y-%m-%d') - datetime.datetime.now()).days + 1
        values = {
            'quotation': order,
            'message': message and int(message) or False,
            'option': bool(filter(lambda x: not x.line_id, order.options)),
            'order_valid': (not order.validity_date) or (now <= order.validity_date),
            'days_valid': max(days, 0)
        }
        return request.website.render('bc_website_purchase.po_quotation', values)

    # @http.route(['/purchase/accept'], type='json', auth="public", website=True)
    @http.route(['/purchase/<int:order_id>/<token>/accept'], type='http', auth="public", website=True)
    def accept(self, order_id, token=None, signer=None, sign=None, **post):
        order_obj = request.registry.get('purchase.order')
        order = order_obj.browse(request.cr, SUPERUSER_ID, order_id)
        if token != order.access_token:
            return request.website.render('website.404')
        attachments=sign and [('signature.png', sign.decode('base64'))] or []
        order_obj.signal_workflow(request.cr, SUPERUSER_ID, [order_id], 'bid_received', context=request.context)
        message = _('RFQ signed by %s') % (signer,)
        self.__message_post(message, order_id, type='comment', subtype='mt_comment', attachments=attachments)
        return werkzeug.utils.redirect("/purchase/%s" % (order_id))

    @http.route(['/purchase/<int:order_id>/<token>/decline'], type='http', auth="public", website=True)
    def decline(self, order_id, token, **post):
        order_obj = request.registry.get('purchase.order')
        order = order_obj.browse(request.cr, SUPERUSER_ID, order_id)
        if token != order.access_token:
            return request.website.render('website.404')
        request.registry.get('purchase.order').action_cancel(request.cr, SUPERUSER_ID, [order_id])
        message = post.get('decline_message')
        if message:
            self.__message_post(message, order_id, type='comment', subtype='mt_comment')
        return werkzeug.utils.redirect("/purchase/%s/%s?message=2" % (order_id, token))

    @http.route(['/purchase/<int:order_id>/<token>/post'], type='http', auth="public", website=True)
    def post(self, order_id, token, **post):
        # use SUPERUSER_ID allow to access/view order for public user
        order_obj = request.registry.get('purchase.order')
        order = order_obj.browse(request.cr, SUPERUSER_ID, order_id)
        message = post.get('comment')
	ufile = post.get('attachment')
	attachment_ids = []
	kwargs = {}

        if token != order.access_token:
            return request.website.render('website.404')

        if ufile:
            Model = request.session.model('ir.attachment')
            try:
                data_attach = {
                    'name': ufile.filename,
                    'datas': base64.encodestring(ufile.read()),
                    'datas_fname': ufile.filename,
                    'res_model': 'purchase.order',
                    'res_id': int(order_id)
                }
                attachment_id = Model.create( data_attach, request.context)
                args = {
                    'filename': ufile.filename,
                    'id':  attachment_id
                }
                #attachment_ids.append((0, 0, data_attach))
                attachment_ids.append(attachment_id)
                kwargs = { 'attachment_ids': attachment_ids }
            except Exception:
                args = {'error': "Something horrible happened"}
                _logger.exception("Fail to upload attachment %s" % ufile.filename)
                return werkzeug.utils.redirect("/purchase/%s/%s?message=0" % (order_id, token))

        if message:
            self.__message_post(message, order_id, type='comment', subtype='mt_comment',**kwargs)
        return werkzeug.utils.redirect("/purchase/%s/%s?message=1" % (order_id, token))

    # def __message_post(self, message, order_id, type='comment', subtype=False, attachments=[]):
    def __message_post(self, message, order_id, type='comment', subtype=False, **kwargs):
        request.session.body =  message
        cr, uid, context = request.cr, request.uid, request.context
        user = request.registry['res.users'].browse(cr, SUPERUSER_ID, uid, context=context)
        if 'body' in request.session and request.session.body:
            request.registry.get('purchase.order').message_post(cr, SUPERUSER_ID, order_id,
                    body=request.session.body,
                    type=type,
                    subtype=subtype,
                    author_id=user.partner_id.id,
                    context=context,
                    attachments=None,
		    parent_id=False,
		    subject=None,
		    content_subtype='html',
		    **kwargs
                )
            request.session.body = False
        return True

    @http.route(['/purchase/update_line'], type='json', auth="public", website=True)
    # def update_line(self, update_data, **post):
    def update_line(self, **post):
	order_id = post['order_id']
	post_length = len(post['line_id'])
       	order_obj = request.registry.get('purchase.order')
	order = order_obj.browse(request.cr, SUPERUSER_ID or request.uid, order_id)
	if order.state not in ('draft','sent'):
        	return False
	# import pdb;pdb.set_trace()

	for i in range(len(post['line_id'])):	
		line_id = post['line_id'][i]
		try:
			leadtime = post['leadtime'][i]
		except:
			leadtime = 0
			pass
		price_unit = post['price_unit'][i]
		vals = {
			'price_unit': price_unit,
			'leadtime': leadtime,
			}
	        line_id=int(line_id)

        	order_line_obj = request.registry.get('purchase.order.line')
	        order_line_obj.write(request.cr, SUPERUSER_ID, [line_id], vals, context=request.context)
	order_obj.signal_workflow(request.cr, SUPERUSER_ID, [order_id], 'bid_received', context=request.context)
        return True

    @http.route(['/purchase/save'], type='json', auth="public", website=True)
    def save(self, **post):
	order_id = post['order_id']
	post_length = len(post['line_id'])
       	order_obj = request.registry.get('purchase.order')
	order = order_obj.browse(request.cr, SUPERUSER_ID or request.uid, order_id)
	if order.state not in ('draft','sent','confirmed','approved'):
        	return False
	
	for i in range(len(post['line_id'])):	
		line_id = post['line_id'][i]
		try:
			leadtime = post['leadtime'][i]
		except:
			leadtime = 0
			pass
		if order.state in ('draft','sent'):	
			price_unit = post['price_unit'][i]
			vals = {
				'price_unit': price_unit,
				'leadtime': leadtime,
				}
		else:
			vals = {
				'date_code': post['date_code'][i],
				'units_shipped': post['units_shipped'][i],
				'weight': post['weight'][i],
				'collies': post['collies'][i],
				'units_in_stock': post['units_in_stock'][i],
				'batch_number': post['batch_number'][i],
				'tracking_number': post['tracking_number'][i],
				'date_code': post['date_code'][i],
				}
	        line_id=int(line_id)

        	order_line_obj = request.registry.get('purchase.order.line')
	        order_line_obj.write(request.cr, SUPERUSER_ID, [line_id], vals, context=request.context)
	order_obj.write(request.cr,SUPERUSER_ID,[order_id],{'saved': True},context=request.context)
        return True

    @http.route(["/purchase/template/<model('purchase.quote.template'):quote>"], type='http', auth="user", website=True)
    def template_view(self, quote, **post):
        values = { 'template': quote }
        return request.website.render('bc_website_purchase.po_template', values)



