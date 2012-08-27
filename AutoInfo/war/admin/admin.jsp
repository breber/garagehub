<%@ page language="java" contentType="text/html"%>
<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />

	<title>Administrative Functions</title>
</head>
<body>
	<div class="navbar navbar-inverse navbar-fixed-top">
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
		<div class="well well-small">
			<form action="/admin/deletevehicles" method="POST">
				<button type="submit" class="btn btn-danger">Delete All Vehicles</button>
			</form>
			
			<form action="/admin/deletecarresponsestring" method="POST">
				<button type="submit" class="btn btn-danger">Delete All CarResponseString</button>
			</form>
			
			<form action="/admin/clearmemcache" method="POST">
				<button type="submit" class="btn btn-danger">Clear Server Cache</button>
			</form>
		</div>
	</div>
</body>
</html>