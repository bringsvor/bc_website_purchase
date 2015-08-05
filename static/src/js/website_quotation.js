$(function () {
'use strict';
var website = openerp.website;
var color = $('#btnSubmit').css('background-color');
$('.columnID').css("visibility","hidden");
$('#quotation_id').css("visibility","hidden");

website.ready().done( function() {
    $('.bc_attachment_url').each( function( index, element ) {
        var attachment_id = $(element).attr("attachment_id");
        var message_id =  $(element).attr("message_id");
        console.log("attachment_id:",attachment_id);
        console.log("message_id:",message_id);
        console.log("openerp:",website);
        var url = openerp.website.session.url('/mail/download_attachment', {
                'model': 'mail.message',
                'id': message_id,
                'method': 'download_attachment',
                'attachment_id': attachment_id
            });
    //        var url = "empty";
        console.log("url:",url);
        $(element).attr("href", url);
    });
} );



var formChanged = true;
$(".update_line.js_unitprice.input-group").each(function(index,element) {
	$(element).numericInput({
		allowFloat: true, // Accpets positive numbers (floating point)
		allowNegative: false // Accpets positive or negative integer
	});
        if ( !($(element).val())){
		formChanged = false;
		}
});

$(".update_line.js_leadtime.input-group").each(function(index,element) {
        var control_var = isNaN($(element).val());
	console.log(control_var);
        if ( !$(element).val() ){
		formChanged = false;
		}
	});
if (formChanged == false) {
	$('#btnSave').addClass('disabled');
	$('#btnSave').prop('disabled', true);
	$('#btnSubmit').addClass('disabled');
	$('#btnSubmit').prop('disabled', true);
	}

website.if_dom_contains('div.o_bc_website_purchase', function () {

     
   $('.update_line.js_unitprice.input-group').on('keydown',function(event){
        // event.preventDefault();
   	formChanged = true;
	// $('#btnSave').css('background-color','#f0ad4e');
	$('#btnSave').removeClass('disabled');
	$('#btnSubmit').removeClass('disabled');
	$('#btnSave').prop('enabled',true);
	$('#btnSubmit').prop('enabled',true);
	return true;
   });

 
   $('.update_line.js_leadtime.input-group').on('keydown',function(event){
	if (event.keyCode >= 48 && event.keyCode <= 57 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 13) {
		formChanged = true;
		// $('#btnSave').css('background-color','#f0ad4e');
		$('#btnSave').removeClass('disabled');
		$('#btnSubmit').removeClass('disabled');
		$('#btnSave').prop('enabled',true);
		$('#btnSubmit').prop('enabled',true);
		return true;
		}
	else {
		return false;
		}
	});

   $('#btnCalc').hide();

   // Click on the submit button
   $('#btnSave').on('click', function (ev) {
	console.log('Clicked Save Button');
	if (formChanged == false) {
		return false;
		}
	// Reads quotation ID
	var quotation_id = parseInt($('#quotation_id').text());

	var line_ids = [];
	var line_unit_prices = [];
	var line_leadtimes = [];
	var line_update = []
	var i = 0;

	// Reads quotation lines IDs	
	$('.columnID').each(function(index,element) {
		var element_column = parseInt($(element).text());
		if (!isNaN(element_column)){
			line_ids.push(parseInt($(element).text()));
			}
		});
	
	// Reads quotation lines unit prices
	$('.update_line.js_unitprice.input-group').each(function(index,element) {
		line_unit_prices.push(parseFloat($(element).val()));
		});
	console.log(line_unit_prices);

	// Reads quotation  prices
	$('.update_line.js_leadtime.input-group').each(function(index,element) {
		if ( $(element).val() != 'N/A' ) {
			line_leadtimes.push(parseInt($(element).val()));
			}
		else {
			line_leadtimes.push(0);
			}
		});

	var i = 0;
	for ( i = 0; i < line_ids.length ; i++) {
		console.log(line_ids[i]);
		console.log(line_unit_prices[i]);
		console.log(line_leadtimes[i]);
        	openerp.jsonRpc("/purchase/save", 'call', {
                	'order_id': quotation_id,
                	'line_id': line_ids,
                	'price_unit': line_unit_prices,
                	'leadtime': line_leadtimes,
	                })
        	        .then(function (data) {
				$(".update_line.js_unitprice.input-group").prop('disabled', true);
				$(".update_line.js_leadtime.input-group").prop('disabled', true);
			        location.reload();
	                });
		}

	location.reload();
        return false;
	
	});

   // Click on the submit button
   $('#btnSubmit').on('click', function (ev) {
	console.log('Clicked Submit Button');
	if (formChanged == false) {
		return false;
		}
	// Reads quotation ID
	var quotation_id = parseInt($('#quotation_id').text());

	var line_ids = [];
	var line_unit_prices = [];
	var line_leadtimes = [];
	var line_update = []
	var i = 0;
	$(".update_line.js_unitprice.input-group").prop('disabled', true);
	$(".update_line.js_leadtime.input-group").prop('disabled', true);

	$('#bc_website_purchase_po_state').text('Bid Received');

	// Reads quotation lines IDs	
	$('.columnID').each(function(index,element) {
		var element_column = parseInt($(element).text());
		if (!isNaN(element_column)){
			line_ids.push(parseInt($(element).text()));
			}
		});
	
	// Reads quotation lines unit prices
	$('.update_line.js_unitprice.input-group').each(function(index,element) {
		line_unit_prices.push(parseFloat($(element).val()));
		});

	// Reads quotation  prices
	$('.update_line.js_leadtime.input-group').each(function(index,element) {
		line_leadtimes.push(parseInt($(element).val()));
		});

	var i = 0;
	for ( i = 0; i < line_ids.length ; i++) {
		console.log(line_ids[i]);
		console.log(line_unit_prices[i]);
		console.log(line_leadtimes[i]);
        	openerp.jsonRpc("/purchase/update_line", 'call', {
                	'order_id': quotation_id,
                	'line_id': line_ids,
                	'price_unit': line_unit_prices,
                	'leadtime': line_leadtimes,
	                })
        	        .then(function (data) {
				$(".update_line.js_unitprice.input-group").prop('disabled', true);
				$(".update_line.js_leadtime.input-group").prop('disabled', true);
			        location.reload();
	                });
		}
	// setTimeout(location.reload,5000);
	for (i = 0; i < 100; i++) {
		location.reload();
		}
        return false;
	
	});

   // Click on the calc button
   $('.update_line.js_unitprice.input-group').on('blur',function() {
	$('#btnCalc').click();
	});

   $('#btnCalc').on('click', function (ev) {
	console.log('Click function');
	var subtotal = [];
	var subtotal_qty = [];
	var total_order = 0;
	var total_order_list = [];
	var i = 0;
	$('.js_product_qty').each(function(index,element) {
		subtotal_qty.push(parseFloat($(element).text()));
		});
	$('.update_line.js_unitprice.input-group').each(function(index,element) {
		subtotal.push(parseFloat($(element).val()));
		});
	for ( i = 0; i < subtotal.length; i ++) {
		total_order = total_order + subtotal[i] * subtotal_qty[i];
		total_order_list.push(subtotal[i] * subtotal_qty[i]);
		}
	$('.js_line_subtotal span').each(function(index,element) {
		$(element).text(total_order_list[index]);
		});
	$('.subtotal_field').children().text(total_order);

	});

})

});
// }());
