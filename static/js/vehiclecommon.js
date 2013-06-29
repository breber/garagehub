function getVehicleId() {
	return /\/vehicle\/([^\/]+)/.exec(window.location.pathname);
}

function newAlert(message) {
	var alertDiv =
		"<div class='alert'>" +
			"<button type='button' class='close' data-dismiss='alert'>&times;</button>" +
			"<strong>Warning!</strong> " + message +
		"</div>";

	$("#alert").html(alertDiv);
}

// FOR maintenance, gasmileage and expenses

function setupHandlers() {
	$("#record-edit").click(function() {
		editRecord();
	});

	$("#record-delete").click(function() {
		deleteRecord();
	});
}

function getSelectedRow() {
	return $("tr.active").attr("id");
}

function deleteRecord() {
	var selectedId = getSelectedRow();
	if (selectedId) {
		var url = /(\/vehicle\/[^\/]+\/[^\/]+)/.exec(window.location.pathname);
		window.location = url[0] + "/delete/" + selectedId;
	} else {
		newAlert("Please select a record to delete");
	}
}

function editRecord() {
	var selectedId = getSelectedRow();
	if (selectedId) {
		var url = /(\/vehicle\/[^\/]+\/[^\/]+)/.exec(window.location.pathname);
		window.location = url[0] + "/edit/" + selectedId;
	} else {
		newAlert("Please select a record to edit");
	}
}
