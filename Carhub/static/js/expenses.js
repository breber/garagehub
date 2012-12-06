var editID;

$(document).ready(function() {
	var dTable = $('#expense-table').dataTable({
		"sDom" : "<'row'<'span6'l><'span6'f>r>t",
		"bPaginate" : false,
		"bLengthChange" : false,
		"bFilter" : false,
		"bSort" : true,
		"bInfo" : false,
		"bAutoWidth" : false,
		"oTableTools" : {
			"sRowSelect" : "multi",
		},
		/*"aoColumnDefs": [
		                 { "bVisible":    false, "aTargets": [0]} 
		             ],*//* this code will hide the first row  */
		"aaSorting" : [ [ 0, 'desc' ] ]
	});

	//make rows selectable
	$('#expense-table tbody').click(function(event) {
		$(dTable.fnSettings().aoData).each(function() {
			$(this.nTr).removeClass('active');
		});
		$('.alert').alert('close');
		
		$('#expense-delete').removeAttr('disabled');
		$('#expense-edit').removeAttr('disabled');
		
		$(event.target.parentNode).addClass('active');

		//get key for record
		editID = event.target.parentNode.id;
	});
});

$('.receiptlink').click(function() {
	$('#displayimage').modal();
	$('#modalimage').attr('src', this.getAttribute('value'));
});

function editRecord(link) {
	// make sure something is selected
	if (editID) {
		window.location = link + editID;		
	} else if (link.indexOf("edit") > -1){
		newAlert("Please select a record to edit.");
	} else if (link.indexOf("delete") > -1){
		newAlert("Please select a record to delete.");
	}
}

function newAlert (message) {
	$('.alert').remove();
	$("#alert-area").append($("<div class='alert alert-area fade in'>" +
			"<button type='button' class='close' data-dismiss='alert'>x</button>" +
			"<strong>Warning!</strong> " + message + "" +
					"</div>"));
	$('.alert').delay(2000).fadeOut("slow", function () { $(this).remove(); });
}
