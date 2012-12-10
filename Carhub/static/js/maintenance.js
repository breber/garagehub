var maintDatatables;

$(document).ready(function() {
	$('.maint-datatable').dataTable({
		"sDom" : "t",
		"bPaginate" : false,
		"bLengthChange" : false,
		"bFilter" : false,
		"bSort" : true,
		"bInfo" : false,
		"bAutoWidth" : false,
		"aaSorting" : [ [ 0, 'desc' ] ]
	});
	
	// Setup the handlers for the edit/delete buttons
	setupHandlers();

	// make rows selectable
	$('.maint-datatable tbody').click(function(event) {
		$('.maint-datatable').each(function() {
			$($(this).dataTable().fnSettings().aoData).each(function() {
				$(this.nTr).removeClass('active');
			});
		});
		
		$(event.target.parentNode).addClass('active');
	});

	$('.receiptlink').click(function() {
		$('#displayimage').modal();
		$('#modalimage').attr('src', this.getAttribute('value'));
	});
});
