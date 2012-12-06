var editID;

$(document).ready(function() {

	$('#notif-datatable').dataTable({
		"sDom" : "t",
		"bPaginate" : false,
		"bLengthChange" : false,
		"bFilter" : false,
		"bSort" : true,
		"bInfo" : false,
		"bAutoWidth" : false,
		"oTableTools" : {
			"sRowSelect" : "multi",
		},
		"aaSorting" : [ [ 0, 'desc' ] ]
	});

	// make rows selectable
	$('#notif-datatable tbody').click(function(event) {
		$($('#notif-datatable').dataTable().fnSettings().aoData).each(function() {
			$(this.nTr).removeClass('active');
		});

		$(event.target.parentNode).addClass('active');

		// get key for record
		editID = event.target.parentNode.id;
	});
	
	$('#notif-deleteButton').click(function() {
		if (editID) {
			window.location = "/notifications/delete/" + editID;
		} else {
			alert("Please select a notification to delete.");
		}
	});
});