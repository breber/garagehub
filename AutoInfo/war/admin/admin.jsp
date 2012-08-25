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
	<div class="navbar navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
				<a class="brand" href="/">Automotive Info</a>
				<ul class="nav">
					<li><a href="/">Home</a></li>
				</ul>
				
				<ul class="nav pull-right">
					<jsp:include page="/username.jsp" />
				</ul>
			</div>
		</div>
	</div>

	<div class="container">
		<button id="deleteAllVehicles" class="btn btn-danger">Delete All Vehicles</button>
	</div>
</body>
</html>