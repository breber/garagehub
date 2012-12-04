var editID;

$(document).ready(function() {
	$('.maint-datatable').dataTable( {
		"sDom": "<'row'<'span6'l><'span6'f>r>t",
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": false,
		"bSort": true,
		"bInfo": false,
		"bAutoWidth": false,
		"aaSorting": [[ 0, 'desc' ]]
	} );

	//make rows selectable
	$('.maint-datatable tbody').click(function(event) {
		$(this.parentElement.fnSettings().aoData).each(function (){
			$(this.nTr).removeClass('active');
		});
		$(event.target.parentNode).addClass('active');
		
		//get key for record
		editID = event.target.parentNode.id;
	});

	$('.receiptlink').click( function() {
		$('#displayimage').modal();
		$('#modalimage').attr('src', this.getAttribute('value'));
	});

});

function editRecord(link){
	// make sure something is selected
	if(editID) {
		window.location = link + editID;		
	} else if(link.indexOf("edit") > -1){
		alert("Please select a record to edit.");
	} else if(link.indexOf("delete") > -1){
		alert("Please select a record to delete.");
	}
	
}