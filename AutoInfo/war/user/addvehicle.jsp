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
		<div class="well well-small">
			<h2>Add Vehicle</h2>

			<p>Make</p>
			<select id="makes">
				<option>Select a make</option>
				<% for (String s : DatastoreUtils.getListOfMakes()) { %>
					<option><%= s %></option>
				<% } %>
			</select>

			<p>Model</p>
			<select id="models">
				<option>Select a model</option>
			</select>
			
			<p>Year</p>
			<select id="years">
				<option>Select a year</option>
			</select>
		</div>
	</div>
</body>
</html>