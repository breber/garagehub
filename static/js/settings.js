var editID;
var editText;
var editCategoryType;
var maintDatatables;

$(document).ready(function() {
	var catDTable = $('#expense-category-table').dataTable({
		"sDom" : "t",
		"bPaginate" : false,
		"bLengthChange" : false,
		"bFilter" : false,
		"bSort" : false,
		"bInfo" : false,
		"bAutoWidth" : false
	});

	var maintCatDTable = $('#maint-category-table').dataTable({
		"sDom" : "t",
		"bPaginate" : false,
		"bLengthChange" : false,
		"bFilter" : false,
		"bSort" : false,
		"bInfo" : false,
		"bAutoWidth" : false
	});

	// make rows selectable
	$('.category-datatable tbody').click(function(event) {
		$(catDTable.fnSettings().aoData).each(function() {
			$(this.nTr).removeClass('active');
		});
		$(maintCatDTable.fnSettings().aoData).each(function() {
			$(this.nTr).removeClass('active');
		});

		// get key for record
		editID = event.target.parentNode.id;
		if(editID != "add"){
			$(event.target.parentNode).addClass('active');
		}

		editText = event.target.childNodes[0].data;
		if($(event.target).hasClass('expense')){
			editCategoryType = "expense";
		} else if ($(event.target).hasClass('maintenance')){
			editCategoryType = "maintenance";
		}
	});

	$('#editCategory').click(function() {
		if(editID && editID != "add"){
			$('#modalheader').text("Edit Category");
			$('#categoryName').val(editText);
			$(saveForm).attr("action", "/settings/category/" + editCategoryType + "/edit/" + editID);
			$('#editCategoryModal').modal();
		}
	});

	$('#addExpCategory').click(function() {
		$('#modalheader').text("Add Expense Category");
		$('#categoryName').val("");
		$(saveForm).attr("action", "/settings/category/expense/add");
		$('#editCategoryModal').modal();
	});

	$('#addMaintCategory').click(function() {
		$('#modalheader').text("Add Maintenance Category");
		$('#categoryName').val("");
		$(saveForm).attr("action", "/settings/category/maintenance/add");
		$('#editCategoryModal').modal();
	});

	$('#deleteCategory').click(function() {
		if (editID && editID != "add") {
			window.location = "/settings/category/" + editCategoryType + "/delete/" + editID;
		}
	});
});
