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
	var prettyDate = (currentDate.getFullYear() + '-' + (currentDate.getMonth()+1) + '-' + currentDate.getDate() );
	// make the date picker work
	$('#datePurchased').datepicker({
		format: 'yyyy-mm-dd'
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
		
			prepareNewCategory();
			// switch to category tab
			$('#categorytab a:first').tab('show'); 
		} else {
			alert("False");
		}
	});
	
	
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






