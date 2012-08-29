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
				<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</a>
			
				<a class="brand" href="/">Automotive Info</a>
				
				<div class="nav-collapse collapse">
					<ul class="nav">
						<li><a href="/">Home</a></li>
					</ul>
					
					<div class="nav pull-right">
						<jsp:include page="/username.jsp" />
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="container-fluid center-block">
		<div class="well well-small">
			<table class="table table-hover">
				<tr>
					<td>Reload Vehicles from Cars.com</td>
					<td>
						<form action="/cron/fetchvehicleinfo" method="GET">
							<button type="submit" class="btn pull-right">Reload</button>
						</form>
					</td>
				</tr>
				<tr>
					<td>Delete all Vehicles</td>
					<td>
						<form action="/admin/deletevehicles" method="POST">
							<button type="submit" class="btn btn-danger pull-right">Delete</button>
						</form>
					</td>
				</tr>
				<tr>
					<td>Delete all CarResponseString</td>
					<td>
						<form action="/admin/deletecarresponsestring" method="POST">
							<button type="submit" class="btn btn-danger pull-right">Delete</button>
						</form>
					</td>
				</tr>
				<tr>
					<td>Clear Server Cache</td>
					<td>
						<form action="/admin/clearmemcache" method="POST">
							<button type="submit" class="btn btn-danger pull-right">Delete</button>
						</form>
					</td>
				</tr>
			</table>
		</div>
	</div>
</body>
</html>