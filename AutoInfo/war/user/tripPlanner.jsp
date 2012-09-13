<%@page import="com.google.appengine.api.users.UserServiceFactory"%>
<%@page import="com.google.appengine.api.users.UserService"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance();
%>


<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />
	
	<!-- 	Google maps api javascript -->
	<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD6rEVLWJAAQ6p3IObKwkyGoAVQ_GQZnIg&sensor=false"></script>
    
	<title>CarHub</title>
	
	<style>
		body {
		  font-size: 0.8em;
		}
		
		#map-container, #side-container, #side-container li {
		  float: left;
		}
		
		#map-container {
		  width: 500px;

		}
		
		#side-container {
		  border: 1px solid #bbb;
		  margin-right: 5px;
		  padding: 2px 4px;
		  text-align: right;
		  width: 260px;
		}
		#side-container ul {
		  list-style-type: none;
		  margin: 0;
		  padding: 0;
		}
		#side-container li input {
		  font-size: 0.85em;
		  width: 210px;
		}
		#side-container .dir-label {
		  font-weight: bold;
		  padding-right: 3px;
		  text-align: left;
		  width: 40px;
		}
		
		#dir-container {
		  float: left;
		  overflow: auto;
		  padding: 2px 0px 2px 0px;
		}
		#dir-container table {
		  font-size: 1em;
		  padding: 2px;
		}
	</style>

</head>
<body>
	<div class="navbar navbar-inverse navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
				<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</a>
			
				<a class="brand" href="/">CarHub</a>
				
				<div class="nav-collapse collapse">
					<jsp:include page="/user/navbar.jsp" />
					
					<div class="nav pull-right">
						<jsp:include page="/username.jsp" />
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="container-fluid center-block">
		<div class="row-fluid">
			<jsp:include page="/sideNav.jsp" />

			<div class="well well-small span9">
				<h2>Trip Planner</h2>

				<div id="side-container">
					<ul>
						<li class="dir-label">From:</li>
						<li><input id="from-input" type=text value="Chicago, IL" /></li>
						<li class="dir-label">To:</li>
						<li><input id="to-input" type=text value="San Jose, CA" /></li>
					</ul>
					<div>
						<input onclick="Demo.getDirections();" type=button value="Go!" style="float: left"/>
					</div>
					<div id="dir-container"></div>
				</div>
				<div id="map_canvas" style="width: 500px; height: 300px"></div>
				<br/>
				<div style="list-style-type: none;">
					<form>
						Number of Miles: <br/><input id="num-miles-input" type="text" name="num-miles-input" /><br /> 
						Average MPG: <br/><input id="avg-mpg-input" type="text" name="avg-mpg-input" />
						<br/> Estimated Price Per Gallon: <br/><input id="avg-ppg-input" type="text" name="avg-ppg-input" />
					</form>
					<div>
						<input onclick="calculateTripPrice();" type=button value="Calculate Cost" style="float: left"/>
					</div>
					<br/>
					<br/>
					<form>
						Estimated Cost: <br/><input id="est-cost-trip" type="text" name="est-cost-trip" /><br /> 
					</form>
				</div>


			</div>
			
		</div>
	</div>
	
	<script type="text/javascript">	
	    function calculateTripPrice() {
	    	
	        var miles = document.getElementById('num-miles-input').value;
	        var mpg = document.getElementById('avg-mpg-input').value;
	        var fuelCost = document.getElementById('avg-ppg-input').value;
	        
	        var cost = miles / mpg * fuelCost;
	        
	        document.getElementById('est-cost-trip').value = '$' + cost.toFixed(2);
	        
	    }
    
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
	    		      alert('Directions failed: ' + dirStatus);
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
	    		    var dirRequest = {
	    		      origin: fromStr,
	    		      destination: toStr,
	    		      travelMode: google.maps.DirectionsTravelMode.DRIVING,
	    		      unitSystem: google.maps.DirectionsUnitSystem.IMPERIAL,
	    		      provideRouteAlternatives: true
	    		    };
	    		    Demo.dirService.route(dirRequest, Demo.showDirections);
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
   		});
	</script>
	
	
</body>
</html>

