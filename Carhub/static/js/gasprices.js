$().ready(function() {
	// When the page is ready, hide the table and loading
	// sections so there isn't a huge blank space in the page
	$("#table").hide();
	$("#loading").hide();
});

function getGasPrices() {
	$("#table").empty();
	
	var isChecked = $('#location').attr('checked');
	var JSONGasFeed;
	if (isChecked) {
		getLocation();
	} else {
		useZipCode();
	}
};

function hideZipCode() {
	if ($("#location").is(":checked")) {
		$("#zip").prop("disabled", true);
		$("#zip").val("");
	} else {
		$("#zip").prop("disabled", false);
	}
};

function sendJSONRequest(lat, lon) {
	var radius = document.getElementById('radius').value;
	
	if (!radius) {
		radius = 0;
		document.getElementById('radius').value = radius;
	}
	
	var grade = document.getElementById('grade').value;
	var sort = document.getElementById('sort').value;
	JSONGasFeed = 'http://api.mygasfeed.com/stations/radius/'+lat+'/'+lon+'/'+radius+'/'+grade+'/'+sort+'/zax22arsix.json?callback=?';
	displayGasPrices(JSONGasFeed);
};

function useZipCode() {
	var geocoder = new google.maps.Geocoder();
	var address = document.getElementById('zip').value;
	if (address) {
		geocoder.geocode( { 'address': address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				var latLon = String(results[0].geometry.location);
				var word = latLon.split(",")
				var lat = word[0].substring(1);
				var lon = word[1].substring(1, word[1].length-1);
				sendJSONRequest(lat, lon);
			}
		});
	} else {
		alert('Please enter a zip code or use the Detect My Location option');
	}
};

function useLocation(position) {
	var lat = position.coords.latitude;
	var lon = position.coords.longitude;
	sendJSONRequest(lat, lon);
};

function getLocation(){
   if (navigator.geolocation) {
	  // 30 seconds
      var options = {timeout:30000};
      navigator.geolocation.getCurrentPosition(useLocation, 
                                               errorHandler,
                                               options);
   } else {
      alert("Sorry, your browser does not support geolocation.");
   }
};

function errorHandler(err) {
	if (err.code == 1) {
		alert("Error: Access is denied!");
	} else if (err.code == 2) {
		alert("Error: Position is unavailable!");
	}
};

function showLoading() {
	$("#loading").removeClass("hidden");
	$("#loading").show();
	
	$("#table").hide();
};

function stopLoading(){
	$("#loading").hide();
	$("#table").show();
};

function displayGasPrices(JSONGasFeed) {
	showLoading();
	$.getJSON(JSONGasFeed, function(json) {
		var grade = document.getElementById('grade').value;
		stopLoading();
		
		$.each(json.stations, function(i, item) {
			var price;
			if (grade === 'reg') {
				price = item.reg_price;
			} else if (grade === 'mid') {
				price = item.mid_price;
			} else if (grade === 'pre') {
				price = item.pre_price;
			} else if (grade === 'diesel') {
				price = item.diesel_price;
			}

			if (price !== 'N/A') {
				$('#table').last().append("<tr><td>"+item.station+"</td><td>"+item.address+"</td><td>"+price+"</td><td>"+item.distance+"</td><td>"+item.diesel_date+"</td></tr>");
			}
		});
		
		$.each(json.stations, function(i, item){
			var price;
			if (grade === 'reg') {
				price = item.reg_price;
			} else if (grade === 'mid') {
				price = item.mid_price;
			} else if (grade === 'pre') {
				price = item.pre_price;
			} else if (grade === 'diesel') {
				price = item.diesel_price;
			}
			
			if (price === 'N/A') {
				$('#table').last().append("<tr><td>"+item.station+"</td><td>"+item.address+"</td><td>"+price+"</td><td>"+item.distance+"</td><td>"+item.diesel_date+"</td></tr>");
			}
	    });
		
		$('#table').prepend("<tr><th>Name</th><th>Location</th><th>Price</th><th>Distance</th><th>Last Updated</th></tr>");
	});
};
