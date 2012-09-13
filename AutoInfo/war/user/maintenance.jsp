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
				<h2>Maintenance Records</h2>
				
				<h3>Oil Changes</h3>
				<table class="table">
				
				<tr>
				<th>Date</th>
				<th>Price</th>
				<th>Service Provider</th>
				<th>Suggested Miles</th>
				<th>Suggested Date</th>
				<th>Picture</th>
				</tr>
				
				<tr>
				<td>3/12/2012</td>
				<td>$25.99</td>
				<td>Honda Dealership</td>
				<td>4000</td>
				<td>7/12/2012</td>
				<td><a>Picture</a>
				</tr>
				
				<tr>
				<td>12/13/2011</td>
				<td>$21.99</td>
				<td>Jiffy Lube</td>
				<td>3000</td>
				<td>3/13/2012</td>
				<td><a>Picture</a>
				</tr>
				
				</table>
				
				<h3>Car Washes</h3>
				<table class="table">
				
				<tr>
				<th>Date</th>
				<th>Price</th>
				<th>Service Provider</th>
				</tr>
				
				<tr>
				<td>3/12/2012</td>
				<td>$9.99</td>
				<td>Primp My Ride</td>
				</tr>
				
				<tr>
				<td>12/13/2011</td>
				<td>$10.99</td>
				<td>Greasy Joe's</td>
				</tr>
				
				</table>
				
				<h3>Miscellaneous</h3>
				<table class="table">
				
				<tr>
				<th>Description</th>
				<th>Date</th>
				<th>Price</th>
				<th>Service Provider</th>
				</tr>
				
				<tr>
				<td>Fix airbags</td>
				<td>7/11/2011</td>
				<td>$5000.00</td>
				<td>Airbag Fixer-Uppers, Inc.</td>
				</tr>
				
				<tr>
				<td>Clutch removal</td>
				<td>12/25/2010</td>
				<td>$400.00</td>
				<td>Stick 2 Auto Garage</td>
				</tr>
				
				</table>
			</div>
		</div>
	</div>
</body>
</html>