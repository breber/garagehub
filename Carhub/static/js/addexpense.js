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
	
	// set up new category tbx to be empty
	prepareEmptyTextInput( $('#newCategory'), "Enter New Category");
	prepareEmptyTextInput( $('#odometerStart'), "Enter Odometer Start");
	
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
		
			prepareEmptyTextInput( $('#newCategory'), "Enter New Category");
			// switch to category tab
			$('#categorytab a:first').tab('show'); 
		} else {
			alert("False");
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

function prepareEmptyTextInput(component, startingString) {
	component.css("color","gray");
	component.val(startingString);
	component.click( emptyTextInputClick );
}

function emptyTextInputClick(){
	$(this).val("");
	$(this).unbind("click");
	$(this).css("color","black");
}

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
	$('#datePurchased').val( $('#editdatepurchased').text());
	$('#category').val( $('#editcategory').text());
	
	$('#location').val( $('#editlocation').text());
	
	
	$('#amount').val($('#editamount').text());
	$('#description').val( $('#editdescription').text());	
}

//Populate Maintenance fields based on record input
function editMaintenanceRecord() {
	$('#datePurchased').val( $('#editdatepurchased').text());
	$('#category').val( $('#editcategory').text());
	$('#location').val( $('#editlocation').text());
	$('#amount').val($('#editamount').text());
	$('#description').val( $('#editdescription').text());	
	$('#description').val( $('#editodometer').text());
}

//Populate Fuel Record fields based on record input
function editFuelRecord() {
	$('#datePurchased').val( $('#editdatepurchased').text());
	$('#category').val( $('#editcategory').text());
	
	$('#location').val( $('#editlocation').text());
	
	
	$('#amount').val($('#editamount').text());
	$('#description').val( $('#editdescription').text());	
}





