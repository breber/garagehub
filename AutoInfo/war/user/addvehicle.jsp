<%@page import="edu.se319.team1.carhub.servlets.VehicleServlet"%>
<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
%>
<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />
	<script type="text/javascript" src="/js/addvehicle.js"></script>
	
	<title>CarHub</title>
</head>
<body>
	<jsp:include page="/user/navbar.jsp" />

	<div class="container-fluid center-block">
		<div class="well">
			<h2>Add Vehicle</h2>

			<form action="/user/addvehicle" method="post">
				<p>Make</p>
				<select id="makes" name="<%= VehicleServlet.NAME_MAKE %>">
					<option>Select a make</option>
					<% for (String s : DatastoreUtils.getListOfMakes()) { %>
						<option><%= s %></option>
					<% } %>
				</select>
	
				<p>Model</p>
				<select id="models" name="<%= VehicleServlet.NAME_MODEL %>">
					<option>Select a model</option>
				</select>
				
				<p>Year</p>
				<select id="years" name="<%= VehicleServlet.NAME_YEAR %>">
					<option>Select a year</option>
				</select>
				<br>
				<button type="submit" class="btn btn-primary">Submit</button>
			</form>
		</div>
	</div>
</body>
</html>