// variable to keep track if we are using a new category or not
var categoriesLength = -1;

$(document).ready(function() {
	// display input fields based on which record is being added
	if(window.location.pathname.indexOf("gasmileage") > -1){
		$('.gasmileage').removeClass( "hidden");
	} else if(window.location.pathname.indexOf("maintenance") > -1){
		$('.maintenance').removeClass( "hidden");
	} else if(window.location.pathname.indexOf("expense") > -1){
		$('.generic').removeClass( "hidden");
	}
	
	// validation engine set up
	$('#addform').validationEngine();
	
	var currentDate = new Date();
	var prettyDate = (currentDate.getFullYear() + '/' + (currentDate.getMonth()+1) + '/' + currentDate.getDate() );
	// make the date picker work
	$('#datePurchased').datepicker({
		format: 'yyyy/mm/dd'
	});
	
	$('#datePurchased').val(prettyDate);

	
	// make function to toggle between using new category and existing categories 
	$('#categoryButton').click(function(){
		// hide validation warnings because you are not submitting it
		$('#addform').validationEngine('hide');
		
		if($('#newCategory').val() != "" && $('#newCategory').val() != null && $('#newCategory').val() != "Enter New Category"){
			if(categoriesLength == -1){
				categoriesLength = $('#category')[0].options.length;				
			} 
			$('#category')[0].options[categoriesLength]=new Option($('#newCategory').val(), $('#newCategory').val(), false, true);
		
			// switch to category tab
			$('#categorytab a:first').tab('show'); 
		}
	});

	
	// try to load expense record to edit.
	if(window.location.pathname.indexOf("edit") > -1){
		editExpenseRecord();
		if(window.location.pathname.indexOf("gasmileage") > -1){
			editFuelRecord();
		} else if(window.location.pathname.indexOf("maintenance") > -1){
			editMaintenanceRecord();
		} else if(window.location.pathname.indexOf("expense") > -1){
			editExpenseRecord();
		}
	}
	
	
});

function manualOdometerClick() {
	$('#odometertab li:eq(1) a').tab('show');
}

function newCategoryKeyPress(e)
{
    // look for window.event in case event isn't passed in
    if (typeof e == 'undefined' && window.event) { e = window.event; }
    if (e.keyCode == 13)
    {
        document.getElementById('categoryButton').click();
    }
}

// Populate baseExpense fields based on record input
function editExpenseRecord() {
	//change header 
	$('.page-header').text("Edit Expense");
	
	$('#datePurchased').val( $('#editdatepurchased').text());
	$('#category').val( $('#editcategory').text());
	$('#location').val( $('#editlocation').text());
	$('#amount').val($('#editamount').text());
	$('#description').val( $('#editdescription').text());	
}

//Populate Maintenance fields based on record input
function editMaintenanceRecord() {
	//change header 
	$('.page-header').text("Edit Maintenance Record");
	
	$('#datePurchased').val( $('#editdatepurchased').text());
	$('#category').val( $('#editcategory').text());
	$('#location').val( $('#editlocation').text());
	$('#amount').val($('#editamount').text());
	$('#description').val( $('#editdescription').text());	
	$('#odometerEnd').val( $('#editodometer').text());
}

//Populate Fuel Record fields based on record input
function editFuelRecord() {
	//change header 
	$('.page-header').text("Edit Fuel Record");
	
	$('#datePurchased').val( $('#editdatepurchased').text());
	$('#location').val( $('#editlocation').text());
	$('#amount').val($('#editamount').text());
	$('#description').val( $('#editdescription').text());	
	$('#pricepergallon').val($('#editpricepergallon').text());
	$('#grade').val($('#editfuelgrade').text());
	
	// Uncheck use last fuel up and switch to manual entry tab
	$('#sinceLastFuelRecord').attr('checked', false);
	$('#odometertab li:eq(1) a').tab('show');
	
	var tmpOdometer = $('#editodometerstart').text();
	if(tmpOdometer != "-1"){
		$('#odometerStart').val(tmpOdometer);
	}
	tmpOdometer = $('#editodometerend').text();
	if(tmpOdometer != "-1"){
		$('#odometerEnd').val(tmpOdometer);
	}
}





