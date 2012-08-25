<%@ page language="java" contentType="text/html"%>
<!DOCTYPE html>
<html>
<head>
	<link type="text/css" href="/css/bootstrap.min.css" rel="stylesheet" />
	<link type="text/css" href="/css/auto.css" rel="stylesheet" />
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
	<jsp:include page="/header.jsp">
		<jsp:param value="false" name="showAdminLink"/>
	</jsp:include>

	<div class="container">
		<button id="deleteAllVehicles" class="btn btn-danger">Delete All Vehicles</button>
	</div>
</body>
</html>