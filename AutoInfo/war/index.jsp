<%@page import="com.google.appengine.api.users.UserServiceFactory"%>
<%@page import="com.google.appengine.api.users.UserService"%>
<%@page language="java" contentType="text/html"%>

<%
	UserService service = UserServiceFactory.getUserService();
	boolean isAdmin = service.isUserLoggedIn() && service.isUserAdmin();
%>
<!DOCTYPE html>
<html>
<head>
	<link type="text/css" href="/css/bootstrap.min.css" rel="stylesheet" />
	<link type="text/css" href="/css/auto.css" rel="stylesheet" />
	<script type="text/javascript" src="/js/jquery.min.js"></script>
	<script type="text/javascript" src="/js/bootstrap.min.js"></script>

	<title>Automotive Info</title>
</head>
<body>
	<jsp:include page="header.jsp">
		<jsp:param value="<%= isAdmin %>" name="showAdminLink"/>
	</jsp:include>

	<div class="container">
		<h2>Welcome...</h2>
		<p>Nothing exciting to see yet...</p>
	</div>
</body>
</html>