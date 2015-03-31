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
	jQuery.getJSON('//localhost:8000/cart/status', { session: document.session }, function(data, status,xhr) {
		$('#count').html(data['Count']);
		setTimeout(request,0);
	});
}