$(document).ready(function() {
	
	$('.changingDiv').hide();
	$('#onetimeFreq').attr('checked', 'checked');
	$('#dateCheckbox').attr('checked', 'checked');
	showProperFields();

	var currentDate = new Date();
	var prettyDate = (currentDate.getFullYear() + '-' + (currentDate.getMonth()+1) + '-' + currentDate.getDate() );
	
	$('#dateToNotify').datepicker({
		format: 'yyyy-mm-dd'
	});
	
	$('#dateToNotify').val(prettyDate);
	
	$('.triggerChange').click(showProperFields);
});

function showProperFields() {
	
	$('.changingDiv').hide();
	
	if ($('#mileageCheckbox').is(':checked')) {
		if ($('#onetimeFreq').is(':checked')) {
			$('#onetimeMilesDiv').show();
		}
		else if ($('#recurringFreq').is(':checked')) {
			$('#recurringMilesDiv').show();
		}
	}
	
	if ($('#dateCheckbox').is(':checked')) {
		if ($('#onetimeFreq').is(':checked')) {
			$('#onetimeDateDiv').show();
		}
		else if ($('#recurringFreq').is(':checked')) {
			$('#recurringDateDiv').show();
		}
	}
}