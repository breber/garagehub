$().ready(function() {
	// When the page is ready, hide the table and loading
	// sections so there isn't a huge blank space in the page
	$("#gaspricetable").hide();
	$("#loading").hide();
});

function getGasPrices() {
	$("#gaspricetable").empty();
	
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
	
	$("#gaspricetable").hide();
};

function stopLoading(){
	$("#loading").hide();
	$("#gaspricetable").show();
};

var oTable;

function displayGasPrices(JSONGasFeed) {
	showLoading();
	$.getJSON(JSONGasFeed, function(json) {
		var grade = document.getElementById('grade').value;
		stopLoading();
		
		$.each(json.stations, function(i, item) {
			var price;
			var dateUpdated;
			if (grade === 'reg') {
				price = item.reg_price;
				dateUpdated = item.reg_date;
			} else if (grade === 'mid') {
				price = item.mid_price;
				dateUpdated = item.mid_date;
			} else if (grade === 'pre') {
				price = item.pre_price;
				dateUpdated = item.pre_date;
			} else if (grade === 'diesel') {
				price = item.diesel_price;
				dateUpdated = item.diesel_date;
			}

			if (price !== 'N/A') {
				$('#gaspricetable').last().append("<tr><td>"+item.station+"</td><td>"+item.address+"</td><td>"+price+"</td><td>"+item.distance+"</td><td>"+dateUpdated+"</td><td>"+item.lat+"</td><td>"+item.lng+"</td></tr>");
			}
		});
		var count = 0;
		$.each(json.stations, function(i, item){
			var price;
			var dateUpdated;
			if (grade === 'reg') {
				price = item.reg_price;
				dateUpdated = item.reg_date;
			} else if (grade === 'mid') {
				price = item.mid_price;
				dateUpdated = item.mid_date;
			} else if (grade === 'pre') {
				price = item.pre_price;
				dateUpdated = item.pre_date;
			} else if (grade === 'diesel') {
				price = item.diesel_price;
				dateUpdated = item.diesel_date;
			}
			
			if (price === 'N/A') {
				$('#gaspricetable').last().append("<tr><td>"+item.station+"</td><td>"+item.address+"</td><td>"+price+"</td><td>"+item.distance+"</td><td>"+dateUpdated+"</td><td>"+item.lat+"</td><td>"+item.lng+"</td></tr>");//.click(function(e){alert(e.text());});
			}
			count = count + 1;
	    });
		
		$('#gaspricetable').prepend("<thead><tr><th>Name</th><th>Location</th><th>Price</th><th>Distance</th><th>Last Updated</th><th>Lat</th><th>Lon</th></tr></thead>");
		

		$("#gaspricetable td:nth-child(6),th:nth-child(6)").hide();
		$("#gaspricetable td:nth-child(7),th:nth-child(7)").hide();
		
		if (typeof oTable == 'undefined') {
			oTable = $('#gaspricetable').dataTable({
				"bPaginate": false,
		        "bLengthChange": false,
		        "bFilter": false,
		        "bSort": true,
		        "bInfo": false,
		        "bAutoWidth": false
			});
		}
		else
		{
			oTable.fnClearTable( 0 );
			oTable.fnDraw();
		}
		
	});
};
