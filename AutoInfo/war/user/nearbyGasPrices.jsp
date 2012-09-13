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

	<title>CarHub</title>
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
				<h2>Nearby Gas Prices</h2>

				<form action="form_action.asp" method="get">
					<input type="checkbox" id="location" name="loaction" value="location" /> Detect my
					location<br /> <br /> Zip Code: <input type="text" name="zip" id="zip" /><br />
					<br /> <input type="button" onclick="getGasPrices();" value="Get Gas" />
				</form>
				
				<table class="table" id="table">
					<tr>
						<th>Name</th>
						<th>Location</th>
						<th>Price</th>
						<th>Last Updated</th>
					</tr>
				</table>

			</div>
		</div>
	</div>
	<script src="http://code.jquery.com/jquery-latest.js"></script>
	<script src="https://maps.googleapis.com/maps/api/js?sensor=false"></script>
 
	<script type="text/javascript">
	
	function getGasPrices(){
		$("#table").find("tr:gt(0)").remove();
		var geocoder = new google.maps.Geocoder();
		var isChecked = $('#location').attr('checked')?true:false;
		var JSONGasFeed;
		if(isChecked){
			getLocation();
				

			
		}else{
			var address = document.getElementById('zip').value;
	        geocoder.geocode( { 'address': address}, function(results, status) {
	          if (status == google.maps.GeocoderStatus.OK) {
	        	  var latLon = String(results[0].geometry.location);
	        	  var word = latLon.split(",")
	        	  var lat = word[0].substring(1);
	        	  var lon = word[1].substring(1, word[1].length-1);
	        	  JSONGasFeed = 'http://api.mygasfeed.com/stations/radius/'+lat+'/'+lon+'/5/reg/price/g7slhsg67l.json?callback=?';
				  displayGasPrices(JSONGasFeed);
	            }
	        });
		}
		
	}
	
	function showLocation(position) {
	  	var latitude = position.coords.latitude;
	  	var longitude = position.coords.longitude;
	  	JSONGasFeed = 'http://api.mygasfeed.com/stations/radius/'+latitude+'/'+longitude+'/5/reg/price/g7slhsg67l.json?callback=?';
		displayGasPrices(JSONGasFeed);
	}
	
	function getLocation(){
	   if(navigator.geolocation){
		   //30 seconds
	      var options = {timeout:30000};
	      navigator.geolocation.getCurrentPosition(showLocation, 
	                                               errorHandler,
	                                               options);
	   }else{
	      alert("Sorry, your browser does not support geolocation.");
	   }
	}
	
	function errorHandler(err) {
		  if(err.code == 1) {
		    alert("Error: Access is denied!");
		  }else if( err.code == 2) {
		    alert("Error: Position is unavailable!");
		  }
		}
	
	function displayGasPrices(JSONGasFeed){
		$.getJSON(JSONGasFeed, function(json) {
			$.each(json.stations, function(i, item){
				$('#table').append("<tr><td>"+item.station+"</td><td>"+item.address+"</td><td>"+item.reg_price+"</td><td>"+item.mid_date+"</td></tr>");

		    });
		});
	}
	</script>
</body>
</html>