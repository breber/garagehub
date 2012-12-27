$(document).ready(function() {
	var dTable = $('#expense-table').dataTable({
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
	$('#expense-table tbody').click(function(event) {
		$(dTable.fnSettings().aoData).each(function() {
			$(this.nTr).removeClass('active');
		});

		$(event.target.parentNode).addClass('active');
	});
});

$('.receiptlink').click(function() {
	$('#displayimage').modal();
	$('#modalimage').attr('src', this.getAttribute('value'));
});
