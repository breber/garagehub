// variable to keep track if we are using a new category or not
var usingNewCategory = false;

$(document).ready(function() {
	// display input fields based on which record is being added
	if(window.location.pathname.indexOf("gasmileage") > -1){
		$('.generic').hide();
		$('.maintenance').hide();
		$('.gasmileage').show();
	} else if(window.location.pathname.indexOf("maintenance") > -1){
		$('.generic').hide();
		$('.gasmileage').hide();
		$('.maintenance').show();
	} else if(window.location.pathname.indexOf("expense") > -1){
		$('.gasmileage').hide();
		$('.maintenance').hide();
		$('.generic').show();
	}
	
	
	$('#collapseTwo').on('hidden', function() {
		// clears the value so that we know to use the existing category
		$("#newCategory").val("");
	});
	
	var currentDate = new Date();
	var prettyDate = (currentDate.getMonth()+1) + '/' + currentDate.getDate() + '/' + currentDate.getFullYear();
	// make the date picker work
	$('#datePurchased').datepicker({ dateFormat: "mm/dd/yyyy", 
		yearRange: '1900:2020' });
	
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
	
	
	
	//TODO have tell which expense type it is
	
});






