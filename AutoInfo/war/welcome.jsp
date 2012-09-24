<%@page import="com.google.appengine.api.users.UserService"%>
<%@page import="com.google.appengine.api.users.UserServiceFactory"%>
<%@page language="java" contentType="text/html"%>

<%
	UserService user = UserServiceFactory.getUserService();
%>

<div class="container-fluid center-block">
	<div class="hero-unit">
		<h1>CarHub</h1>
		<p>A place for all your car related needs.</p>
		
		<p>Please log in to continue.</p>
	</div>
</div>