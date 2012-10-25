$().ready(function() {
	//TODO probably will add stuff in here eventually.
	$('#collapseTwo').on('hidden', function() {
		//clears the value so that we know to use the existing category
		$("#newCategory").val("");
	});
});