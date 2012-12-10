//array to keep track of the markers displayed in the map
var markersArray = [];

//variable to keep track of the 
var latLngModal;

//variable to keep track of the map
var Demo = {

		  init: function() {
			  var mapOptions = {
				        zoom: 14,
				        center: new google.maps.LatLng(-34.397, 150.644),
				        mapTypeId: google.maps.MapTypeId.ROADMAP
				      };
		    Demo.map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

		  }
		};

//Ready function
$(document).ready(function() {
	// When the page is ready, hide the table and loading
	// sections so there isn't a huge blank space in the page
	$("#gaspricetable").hide();
	$("#loading").hide();
	
	// Setup click handlers
	$("#location").click(hideZipCode);
	$("#fetchPrices").click(getGasPrices);
	
	getGasPrices();
});

//Work around for the map displaying grey areas on the modal load
$('#modalMap').on('shown', function () {
    google.maps.event.trigger(Demo.map, "resize");
    var lat = $(this).parent().find('td').eq(5).text();
	var lon = $(this).parent().find('td').eq(6).text();
	var latLng = new google.maps.LatLng(lat, lon); //Makes a latlng
	Demo.map.panTo(latLngModal);
});

//render the map
google.maps.event.addDomListener(window, 'load', Demo.init);

$("#gaspricetable tr td").live("click", function() {
	var lat = $(this).parent().find('td').eq(5).text();
	var lon = $(this).parent().find('td').eq(6).text();
	$( "#modalMap" ).modal();	
	

	var mapOptions = {
	        zoom: 14,
	        center: new google.maps.LatLng(lat, lon),
	        mapTypeId: google.maps.MapTypeId.ROADMAP
	      };
	Demo.map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

    clearOverlays();
    
    var latLng = new google.maps.LatLng(lat, lon); //Makes a latlng
	addMarker(latLng);
	latLngModal = latLng;
});

// Function for adding a marker to the page.
function addMarker(location) {
    marker = new google.maps.Marker({
        position: location,
        map: Demo.map
    });
    
    markersArray.push(marker);
}

//function to clear all map overlays
function clearOverlays() {
	  if (markersArray) {
	    for (i in markersArray) {
	      markersArray[i].setMap(null);
	    }
	  }
	}


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
		newAlert('Please enter a zip code or use the Detect My Location option');
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
	   newAlert("Sorry, your browser does not support geolocation.");
   }
};

function errorHandler(err) {
	if (err.code == 1) {
		newAlert("Error: Access is denied!");
	} else if (err.code == 2) {
		newAlert("Error: Position is unavailable!");
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
			var distance = item.distance;
			var price = item.price;
			var dateUpdated = item.date;
			var index = distance.indexOf("miles");
			if(index != -1){
				distance = distance.substr(0, index);
			}
			
			$('#gaspricetable').last().append("<tr class=\"linkable\"><td>"+item.station+"</td><td>"+item.address+"</td><td>"+price+"</td><td>"+distance+"</td><td>"+dateUpdated+"</td><td>"+item.lat+"</td><td>"+item.lng+"</td></tr>");
			
		});
		
		$('#gaspricetable').prepend("<thead><tr><th>Name</th><th>Location</th><th>Price (Dollars)</th><th>Distance (Miles)</th><th>Last Updated</th><th>Lat</th><th>Lon</th></tr></thead>");

		//Hide the latitude and longitude columns
		$("#gaspricetable td:nth-child(6),th:nth-child(6)").hide();
		$("#gaspricetable td:nth-child(7),th:nth-child(7)").hide();
		
		
		var sort = document.getElementById('sort').value;
		var sortByColumn = 2;
		if(sort === "distance"){
			sortByColumn = 3;
		}
		if (typeof oTable == 'undefined') {
			oTable = $('#gaspricetable').dataTable({
				"aaSorting": [[ sortByColumn, "asc" ]],
				"bPaginate": false,
		        "bLengthChange": false,
		        "bFilter": false,
		        "bInfo": false,
		        "bAutoWidth": false
			});

		}
		else
		{
			oTable.fnDestroy();
			oTable = $('#gaspricetable').dataTable({
				"aaSorting": [[ sortByColumn, "asc" ]],
				"bPaginate": false,
		        "bLengthChange": false,
		        "bFilter": false,
		        "bInfo": false,
		        "bAutoWidth": false
			});
		
		}
		
	});
};
