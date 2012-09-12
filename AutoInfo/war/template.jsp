






<!DOCTYPE html>
<html>
<head>


<meta name="viewport"
	content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<link type="text/css"
	href="http://automotiverecords.appspot.com/css/bootstrap.min.css"
	rel="stylesheet" />
<link type="text/css"
	href="http://automotiverecords.appspot.com/css/bootstrap-responsive.min.css"
	rel="stylesheet" />
<link type="text/css"
	href="http://automotiverecords.appspot.com/css/auto.css"
	rel="stylesheet" />
<script type="text/javascript"
	src="http://automotiverecords.appspot.com/js/jquery.min.js"></script>
<script type="text/javascript"
	src="http://automotiverecords.appspot.com/js/bootstrap.min.js"></script>

<title>Automotive Info</title>
</head>
<body>
	<div class="navbar navbar-inverse navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
				<a class="btn btn-navbar" data-toggle="collapse"
					data-target=".nav-collapse"> <span class="icon-bar"></span> <span
					class="icon-bar"></span> <span class="icon-bar"></span>
				</a> <a class="brand" href="/">Automotive Info</a>

				<div class="nav-collapse collapse">
					<ul class="nav">
						<li><a href="/">Garage</a></li>
					</ul>
					<ul class="nav">
						<li class="dropdown"><a href="#" class="dropdown-toggle"
							data-toggle="dropdown">Tools <b class="caret hidden-phone"></b></a>
							<ul class="dropdown-menu">
								<li><a href="">Nearby Gas Prices</a></li>
								<li><a href="">Trip Planner</a></li>
							</ul></li>
					</ul>

					<div class="nav pull-right">







						<ul class="nav">
							<li class="hidden-phone"><a
								href="http://gravatar.com/emails" style="padding: 0 0 0;"
								rel="tooltip" title="Change your avatar at gravatar.com"
								data-placement="bottom"> <img
									src="http://www.gravatar.com/avatar/ba9382294b60b3843d5fd1afd3da7962?s=40" />
							</a></li>
							<li class="dropdown"><a href="#" class="dropdown-toggle"
								data-toggle="dropdown">user@google.com <b
									class="caret hidden-phone"></b></a>
								<ul class="dropdown-menu">

									<li><a href="/admin/admin.jsp">Admin</a></li>

									<li><a href="#">Settings</a></li>
									<li class="divider"></li>
									<li><a href="/_ah/logout?continue=%2F">Logout</a></li>
								</ul></li>
						</ul>


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
					<li><a href="">Garage</a></li>
					<li><a href="/user/addvehicle.jsp">Add Vehicle</a></li>
					<li class="active">Find Gas</li>
					<li><a href="">Expense Manager</a></li>
					<li><a href="">Maintenance Tracking</a></li>
					<li><a href="">Trip Planner</a></li>
				</ul>
			</div>

			<div class="well well-small span9">
				<h2>Nearby Gas Prices</h2>

				<form action="form_action.asp" method="get">
					<input type="checkbox" name="vehicle" value="Bike" /> Detect my
					location<br /> <br /> Zip Code: <input type="text" name="fname" /><br />
					<br /> <input type="submit" value="Get Gas" />
				</form>
			</div>
		</div>
	</div>


</body>
</html>