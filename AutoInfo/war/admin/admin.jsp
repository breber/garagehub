<%@ page language="java" contentType="text/html"%>
<!DOCTYPE html>
<html>
<head>
	<link type="text/css" href="/css/bootstrap.min.css" rel="stylesheet" />
	<script type="text/javascript" src="/js/jquery.min.js"></script>
	<script type="text/javascript" src="/js/bootstrap.min.js"></script>
	
	<script type="text/javascript">
		
		$().ready(function() {
			$("#deleteAllVehicles").click(function() {
				$.post('/admin/deletevehicles', function(data) {
					console.log(data);
				});
			});
		});
	
	</script>

	<title>Administrative Functions</title>
</head>
<body>

	<button id="deleteAllVehicles">Delete All Vehicles</button>

</body>
</html>