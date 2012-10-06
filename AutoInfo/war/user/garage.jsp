<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.data.UserVehicle"%>
<%@page import="java.util.List"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
	List<UserVehicle> vehicles = DatastoreUtils.getUserVehicles(user);
%>

<div class="container-fluid center-block">
	<div class="row-fluid">
		<div class="well span3" style="padding: 8px 0;">
			<ul class="nav nav-list">
				<li class="nav-header">Navigate</li>
				<li class="active">Garage</li>
				<li><a href="/user/addvehicle.jsp">Add Vehicle</a></li>
			</ul>
		</div>
	
		<div class="well well-small span9">
			<h2>Your Garage</h2>

			<% if (vehicles.isEmpty()) { %>
				<p>You don't have any vehicles registered.</p>
				<p>Register one <a href="/user/addvehicle.jsp">here</a>!</p>
			<% } else { %>
				<table class="table">
					<tr>
						<th>Year</th>
						<th>Make</th>
						<th>Model</th>
					</tr>
				<% for (UserVehicle v : vehicles) { %>
					<tr>
						<td><%=v.getYear() %></td>
						<td><%=v.getMake() %></td>
						<td><%=v.getModel() %></td>
					</tr>
				<% } %>
				</table>
			<% } %>
		</div>
	</div>
</div>
