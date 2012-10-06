<%@page import="edu.se319.team1.carhub.data.DatastoreUtils"%>
<%@page import="edu.se319.team1.carhub.data.UserVehicle"%>
<%@page import="java.util.List"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
	List<UserVehicle> vehicles = DatastoreUtils.getUserVehicles(user);
%>
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
				<ul class="nav">
					<% if (user != null && user.isLoggedIn()) { %>
					<li class="dropdown">
						<a href="#" class="dropdown-toggle"	data-toggle="dropdown">Garage <b class="caret hidden-phone"></b></a>
						<ul class="dropdown-menu">
							<% for (UserVehicle v : vehicles) { %>
							<li><a href="/user/car.jsp?carName=<%=v.getIdentifier()%>"><%= v.toString() %></a></li>
							<% } %>
							<% if (!vehicles.isEmpty()) { %>
							<li class="divider"></li>
							<% } %>
							<li><a href="/user/addvehicle.jsp"><i class="icon-plus"></i> Add Vehicle</a>
						</ul>
					</li>
					<% } %>
					<li class="dropdown">
						<a href="#" class="dropdown-toggle"	data-toggle="dropdown">Tools <b class="caret hidden-phone"></b></a>
						<ul class="dropdown-menu">
							<li><a href="/user/nearbyGasPrices.jsp">Nearby Gas Prices</a></li>
							<li><a href="/user/tripPlanner.jsp">Trip Planner</a></li>
						</ul>
					</li>
					<% if (user != null && user.isLoggedIn()) { %>
					<li class="dropdown">
						<a href="#" class="dropdown-toggle"	data-toggle="dropdown">Notifications <span class="badge badge-important">2</span> <b class="caret hidden-phone"></b></a>
						<ul class="dropdown-menu">
							<li><a href="">Car A: Oil change due in 100 miles</a></li>
							<li><a href="">Car B: Has not been washed in 5 years</a></li>
						</ul>
					</li>
					<% } %>
				</ul>
				
				<div class="nav pull-right">
					<jsp:include page="/username.jsp" />
				</div>
			</div>
		</div>
	</div>
</div>
