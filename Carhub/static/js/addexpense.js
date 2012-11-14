// variable to keep track if we are using a new category or not
var usingNewCategory = false;

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
	
	
	
	//category stuff
	$('#collapseTwo').on('hidden', function() {
		// clears the value so that we know to use the existing category
		$("#newCategory").val("");
	});
	
	var currentDate = new Date();
	var prettyDate = (currentDate.getFullYear() + '-' + (currentDate.getMonth()+1) + '-' + currentDate.getDate() );
	// make the date picker work
	$('#datePurchased').datepicker({
		format: 'yyyy-mm-dd'
	});
	
	$('#datePurchased').val(prettyDate);
	
	// start out with new category field hidden
	$('#newCategory').hide();
	
	// make function to toggle between using new category and existing categories 
	$('#categoryButton').click(function(){
		usingNewCategory = ! usingNewCategory;
		if(usingNewCategory){
			$('#newCategory').show();
			$('#category').hide();
			$('#categoryButton').html("Use Existing Category");
		} else {
			$('#newCategory').hide();
			$('#newCategory').val("");
			$('#category').show();
			$('#categoryButton').html("Add and Use New Category");
		}
	});
	
	
});






