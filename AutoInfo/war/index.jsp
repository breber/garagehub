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
					<% if (user.isLoggedIn()) { %>
					<jsp:include page="/user/navbar.jsp" />
					<% } %>
					<div class="nav pull-right">
						<jsp:include page="/username.jsp" />
					</div>
				</div>
			</div>
		</div>
	</div>

	<% if (user.isLoggedIn()) { %>
	<!-- TODO: include a separate page -->
	<%-- <jsp:include page="/user/garage.jsp" /> --%>
	<% } else { %>
	<jsp:include page="welcome.jsp" />
	<% } %>
</body>
</html>