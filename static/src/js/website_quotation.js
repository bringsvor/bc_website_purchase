$(function () {
'use strict';
var website = openerp.website;
var color = $('#btnSubmit').css('background-color');
$('.columnID').css("visibility","hidden");
$('#quotation_id').css("visibility","hidden");

function isDate(txtDate)
{
    var currVal = txtDate;
    if(currVal == '')
        return false;

    var rxDatePattern = /^(\d{4})(\/|-)(\d{1,2})(\/|-)(\d{1,2})$/; //Declare Regex
    var dtArray = currVal.match(rxDatePattern); // is format OK?

    if (dtArray == null) 
        return false;

    //Checks for mm/dd/yyyy format.
    var dtMonth = dtArray[3];
    var dtDay= dtArray[5];
    var dtYear = dtArray[1];        

    if (dtMonth < 1 || dtMonth > 12) 
        return false;
    else if (dtDay < 1 || dtDay> 31) 
        return false;
    else if ((dtMonth==4 || dtMonth==6 || dtMonth==9 || dtMonth==11) && dtDay ==31) 
        return false;
    else if (dtMonth == 2) 
    {
        var isleap = (dtYear % 4 == 0 && (dtYear % 100 != 0 || dtYear % 400 == 0));
        if (dtDay> 29 || (dtDay ==29 && !isleap)) 
                return false;
    }
    return true;
}



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
$(".update_line.js_units_shipped.input-group").each(function(index,element) {
	$(element).numericInput({
		allowFloat: false, // Accpets positive numbers (floating point)
		allowNegative: false // Accpets positive or negative integer
	});
        // if ( !($(element).val())){
	//	formChanged = false;
	//	}
});
$(".update_line.js_weight.input-group").each(function(index,element) {
	$(element).numericInput({
		allowFloat: false, // Accpets positive numbers (floating point)
		allowNegative: false // Accpets positive or negative integer
	});
        //if ( !($(element).val())){
	//	formChanged = false;
	//	}
});
$(".update_line.js_collies.input-group").each(function(index,element) {
	$(element).numericInput({
		allowFloat: false, // Accpets positive numbers (floating point)
		allowNegative: false // Accpets positive or negative integer
	});
        //if ( !($(element).val())){
	//	formChanged = false;
	//	}
});
$(".update_line.js_units_in_stock.input-group").each(function(index,element) {
	$(element).numericInput({
		allowFloat: false, // Accpets positive numbers (floating point)
		allowNegative: false // Accpets positive or negative integer
	});
        //if ( !($(element).val())){
	//	formChanged = false;
	//	}
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
   $('#btnPurchaseCancel').on('click', function (ev) {
	if (confirm("Close Window?")){
		close();
		}
	});

   // Click on the save button
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
	var line_units_shipped = [];
	var line_weight = [];
	var line_collies = [];
	var line_units_in_stock = [];
	var line_batch_number = [];
	var line_tracking_number = [];
	var line_date_code = [];
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

	// Reads units_shipped
	$('.update_line.js_units_shipped.input-group').each(function(index,element) {
		line_units_shipped.push(parseFloat($(element).val()));
		});
	console.log('Units shipped');
	console.log(line_units_shipped);

	// Reads weight
	$('.update_line.js_weight.input-group').each(function(index,element) {
		line_weight.push(parseFloat($(element).val()));
		});
	console.log('Weight');
	console.log(line_weight);

	// Reads collies
	$('.update_line.js_collies.input-group').each(function(index,element) {
		line_collies.push(parseFloat($(element).val()));
		});
	console.log(line_collies);

	// Reads units_in_stock
	$('.update_line.js_units_in_stock.input-group').each(function(index,element) {
		line_units_in_stock.push(parseFloat($(element).val()));
		});
	console.log(line_units_in_stock);

	// Reads batch_number
	$('.update_line.js_batch_number.input-group').each(function(index,element) {
		line_batch_number.push($(element).val());
		});
	console.log('Batch Number');
	console.log(line_batch_number);

	// Reads tracking_number
	$('.update_line.js_tracking_number.input-group').each(function(index,element) {
		line_tracking_number.push($(element).val());
		});
	console.log('Tracking Number');
	console.log(line_tracking_number);

	// Reads date_code
	$('.update_line.js_date_code.input-group').each(function(index,element) {
		if (!isDate($(element).val())){
			alert('Date is invalid format - Format needs to be yyyy/mm/d');
			return False;
			};
		console.log('Date code');
		console.log($(element).val());
		line_date_code.push($(element).val());
		});
	console.log('Date Code');
	console.log(line_date_code);

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
        $.blockUI({ css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff'
        } });


	for ( i = 0; i < line_ids.length ; i++) {
		console.log(line_ids[i]);
		console.log(line_unit_prices[i]);
		console.log(line_leadtimes[i]);
        	openerp.jsonRpc("/purchase/save", 'call', {
                	'order_id': quotation_id,
                	'line_id': line_ids,
                	'price_unit': line_unit_prices,
                	'leadtime': line_leadtimes,
                	'units_shipped': line_units_shipped,
                	'weight': line_weight,
                	'collies': line_collies,
                	'units_in_stock': line_units_in_stock,
                	'batch_number': line_batch_number,
                	'tracking_number': line_tracking_number,
                	'date_code': line_date_code,
	                })
        	        .then(function (data) {
				$(".update_line.js_unitprice.input-group").prop('disabled', true);
				$(".update_line.js_leadtime.input-group").prop('disabled', true);
			        location.reload();
	                });
		}
	setTimeout($.unblockUI, 5000); 

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

        $('#btnSave').addClass('disabled');
        $('#btnSave').prop('disabled', true);
        $('#btnSubmit').addClass('disabled');
        $('#btnSubmit').prop('disabled', true);


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

        $.blockUI({ css: { 
            border: 'none', 
            padding: '15px', 
            backgroundColor: '#000', 
            '-webkit-border-radius': '10px', 
            '-moz-border-radius': '10px', 
            opacity: .5, 
            color: '#fff' 
        } }); 

	console.log('Quotation ID');
	console.log(quotation_id);
	console.log(line_ids);
	console.log(line_unit_prices);
	console.log(line_leadtimes);
       	openerp.jsonRpc("/purchase/update_line", 'call', {
               	'order_id': quotation_id,
               	'line_id': line_ids,
               	'price_unit': line_unit_prices,
               	'leadtime': line_leadtimes,
                })
       	        .then(function (data) {
			$(".update_line.js_unitprice.input-group").prop('disabled', true);
			$(".update_line.js_leadtime.input-group").prop('disabled', true);
		        // location.reload();
                });

	//for ( i = 0; i < line_ids.length ; i++) {
        //	openerp.jsonRpc("/purchase/update_line", 'call', {
        //        	'order_id': quotation_id,
        //        	'line_id': line_ids,
        //        	'price_unit': line_unit_prices,
        //        	'leadtime': line_leadtimes,
	//                })
        //	        .then(function (data) {
	//			$(".update_line.js_unitprice.input-group").prop('disabled', true);
	//			$(".update_line.js_leadtime.input-group").prop('disabled', true);
	//                });
	//	}

	setTimeout($.unblockUI, 5000); 
	// location.reload();
	// setTimeout(location.reload,5000);
	// for (i = 0; i < 100; i++) {
	//	location.reload();
	//	}
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
