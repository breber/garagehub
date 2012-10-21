<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
%>
<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />

	<title>CarHub</title>
</head>
<body onload="getGasPrices()">
	<jsp:include page="/user/navbar.jsp" />

	<div class="container-fluid center-block">
		<div class="row-fluid">
			<div class="well">
				<h2>Nearby Gas Prices</h2>

				<form>
					<input onclick="hideZipCode();" type="checkbox" id="location" name="loaction" value="location" checked/> Detect my
					location
					<br /> <br /> 
					
					<section>
						<div style="float:left;">
							<label for="zip">Zip Code:</label><input type="text" name="zip" id="zip" disabled/>
						</div>
						<div style = "float:left; margin-left:20px;">
							<label for="radius">Search Radius:</label>
							<select name="radius" id="radius">
								<option value="1">1 Mile</option>
								<option value="2">2 Miles</option>
								<option value="3">3 Miles</option>
								<option value="4">4 Miles</option>
								<option SELECTED value="5">5 Miles</option>
								<option value="6">6 Miles</option>
								<option value="7">7 Miles</option>
								<option value="8">8 Miles</option>
								<option value="9">9 Miles</option>
								<option value="10">10 Miles</option>
								<option value="15">15 Miles</option>
								<option value="20">20 Miles</option>
								<option value="25">25 Miles</option>
								<option value="30">30 Miles</option>
							</select>
						</div>
						<div style="float:left; margin-left:20px;">
							<label for="grade">Fuel Grade:</label>
							<select name="grade" id="grade">
								<option value="reg">Regular</option>
								<option value="mid">Mid</option>
								<option value="pre">Premium</option>
								<option value="diesel">Diesel</option>
							</select>
						</div>
						<div style="float:left; margin-left:20px;">
							<label for="sort">Sort By:</label>
							<select name="sort" id="sort">
								<option value="price">Price</option>
								<option value="distance">Distance</option>
							</select>
						</div>
					</section>
					<br />
					<br />
					<section>
						<div style="float:left; clear:both;">
							<input type="button" class="btn" onclick="getGasPrices();" value="Get Gas" />
						</div>
					</section>
				</form>
				<br/>
				<br/>
				<table class="table pagination" id="table">
				</table>
				<div>Data Powered by www.myGasFeed.com.</div>
			</div>
		</div>
	</div>
	<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD6rEVLWJAAQ6p3IObKwkyGoAVQ_GQZnIg&sensor=false"></script>
 
	<script type="text/javascript">
			
	function getGasPrices() {
		$("#table").empty();
		
		var isChecked = $('#location').attr('checked')?true:false;
		var JSONGasFeed;
		if (isChecked) {
			getLocation();
		} else {
			useZipCode();
		}
	}
	
	function hideZipCode() {
		document.getElementById('zip').disabled = document.getElementById('location').checked;
	}
	
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
	}
	
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
	}
	
	function useLocation(position) {
		var lat = position.coords.latitude;
		var lon = position.coords.longitude;
		sendJSONRequest(lat, lon);
	}
	
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
	}
	
	function errorHandler(err) {
		if (err.code == 1) {
			alert("Error: Access is denied!");
		} else if (err.code == 2) {
			alert("Error: Position is unavailable!");
		}
	}
	
	function showLoading(){
		$('#table').append("<center>Loading...</center><br/>");
		$('#table').append('<center><img id="theImg" src="/img/ajax-loader.gif" /></center>');
	}
	
	function stopLoading(){
		$("#table").empty();
	}

	function displayGasPrices(JSONGasFeed){
		showLoading();
		$.getJSON(JSONGasFeed, function(json) {
			var grade = document.getElementById('grade').value;
			stopLoading();
			
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
	}
	</script>
</body>
</html>