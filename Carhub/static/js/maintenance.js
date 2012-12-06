var editID;
var maintDatatables;

$(document).ready(function() {
	var h3s = [];
	$('.h3').each(function(i) {
		h3s[i] = this.innerHTML;
	});

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

	// make rows selectable
	$('.maint-datatable tbody').click(function(event) {
		$('.maint-datatable').each(function() {
			$($(this).dataTable().fnSettings().aoData).each(function() {
		
				$(this.nTr).removeClass('active');
			});
		});
		$('.alert').alert('close');
		
		$('#maint-delete').removeAttr('disabled');
		$('#maint-edit').removeAttr('disabled');
		
		$(event.target.parentNode).addClass('active');

		// get key for record
		editID = event.target.parentNode.id;
	});

	$('.receiptlink').click(function() {
		$('#displayimage').modal();
		$('#modalimage').attr('src', this.getAttribute('value'));
	});
});

function editRecord(link) {
	// make sure something is selected
	if (editID) {
		window.location = link + editID;
	} else if (link.indexOf("edit") > -1) {
		newAlert("Please select a record to edit.");
	} else if (link.indexOf("delete") > -1) {
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
