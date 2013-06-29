// Ready function
$(document).ready(function() {
	var id = document.getElementById("stationId");
	alert(id.innerHTML);
	sendJSONRequest(id.innerHTML);
});

function sendJSONRequest(stationId) {
	var baseURL = "http://api.mygasfeed.com/stations/details/%s/zax22arsix.json?callback=?";
	var jsonURL = sprintf(baseURL, stationId);
	displayGasPrices(jsonURL);
}

function errorHandler(err) {
	if (err.code == 1) {
		newAlert("Error: Access is denied! Please check your location settings.");
	} else if (err.code == 2) {
		newAlert("Error: Position is unavailable!");
	}
}

function showLoading() {
	$("#loading").removeClass("hidden");
	$("#loading").show();

	$("#gasprices").hide();
}

function stopLoading() {
	$("#loading").hide();
	$("#gasprices").show();
}

function displayGasPrices(JSONGasFeed) {
    showLoading();

    $.getJSON(JSONGasFeed,
        function(json) {
            var data = [];
            var item = json.details;
            
            $('#stationInfo').empty();
        	$('#stationInfo').append('<h4>' + item.station_name+' - '+ item.address+' </h4><h5> Regular Price: '+ item.reg_price+' </h5><h5>Mid Price: '+ item.mid_price+' </h5><h5>Premium Price: '+ item.pre_price + '</h5>');

            stopLoading();
        }
    );
}
