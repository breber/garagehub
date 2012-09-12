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
				<a class="btn btn-navbar" data-toggle="collapse"
					data-target=".nav-collapse"> <span class="icon-bar"></span> <span
					class="icon-bar"></span> <span class="icon-bar"></span>
				</a> <a class="brand" href="/">CarHub</a>

				<div class="nav-collapse collapse">
					<ul class="nav">
						<li class="dropdown"><a href="#" class="dropdown-toggle"
							data-toggle="dropdown">Garage <b class="caret hidden-phone"></b></a>
							<ul class="dropdown-menu">
								<li><a href="">Car 1</a></li>
								<li><a href="">Car 2</a></li>
								<li class="divider"></li>
								<li><a href="">Add Vehicle</a>
							</ul></li>
						<li class="dropdown"><a href="#" class="dropdown-toggle"
							data-toggle="dropdown">Tools <b class="caret hidden-phone"></b></a>
							<ul class="dropdown-menu">
								<li><a href="">Nearby Gas Prices</a></li>
								<li><a href="">Trip Planner</a></li>
							</ul></li>
						<li class="dropdown"><a href="#" class="dropdown-toggle"
							data-toggle="dropdown">Notifications <b
								class="caret hidden-phone"></b></a>
							<ul class="dropdown-menu">
								<li><a href="">No new notifications</a></li>
							</ul></li>
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