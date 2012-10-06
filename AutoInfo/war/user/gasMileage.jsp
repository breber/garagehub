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
				<h2>Gas Mileage Tracker</h2>

				<h3>MPG: 55.8</h3>
				<h3>Miles: 100,234</h3>

				<div class="btn-group" data-toggle="buttons-radio">
					<button type="button" class="btn">Most Recent Fuel Up</button>
					<button type="button" class="btn">1 M</button>
					<button type="button" class="btn">3 M</button>
					<button type="button" class="btn">1 Yr</button>
					<button type="button" class="btn">All</button>
					<button type="button" class="btn">Custom</button>
				</div>

				<table class="table">


					<tr>
						<th>Average MPG</th>
						<th>Miles Driven</th>
						<th>Gallons Used</th>
						<th>Average $ / Gallon</th>
					</tr>

					<tr>
						<td>55.8</td>
						<td>100,234</td>
						<td>501</td>
						<td>$3.29</td>
					</tr>

				</table>


				<br /> <input style="float: right" type="button" class="btn"
					value="Add Fuel Transaction +" /> <br /> <br />

				<table class="table">

					<tr>
						<th>Date</th>
						<th># Gallons</th>
						<th>Total Price</th>
						<th>$ / Gallon</th>
						<th>Location</th>
						<th>Odometer</th>
					</tr>

					<tr>
						<td>2012-09-12 05:07:44</td>
						<td>22.13</td>
						<td>$82.99</td>
						<td>$3.75</td>
						<td>Kum N' Go</td>
						<td>100,234</td>
					</tr>

					<tr>
						<td>2012-09-12 05:07:44</td>
						<td>15.32</td>
						<td>$50.50</td>
						<td>$3.62</td>
						<td>Amaco</td>
						<td>99,823</td>
					</tr>

					<tr>
						<td>2012-09-12 05:07:44</td>
						<td>10.23</td>
						<td>$20.44</td>
						<td>$3.39</td>
						<td>BP</td>
						<td>99,389</td>
					</tr>

					<tr>
						<td>2012-09-12 05:07:44</td>
						<td>2.02</td>
						<td>$6.05</td>
						<td>$3.01</td>
						<td>Philips 66</td>
						<td>98,978</td>
					</tr>

				</table>

			</div>
		</div>
	</div>
</body>
</html>