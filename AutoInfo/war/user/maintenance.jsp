<%@page import="edu.se319.team1.carhub.PathUtils"%>
<%@page import="java.util.List"%>
<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.data.UserVehicle"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	List<String> parsedPath = PathUtils.parsePath(request.getPathInfo());
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
	String carId = parsedPath.get(parsedPath.size() - 1);
	UserVehicle vehicle = DatastoreUtils.getUserVehicle(user, carId);
	String carName = vehicle.toString();
%>
<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />

	<title>CarHub</title>
</head>
<body>
	<jsp:include page="/user/navbar.jsp" />

	<div class="container-fluid center-block">
		<div class="row-fluid">
			<jsp:include page="/sideNav.jsp">
				<jsp:param value='<%=carName %>' name="carName"/>
				<jsp:param value='<%=carId %>' name="carId"/>
			</jsp:include>

			<div class="well span9">
				<h2>Maintenance Records</h2>
				<button class="btn btn-primary pull-right" type="button"
					onclick="parent.location='/user/addrecord.jsp'">Add Record</button>
				
				<h3>Oil Changes</h3>
				<table class="table table-striped table-bordered">
				
				<tr>
				<th>Date</th>
				<th>Price</th>
				<th>Service Provider</th>
				<th>Suggested Miles</th>
				<th>Suggested Date</th>
				<th>Receipt</th>
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
				<table class="table table-striped table-bordered">
				
				<tr>
				<th>Date</th>
				<th>Price</th>
				<th>Service Provider</th>
				<th>Receipt</th>
				</tr>
				
				<tr>
				<td>3/12/2012</td>
				<td>$9.99</td>
				<td>Primp My Ride</td>
				<td><a>Picture</a></td>
				</tr>
				
				<tr>
				<td>12/13/2011</td>
				<td>$10.99</td>
				<td>Greasy Joe's</td>
				<td><a>Picture</a></td>
				</tr>
				
				</table>
				
				<h3>Miscellaneous</h3>
				<table class="table table-striped table-bordered">
				
				<tr>
				<th>Description</th>
				<th>Date</th>
				<th>Price</th>
				<th>Service Provider</th>
				<th>Receipt</th>
				</tr>
				
				<tr>
				<td>Fix airbags</td>
				<td>7/11/2011</td>
				<td>$5000.00</td>
				<td>Airbag Fixer-Uppers, Inc.</td>
				<td><a>Picture</a></td>
				</tr>
				
				<tr>
				<td>Clutch removal</td>
				<td>12/25/2010</td>
				<td>$400.00</td>
				<td>Stick 2 Auto Garage</td>
				<td><a>Picture</a></td>
				</tr>
				
				</table>
			</div>
		</div>
	</div>
</body>
</html>