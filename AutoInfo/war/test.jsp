
<!DOCTYPE html>
<html>
<head>

	
	
	
</head>
<body>
<script src="http://code.jquery.com/jquery-latest.js"></script>
	<script type="text/javascript">
		$.getJSON('http://api.mygasfeed.com/stations/radius/42.0657/-93.6928/5/reg/price/g7slhsg67l.json?callback=?', function(data) {
  var items = [];

  $.each(data, function(key, val) {
    alert(key);
alert(val);
  });

});
	</script>
<script language="JavaScript" src="http://j.maxmind.com/app/geoip.js"></script>
 
<br>Latitude:
<script language="JavaScript">document.write(geoip_latitude());</script>
<br>Longitude:
<script language="JavaScript">document.write(geoip_longitude());</script>

</body>
</html>