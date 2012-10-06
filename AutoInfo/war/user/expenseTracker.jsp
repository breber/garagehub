<%@page import="edu.se319.team1.carhub.data.UserVehicle"%>
<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.PathUtils"%>
<%@page import="java.util.List"%>
<%@page import="com.google.appengine.api.users.UserServiceFactory"%>
<%@page import="com.google.appengine.api.users.UserService"%>
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
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
	function addCategory() {
		alert("Trying to add category");
	}
</script>

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
				<h2>Expense Manager</h2>

				<h3>Total Money Spent: $1,003,304</h3>

				<div>
					<div class="btn-group" style="float: left"
						data-toggle="buttons-radio">
						<button type="button" class="btn">Most Recent Purchase</button>
						<button type="button" class="btn">1 M</button>
						<button type="button" class="btn">3 M</button>
						<button type="button" class="btn">1 Yr</button>
						<button type="button" class="btn">All</button>
						<button type="button" class="btn">Custom</button>
					</div>
					<div style="float: right">
						<input type="button" class="btn" onclick="addCategory();"
							value="Add Category +" />
					</div>
				</div>
				<table class="table table-striped table-bordered">


					<tr>
						<th>Fuel</th>
						<th>Repairs</th>
						<th>Periodic Maintenance</th>
						<th>Making It Look Good</th>
					</tr>

					<tr>
						<td>$1,390</td>
						<td>$1,000</td>
						<td>$0</td>
						<td>$23,000</td>
					</tr>

				</table>


				<br />

				<button style="float: left" type="button" class="btn btn-primary"
					data-toggle="collapse" data-target="#fuelExpenses">Show/Hide
					- Fuel Expenses</button>
				<input style="float: right" type="button" class="btn"
					value="Add Fuel Transaction +" /> <br /> <br />

				<div id="fuelExpenses" class="collapse in">
					<table class="table table-striped table-bordered">

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

				<button style="float: left" type="button" class="btn btn-primary"
					data-toggle="collapse" data-target="#RepairExpenses">Show/Hide
					- Repair Expenses</button>

				<input style="float: right" type="button" class="btn"
					value="Add Repair Transaction +" /> <br /> <br />
				<div id="RepairExpenses" class="collapse in">
					<table class="table table-striped table-bordered">

						<tr>
							<th>Date</th>
							<th>Amount</th>
							<th>Category</th>
							<th>Location</th>
							<th>Description</th>
						</tr>

						<tr>
							<td>2012-09-12 05:07:55</td>
							<td>$22.13</td>
							<td>Repair</td>
							<td>Butch's Body Shop</td>
							<td>I got angry and punched the car, Butch removed the dent.</td>
						</tr>

						<tr>
							<td>2012-09-05 03:25:101</td>
							<td>$500.23</td>
							<td>Repair</td>
							<td>Tony's Shop</td>
							<td>The transmission died in the middle of nowhere, got it
								fixed.</td>
						</tr>

					</table>
				</div>

				<button style="float: left" type="button" class="btn btn-primary"
					data-toggle="collapse" data-target="#MaintenanceExpenses">Show/Hide
					- Maintenance Expenses</button>
				<input style="float: right" type="button" class="btn"
					value="Add Maintenance Transaction +" /> <br /> <br />
				<div id="MaintenanceExpenses" class="collapse in">
					<table class="table table-striped table-bordered">

						<tr>
							<th>Date</th>
							<th>Amount</th>
							<th>Category</th>
							<th>Location</th>
							<th>Description</th>
						</tr>

						<tr>
							<td>2012-02-12 05:09:55</td>
							<td>$1.23</td>
							<td>Maintenance</td>
							<td>Jiffy Lube</td>
							<td>Oil change.</td>
						</tr>

						<tr>
							<td>2012-09-05 03:25:101</td>
							<td>$16.25</td>
							<td>Maintenance</td>
							<td>Auto Zone</td>
							<td>Got anti-freeze / coolant.</td>
						</tr>

					</table>
				</div>

				<button style="float: left" type="button" class="btn btn-primary"
					data-toggle="collapse" data-target="#VanityExpenses">Show/Hide
					- The Cost of Looking Good</button>
				<input style="float: right" type="button" class="btn"
					value="Add Looking Good Transaction +" /> <br /> <br />
				<div id="VanityExpenses" class="collapse in">
					<table class="table table-striped table-bordered">

						<tr>
							<th>Date</th>
							<th>Amount</th>
							<th>Category</th>
							<th>Location</th>
							<th>Description</th>
						</tr>

						<tr>
							<td>2012-09-12 02:37:05</td>
							<td>$1,000.03</td>
							<td>Looking Good</td>
							<td>Custom Colors</td>
							<td>New paint job, purple is my favorite</td>
						</tr>

						<tr>
							<td>2012-01-05 12:89:11</td>
							<td>$3,000</td>
							<td>Looking Good</td>
							<td>Creepy Colors</td>
							<td>Too hard to see car, changed color to Midnight Black</td>
						</tr>

						<tr>
							<td>2011-09-05 12:89:11</td>
							<td>$10,000</td>
							<td>Looking Good</td>
							<td>Decent Painters</td>
							<td>Painted car Camouflage, WIN!</td>
						</tr>

						<tr>
							<td>...</td>
						</tr>

					</table>
				</div>

			</div>
		</div>
	</div>
</body>
</html>