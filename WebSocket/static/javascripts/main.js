$(document).ready(function() {
	document.session = $('#session').val();
	setTimeout(request, 100);
	$('#add-button').click(function(event) {
		jQuery.ajax({
			url: '//localhost:8000/cart',
			type: 'POST',
			data: {
				session: document.session,
				action: 'add'
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled');
				$('#add-to-cart').hide();
				$('#remove-from-cart').show();
				$(event.target).removeAttr('disabled');
			},
			// success: function(data, status, xhr) {
			// 	// $('#add-to-cart').hide();
			// 	// $('#remove-from-cart').show();
			// 	// $(event.target).removeAttr('disabled');
			// 	console.log(document.session);

			// },
		}).done(function( html ) {
			console.log(document.session);
		});;
	});

	$('#remove-button').click(function(event){

		jQuery.ajax({
			url:'//localhost:8000/cart',
			type:'POST',
			data:{
				session:document.session,
				action:'remove'
			},
			dataType:'json',
			beforeSend:function(xhr,settings){
				$(event.target).attr('disabled','disabled');
				$('#add-to-cart').show();
				$('#remove-from-cart').hide();
				$(event.target).removeAttr('disabled');
			},
			// success:function(data,status,xhr){
			// 	$('#remove-from-cart').hide();
			// 	$('#add-to-cart').show();
			// 	$(event.target).removeAttr('disabled');
			// }
		});
	});
});

function request(){
	var host = 'ws://localhost:8000/cart/status';
	var count = parseInt($('#count').text());
	var websocket = new WebSocket(host);
	websocket.onopen = function(event){};
	websocket.onmessage =function(event){
		var data = parseInt($.parseJSON(event.data)['Count']);
		if(count > data){
			$.notify({
				title: 'Thank you',
				message: 'You have added a product'
			},{
				type: 'minimalist',
				delay: 5000,
				icon_type: 'image',
				template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
				'<span data-notify="title">{1}</span>' +
				'<span data-notify="message">{2}</span>' +
				'</div>'
			});
		}
		else{
			$.notify({
				title: 'Thank you',
				message: 'You have removed a product'
			},{
				type: 'minimalist',
				delay: 5000,
				icon_type: 'image',
				template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
				'<span data-notify="title">{1}</span>' +
				'<span data-notify="message">{2}</span>' +
				'</div>'
			});
		}
		$('#count').html(data);
	}
	websocket.onerror = function(event){
		console.log(event);
	}
}