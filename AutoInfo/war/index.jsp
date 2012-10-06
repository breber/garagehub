<%@page import="com.google.appengine.api.users.UserServiceFactory"%>
<%@page import="com.google.appengine.api.users.UserService"%>
<%@page import="edu.se319.team1.carhub.UserWrapper"%>
<%@page language="java" contentType="text/html"%>

<%
	UserWrapper user = UserWrapper.getInstance(request.getSession(false));
%>
<!DOCTYPE html>
<html>
<head>
	<jsp:include page="/includes.jsp" />

	<title>CarHub</title>
</head>
<body>
	<jsp:include page="/user/navbar.jsp" />

	<% if (user.isLoggedIn()) { %>
	<jsp:include page="/user/garage.jsp" />
	<% } else { %>
	<jsp:include page="welcome.jsp" />
	<% } %>
</body>
</html>