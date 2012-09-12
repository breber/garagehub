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
	<script src="https://maps.googleapis.com/maps/api/js?sensor=false"></script>
    
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
					<ul class="nav">
						<li class="dropdown">
							<a href="#" class="dropdown-toggle"	data-toggle="dropdown">Garage <b class="caret hidden-phone"></b></a>
							<ul class="dropdown-menu">
								<li><a href="">Car 1</a></li>
								<li><a href="">Car 2</a></li>
								<li class="divider"></li>
								<li><a href="">Add Vehicle</a>
							</ul>
						</li>
						<li class="dropdown">
							<a href="#" class="dropdown-toggle"	data-toggle="dropdown">Tools <b class="caret hidden-phone"></b></a>
							<ul class="dropdown-menu">
								<li><a href="">Nearby Gas Prices</a></li>
								<li><a href="">Trip Planner</a></li>
							</ul>
						</li>
						<li class="dropdown">
							<a href="#" class="dropdown-toggle"	data-toggle="dropdown">Notifications <b class="caret hidden-phone"></b></a>
							<ul class="dropdown-menu">
								<li><a href="">No new notifications</a></li>
							</ul>
						</li>
					</ul>
					
					<div class="nav pull-right">
						<jsp:include page="/username.jsp" />
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="container-fluid center-block">
		<div class="row-fluid">
			<div class="well span3" style="padding: 8px 0;">
				<ul class="nav nav-list">
					<li class="nav-header">Navigate</li>
					<li><a href="">Car Name</a></li>
					<li>
						<ul>
						<li><a href="">Expense Manager</a></li>
						<li><a href="">Maintenance Records</a></li>
						<li><a href="">Gas Mileage Tracking</a></li>
						<li><a href="">News</a></li>
						</ul>
					</li>
				</ul>
			</div>

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
			</div>
			
		</div>
	</div>
	
	<script type="text/javascript">	    
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
	
	    google.maps.event.addDomListener(window, 'load', Demo.init);
	</script>
	
	
</body>
</html>

