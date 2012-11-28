function calculateTripPrice() {
	
    var miles = document.getElementById('num-miles-input').value;
    var mpg = document.getElementById('avg-mpg-input').value;
    var fuelCost = document.getElementById('avg-ppg-input').value;
    
    var cost = miles / mpg * fuelCost;
    
    document.getElementById('est-cost-trip').value = '$' + cost.toFixed(2);
    
}

function hideFromInput() {
	if ($("#useCurrentLocation").is(":checked")) {
		$("#from-input").prop("disabled", true);
	} else {
		$("#from-input").prop("disabled", false);
	}
};

var Demo = {
// 	    		  // HTML Nodes
		  dirContainer: document.getElementById('dir-container'),
		  fromInput: document.getElementById('from-input'),
		  toInput: document.getElementById('to-input'),

// 	    		  // API Objects
		  dirService: new google.maps.DirectionsService(),
		  dirRenderer: new google.maps.DirectionsRenderer(),
		  map: null,

		  showDirections: function(dirResult, dirStatus) {
			  
		    if (dirStatus != google.maps.DirectionsStatus.OK) {
		      alert('Directions failed. Please check input and enable HTML 5 location services.');
		      return;
		    }

		    // Show directions
		    Demo.dirRenderer.setMap(Demo.map);
		    Demo.dirRenderer.setPanel(Demo.dirContainer);
		    Demo.dirRenderer.setDirections(dirResult);
		    document.getElementById('num-miles-input').value = Math.round(getTotalDistance(dirResult, Demo.dirRenderer.getRouteIndex())/1609.344);
		    calculateTripPrice();
		  },


		  getDirections: function() {
		    var fromStr = Demo.fromInput.value;
		    var toStr = Demo.toInput.value;

		    navigator.geolocation.getCurrentPosition(function(position){
			    var curLat;
			    var curLon;
		    	curLat = position.coords.latitude;
		    	curLon = position.coords.longitude;
		    	if ($("#useCurrentLocation").is(":checked")) {
			    	fromStr = new google.maps.LatLng(curLat, curLon);
			    }
			    var dirRequest = {
			      origin: fromStr,
			      destination: toStr,
			      travelMode: google.maps.DirectionsTravelMode.DRIVING,
			      unitSystem: google.maps.DirectionsUnitSystem.IMPERIAL,
			      provideRouteAlternatives: true
			    };
			    Demo.dirService.route(dirRequest, Demo.showDirections);
		    });
		    
		  },

		  init: function() {
			  var mapOptions = {
				        zoom: 8,
				        center: new google.maps.LatLng(-34.397, 150.644),
				        mapTypeId: google.maps.MapTypeId.ROADMAP
				      };
		    Demo.map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
  

    		    // Show directions onload
		    Demo.getDirections();
		  }
		};

function getTotalDistance(result, index) {
    var meters = 0;
    var route = result.routes[index];
    for (i = 0; i < route.legs.length; i++) {
        //Get the distance in meters
        meters += route.legs[i].distance.value;
    }
    return meters;
}
	    
google.maps.event.addDomListener(window, 'load', Demo.init);

$(document).ready(function()
{
    $('#dir-container').click(function() {
    	  // Handler for .ready() called.
    	document.getElementById('num-miles-input').value = Math.round(getTotalDistance(Demo.dirRenderer.getDirections(), Demo.dirRenderer.getRouteIndex())/1609.344);
		calculateTripPrice();
    });
    
    hideFromInput();
});