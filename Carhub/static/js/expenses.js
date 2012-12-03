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
		"oTableTools": {
            "sRowSelect": "multi",
		},
		/*"aoColumnDefs": [
		                 { "bVisible":    false, "aTargets": [0]}
		             ],*/
		"aaSorting" : [ [ 1, 'desc' ] ]
	});
	 
	//the aoColumnDefs line will hide the first column which has the record key in it.
	
	
	
	//make rows selectable
	$('#expense-table tbody').click(function(event) {
		$(dTable.fnSettings().aoData).each(function (){
			$(this.nTr).removeClass('active');
		});
		$(event.target.parentNode).addClass('active');
		
		//get address
		editID = event.target.parentNode.cells[0].textContent;
	});
	

	/* in case you want row_selected
table.display tr.even.row_selected td {
	background-color: #B0BED9;
}

table.display tr.odd.row_selected td {
	background-color: #9FAFD1;
}*/
});

$('.receiptlink').click( function() {
	$('#displayimage').modal();
	$('#modalimage').attr('src', this.getAttribute('value'));
});

function editSelectedRecord()
{
	//TODO get the selected row and edit it.
	

}

function editRecord(link){

	// TODO make sure something is selected
	
	
	window.location = link + editID;
}

//TODO
// 	make modal to upload images in editable table mode
//	make editable table mode and display the columns that need to be able to be edited
